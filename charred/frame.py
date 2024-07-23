from typing import Literal, Tuple
from .render_utils import (
    fcode, blend_rgba_img_onto_rgb_img_inplace, adjust_for_anchor,
    first_diff_color, last_diff_color, lesser, greater, draw_line,
    betterprint, move_xy, term_height, term_width
)
import numpy as np
from PIL import Image
from .font import Font
from .charred_types import RGBTuple, RGBATuple, Anchor

class CharredFrame:
    """
    Wrapper over a 2D array of pixels for rendering to the screen.
    
    Images with transparency can be added to a CharredFrame, however the final compiled result that gets
    printed to the screen will assume all alpha values are 255 (opaque).
    """

    width: int
    """ Width in pixels (1px = width of 1 monospaced character) """
    height: int
    """ Height in pixels (2px = height of 1 monospaced character). Should always be even. """
    pos: Tuple[int, int]
    """ (x, y) of the top left pixel of the frame. y should always be even. """
    pixels: np.ndarray
    """ 2d array of pixels. Each pixel is an rgb tuple. (0, 0) is the top left of the frame, not the top left of the screen. """

    def __init__(self, size: Tuple[int | None, int | None] = (None, None), pos: Tuple[int | None, int | None] = (0, 0)) -> None:
        """ Optional params:
        - `size`: tuple (width, height) in pixels. None values will default to the terminal's width/height.
        - `pos`: tuple (x, y) in pixels, where the top left corner of the frame will be placed. Defaults to (0, 0) (top left of screen)
        
        NOTE: Height and y-position MUST both be even. Each character is 2 pixels tall, and we cant render half-characters.
        """
        
        assert size[1] is None or size[1] % 2 == 0, f"[CharredFrame/__init__]: height must be even, instead got {size[1]}"
        assert pos[1] is None or pos[1] % 2 == 0, f"[CharredFrame/__init__]: y position must be even, instead got {pos[1]}"
        
        self.width = size[0] if size[0] is not None else term_width()
        self.height = size[1] if size[1] is not None else term_height()
        self.pos = pos
        self.pixels: np.ndarray = np.zeros((self.height, self.width, 3), dtype=np.uint8)

    def __eq__(self, other: "CharredFrame") -> bool:
        return np.array_equal(self.pixels, other.pixels)
    
    def __ne__(self, other: "CharredFrame") -> bool:
        return not self.__eq__(other)

    def render_raw(self) -> None:
        """ Rerenders the FULL frame to the screen, without the need for a previous frame. 
        Keep in mind, this is quite slow and should only be used for rendering things like first frames where there is no previous frame to diff from. """
            
        for i in range(0, self.height, 2):
            string = ""
            for j in range(self.width):
                string += fcode(self.pixels[i,j], self.pixels[i+1,j]) + '▀' # for quick copy: ▀
            
            #compiled_str += string + "\n"
            #betterprint(move_xy(self.pos[0], (i+self.pos[1])//2) + f"\x1b[0m{(i+self.pos[1])//2}{string[1:]}")
            betterprint(move_xy(self.pos[0], (i+self.pos[1])//2) + string)

    def render(self, prev_frame: "CharredFrame") -> None:
        """ Prints the frame to the screen.
        Optimized by only drawing the changes from the previous frame. """
        
        final_string = ""

        i = 0
        for top_row_index in range(0, self.height, 2):       
            first_diff_row1 = first_diff_color(self.pixels[top_row_index], prev_frame.pixels[top_row_index])
            first_diff_row2 = first_diff_color(self.pixels[top_row_index+1], prev_frame.pixels[top_row_index+1])
            
            last_diff_row1 = last_diff_color(self.pixels[top_row_index], prev_frame.pixels[top_row_index])
            last_diff_row2 = last_diff_color(self.pixels[top_row_index+1], prev_frame.pixels[top_row_index+1])
            
            print_start = lesser(first_diff_row1, first_diff_row2)
            print_end = greater(last_diff_row1, last_diff_row2)
            
            start, end = print_start, print_end
            
            # if both are None, that means the rows were the exact same, so we don't need to print anything
            if start is None and end is None:
                #Logger.log(f"Skipping row {i} since it's the same as the previous row!")
                i += 1
                continue

            final_string += move_xy(int(start)+self.pos[0], i+self.pos[1]//2)
            string = ""
            # get a numpy array of which indices are repeat colors (so we can skip fcode)
            color_strip = self.pixels[i*2:i*2+2, start:end+1]
            colors_diffs = np.any(color_strip[:, 1:] != color_strip[:, :-1], axis=(0, 2))
            """ [diff(1, 0), diff(2, 1), ...]. True if different, False if same. """
            #Logger.log(f"color strip 1 first 5: {color_strip[0, :5]}")
            #Logger.log(f"color strip 2 first 5: {color_strip[1, :5]}")
            #
            #Logger.log(f"colors_diffs: {colors_diffs[:5]}")
            
            # add the first pixel
            string += fcode(self.pixels[i*2,start], self.pixels[i*2+1,start]) + '▀'

            for j in range(start+1, end+1):
                # if colors_diffs is True for the current pixel, that means the colors are different from the previous pixel
                # in that case we have to re-fcode
                if colors_diffs[j-start-1]:
                    string += fcode(self.pixels[i*2,j], self.pixels[i*2+1,j]) + '▀'
                else:
                    string += '▀'
            # while loop ize ^^^

            #Logger.log(f"[CharredFrame/render]: str construction: {perf_counter()-start_time_2:4f}")
            # go to coordinates in terminal, and print the string
            # terminal coordinates: start, i
            
            #Logger.log_on_screen(GDConstants.term, f"[CharredFrame/render]: printing@{int(start) + self.pos[0]}, {i + self.pos[1]//2} for len {end-start+1}")
            #Logger.log_on_screen(GDConstants.term, f"[CharredFrame/render]: printing@{int(start) + self.pos[0]},{i + self.pos[1]//2}: \x1b[0m[{string}\x1b[0m]")
            #start_time_2 = perf_counter()
           # betterprint(move_xy(int(start)+self.pos[0], i+self.pos[1]//2) + string)
            #print_buffer.append(((int(start)+self.pos[0], i+self.pos[1]//2), string))
            final_string += string
            i += 1
            #Logger.log(f"[CharredFrame/render]: strlen={len(string)}: {perf_counter()-start_time_2:4f}")
        
        # combine all the print calls into a single call
        #for coords, string in print_buffer:
        #    final_string += move_xy(*coords) + string
            
        betterprint(final_string)
        
        #Logger.log(f"[CharredFrame/render]: print to terminal: {perf_counter()-start_time:4f}")

    def fill(self, color: RGBTuple) -> None:
        """ Fills the entire canvas with the given color. RGB (3-tuple) required. Should be pretty efficient because of numpy. """
        assert len(color) == 3, f"[FrameLayer/fill]: color must be an rgb (3 ints) tuple, instead got {color}"
        self.pixels[:,:] = color
        
    def fill_with_gradient(
        self, 
        color1: RGBTuple, 
        color2: RGBTuple, 
        direction: Literal["horizontal", "vertical"] = "horizontal"
        ) -> None:
        """ Fills the entire canvas with a gradient from color1 to color2.
        
        horizontal=color changes from left to right, vertical=color changes from top to bottom.
        """
        
        # create a gradient
        if direction == "horizontal":
            gradient = np.linspace(color1, color2, self.width)
            
            # fill each row with the gradient
            for i in range(self.height):
                self.pixels[i] = gradient
            
        elif direction == "vertical":
            gradient = np.linspace(color1, color2, self.height)
            
            for i in range(self.width):
                self.pixels[:,i] = gradient

    def add_rect(
        self, 
        color: RGBTuple | RGBATuple, 
        x: int, y: int, 
        width: int, height: int,
        outline_width: int = 0,
        outline_color: RGBTuple | RGBATuple = (0,0,0,0),
        anchor: Anchor = "top-left",
        ) -> None:
        """ Places a rectangle on the frame with the given RGBA color and position.
        Optionally, can add an outline to the rectangle with the given width and color. 
        Can also specify what part of the rectangle x and y refer to. (default is top left)"""

        # add alpha to color/outline if it's an rgb tuple
        
        if color is None:
            return
        
        if len(color) == 3:
            color = (*color, 255)
        if len(outline_color) == 3:
            outline_color = (*outline_color, 255)
            
        x = round(x)
        y = round(y)
        width = round(width)
        height = round(height)
            
        rect_as_pixels = np.full((height+outline_width*2, width+outline_width*2, 4), outline_color, dtype=np.uint8)
        
        # set the middle of rect_as_pixels to the color
        rect_as_pixels[outline_width:outline_width+height, outline_width:outline_width+width] = color
        
        y1 = y - outline_width
        y2 = y + height + outline_width
        x1 = x - outline_width
        x2 = x + width + outline_width
        
        x1, y1 = adjust_for_anchor(x1, y1, rect_as_pixels.shape[1], rect_as_pixels.shape[0], anchor)
        
        # if any coords go out of bounds, set it to the edge of the frame and clip the rect_as_pixels
        clipped_y1 = max(0, y1)
        clipped_y2 = min(self.height, y2)
        clipped_x1 = max(0, x1)
        clipped_x2 = min(self.width, x2)
        
        offset_y1 = clipped_y1 - y1
        offset_y2 = clipped_y2 - y2
        offset_x1 = clipped_x1 - x1
        offset_x2 = clipped_x2 - x2
        
        # clip the rect_as_pixels
        clipped_rect_as_pixels = rect_as_pixels[
            int(offset_y1):int(rect_as_pixels.shape[0]-offset_y2), 
            int(offset_x1):int(rect_as_pixels.shape[1]-offset_x2)
        ]
        
        blend_rgba_img_onto_rgb_img_inplace(
            self.pixels[
                clipped_y1:clipped_y2,
                clipped_x1:clipped_x2
            ], clipped_rect_as_pixels
        )
        
    def add_large_text(
        self, 
        x: int, y: int, 
        font: Font, 
        text: str, 
        anchor: Anchor = "top-left",
        color: RGBTuple | RGBATuple = (255,255,255)) -> None:
        """       
        Draws a font to the pixel array at the specified x and y values based on anchor.
        
        x and y should be relative to the top left corner of the frame.
        
        Note: Fonts SHOULD be monospaced.
        """
        
        pixels = font.assemble(text, color)
            
        # find the top left corner where the text should be placed
        left, top = adjust_for_anchor(x, y, pixels.shape[1], pixels.shape[0], anchor)
        
        # clip to 0, 0
        clipped_left = max(0, left)
        clipped_top = max(0, top)
        
        # these should always be nonnegative
        offset_top = clipped_top - top
        offset_left = clipped_left - left
        
        # if completely offscreen, return
        #if offset_top >= pixels.shape[0] or offset_left >= pixels.shape[1]:
        #    return

        blend_rgba_img_onto_rgb_img_inplace(
            self.pixels[clipped_top:clipped_top+pixels.shape[0]-offset_top, clipped_left:clipped_left+pixels.shape[1]-offset_left],
            pixels[offset_top:, offset_left:]
        )

    def add_image_from_filepath(self, filepath: str, x: int, y: int, anchor: Anchor = "top-left") -> None:
        """ Adds an image to the frame at the given position. """
        pixels = np.array(Image.open(filepath))
        self.add_image_from_pixels(pixels, x, y, anchor)

    def add_image_from_pixels(self, pixels: np.ndarray, x: int, y: int, anchor: Anchor = "top-left") -> None:
        """ Add an array of pixels with the image's `anchor` positioned at (x, y). """
        #Logger.log(f"[FrameLayer/add_pixels_topleft]: adding pixels at {x}, {y}, size {pixels.shape}")

        x, y = adjust_for_anchor(x, y, pixels.shape[1], pixels.shape[0], anchor)

        # if x or y are negative, clip them
        clipped_y1 = max(0, y)
        #clipped_y2 = min(self.height, y+pixels.shape[0])
        clipped_x1 = max(0, x)
        #clipped_x2 = min(self.width, x+pixels.shape[1])
        
        # these should always be nonnegative
        offset_x1 = clipped_x1 - x
        #offset_x2 = clipped_x2 - x
        offset_y1 = clipped_y1 - y
        #offset_y2 = clipped_y2 - y
        
        if offset_x1 >= pixels.shape[1] or offset_y1 >= pixels.shape[0]:
            #Logger.log(f"[FrameLayer/add_pixels_topleft]: clipped off all pixels, returning")
            return

        blend_rgba_img_onto_rgb_img_inplace(
            self.pixels[int(clipped_y1):int(clipped_y1+pixels.shape[0]-offset_y1), int(clipped_x1):int(clipped_x1+pixels.shape[1]-offset_x1)],
            pixels[int(offset_y1):self.height, int(offset_x1):self.width]
        )

    def add_line(self, pos1: Tuple[int, int], pos2: Tuple[int, int], color: RGBTuple, width: int = 1) -> None:
        """ Draws a non-antialiased line between two points on the frame. Width defaults to 1."""
        draw_line(self.pixels, pos1, pos2, color, width)
    
    def copy(self) -> "CharredFrame":
        """ Returns a deep copy of this CharredFrame. (except for the terminal reference) """
        new_frame = CharredFrame((self.width, self.height), self.pos)
        new_frame.pixels = np.copy(self.pixels)
        return new_frame
