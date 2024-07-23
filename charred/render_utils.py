import sys
import numpy as np
from skimage.draw import line, disk
from .charred_types import Anchor, RGBTuple, Tuple
from os import get_terminal_size

def term_width() -> int:
    """ Returns the width in cols (pixels) of the terminal. """
    try:
        return get_terminal_size().columns
    except OSError:
        from shutil import get_terminal_size as gts
        return gts().columns

def term_height() -> int:
    """ Returns the height in PIXELS (2*rows) of the terminal. """
    try:
        return 2*get_terminal_size().lines
    except OSError:
        from shutil import get_terminal_size as gts
        return gts().lines

def move_xy(x: int, y: int) -> str:
	""" Returns the ANSI escape code to move the cursor to the specified x, y position. """
	return f"\033[{y+1};{x+1}H"

def betterprint(text: str) -> None:
    """ uses sys.stdout.write to write text to the terminal without a newline, infinitesimally faster than print?
    Also doesnt add a color reset code at the end just for micro-optimization (i think). """
    #sys.stdout.write(text)
    print("\r" + text, end="")
    
def fcode(fg: RGBTuple = None, bg: RGBTuple = None) -> str:
    '''
    Outputs escape code for setting the foreground and background colors for text.
    - only accepts 3-tuple RGB255 for colors
    - no letter styling (bold, italic, etc.)
    - no predefined color names
    '''
    
    format_str = ''
    
    if fg is not None:
        format_str += '\033[38;2;{};{};{}m'.format(*fg)
    if bg is not None:
        format_str += '\033[48;2;{};{};{}m'.format(*bg)
        
    return format_str

def blend_rgba_img_onto_rgb_img(original: np.ndarray, new: np.ndarray) -> np.ndarray:
    """
    Blends two entire 2D arrays of pixels (so, techincally, 3D arrays) together, expecting
    that the original image is fully opaque and the new image has transparency. If the new
    image is RGB-based (no alpha, 3 channels), it will be treated as fully opaque.
    
    Will clip the new image to the size of the original image, anchoring the top left corner.
    """
    
    # if the new image has no alpha, just return the new image
    if new.shape[2] == 3:
        return new
    
    clipped_new = new[:original.shape[0], :original.shape[1]]
    
    # if new image has 0 in any shape, return
    if clipped_new.shape[0] == 0 or clipped_new.shape[1] == 0:
        return original

    new_rgb = clipped_new[..., :3] # "img" without alpha
    new_alpha = clipped_new[..., 3] / 255.0 # array of just the alpha values
    # blend arrays in PARALLEL (yayyyyyyyy!!!!) 
    #Logger.log(f"blend rgba into rgb: shapes of original, new: {original.shape}, {new.shape}")
    blended_rgb = new_rgb*new_alpha[..., np.newaxis] + original*(1 - new_alpha[..., np.newaxis])

    # return as uint8 types since this returns floats
    return blended_rgb.astype(np.uint8)

def blend_rgba_img_onto_rgb_img_inplace(original: np.ndarray, new: np.ndarray) -> None:
    """ Same as `blend_rgba_img_onto_rgb_img`, but modifies the original array in place. """
    original[:] = blend_rgba_img_onto_rgb_img(original, new)

def draw_line(image: np.ndarray, pos1: tuple, pos2: tuple, color: RGBTuple, width: int = 1) -> None:
    """
    draw a fully opaque line of color `color` on the image from pos1= (x1, y1) to pos2= (x2, y2).
    modifies `image` in place, does not return anything.
    """
    
    x1, y1 = pos1
    x2, y2 = pos2
    
    # Get the coordinates of the line
    rr, cc = line(y1, x1, y2, x2)

    # Clip the coordinates to be within the image dimensions
    rr_clipped = np.clip(rr, 0, image.shape[0]-1)
    cc_clipped = np.clip(cc, 0, image.shape[1]-1)
    
    # for all the rrs that were clipped off, remove the corresponding ccs, otherwise it creates a flat line at the edge
    rr_diffs = rr - rr_clipped
    cc_clipped = cc_clipped[rr_diffs == 0]
    
    #cc_diffs = cc - cc_clipped
    #rr_clipped = rr_clipped[cc_diffs == 0]

    for r, c in zip(rr, cc):
        rr_disk, cc_disk = disk((r, c), radius=width)
        
        # Clip the coordinates to be within the image dimensions
        rr_disk = np.clip(rr_disk, 0, image.shape[0] - 1)
        cc_disk = np.clip(cc_disk, 0, image.shape[1] - 1)
        
        image[rr_disk, cc_disk] = color

def adjust_for_anchor(x: int, y: int, size_x: int, size_y: int, target_anchor: Anchor) -> Tuple[int, int]:
    """
    Returns the actual coordinates of the top left corner of a rectangle of size (size_x, size_y) 
    that is anchored at (x, y) with the specified anchor.

    For example:
    `adjust_for_anchor(5, 5, 10, 12, 'center') -> (0, -1)` (center of rect @ 5, 5, so its top left is 0, -1)

    If sizes are odd, anchors are rounded down.
    """
    
    match target_anchor:
        case "top-left":
            pass
        case "center":
            x -= size_x // 2
            y -= size_y // 2
        case "top-right":
            x -= size_x - 1
        case "bottom-left":
            y -= size_y - 1
        case "bottom-right":
            x -= size_x - 1
            y -= size_y - 1
        case "right":
            x -= size_x - 1
            y -= size_y // 2
        case "left":
            y -= size_y // 2
        case "bottom":
            x -= size_x // 2
            y -= size_y - 1
        case "top":
            x -= size_x // 2
            
        case _:
            raise ValueError(f"Invalid anchor {target_anchor}, expected one of {Anchor.__args__}")
        
    return x, y

def first_diff_color(arr1: np.ndarray, arr2: np.ndarray) -> int | None:
    """
    Returns the index of the first different color in the two arrays. If exactly the same, returns None.
    Both arrays must be 2d numpy arrays, with the 2d axis being 4 long (r,g,b,a)
    
    For example:
    
    `first_diff_color([[1, 2], [3, 6], [4, 200]], [[1, 2], [3, 9], [4, 202]]) -> 1`
    (both i=2 and i=3 are different, but returns 1 since the second pixel is the first different one)
    """
    differences = np.any(arr1 != arr2, axis=1)
    #Logger.log(f"first diff: arr1 first 10 elements: {arr1[:10]}, arr2 first 10 elements: {arr2[:10]}" )
    first_diff = np.argmax(differences)
    
    # if flat index is 0, investigate: it could be that all are the same, or that the first element is actually different
    if first_diff == 0 and not differences[0]:
        return None
    
    return first_diff

def last_diff_color(arr1: np.ndarray, arr2: np.ndarray) -> int | None:
    """
    Returns the index of the last different color in the two arrays. If exactly the same, returns None.
    Both arrays must be 2d numpy arrays, with the 2d axis being 4 long (r,g,b,a)
    
    For example:
    
    `last_diff_color([[1, 2], [3, 6], [4, 200]], [[1, 9], [3, 9], [4, 200]]) -> 1`
    (both i=0 and i=1 are different, but returns 1 since the second pixel is the last different one)
    """
    differences = np.any(arr1 != arr2, axis=1)
    last_diff = len(differences) - np.argmax(differences[::-1]) - 1
    
    # if flat index is last, investigate: it could be that all are the same, or that the first element is actually different
    if last_diff == len(differences) - 1 and not differences[-1]:
        return None
    
    return last_diff

def lesser(a: int | None, b: int | None) -> int | None:
    """
    Takes two numbers that are either None or an int.
    
    If both are not None, then returns the lesser of the two
    If one of them is None, returns the one that isn't None
    If both are None, returns None
    """
    if a is None:
        return b
    if b is None:
        return a
    return min(a, b)

def greater(a: int | None, b: int | None) -> int | None:
    """
    Takes two numbers that are either None or an int.
    
    If both are not None, then returns the greater of the two
    If one of them is None, returns the one that isn't None
    If both are None, returns None
    """
    if a is None:
        return b
    if b is None:
        return a
    return max(a, b)    
