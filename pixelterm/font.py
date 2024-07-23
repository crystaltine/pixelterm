from typing import Dict, TYPE_CHECKING
from PIL import Image
import numpy as np

if TYPE_CHECKING:
    from pixelterm_types import RGBTuple, RGBATuple

class Font:
    """ Represents a monospaced font (parsed from images) that can be drawn to the screen. """
    
    font1: "Font" = ...
    """ The default Pixelterm monospaced font. Should be initialized upon importing the package. """

    PARSER_FORMAT = [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "abcdefghijklmnopqrstuvwxyz",
        "~`0123456789-_+=",
        "!@#$%^&*()[{]}|\\;:'\",<.>/?",
    ]
    
    def __init__(self, path_to_font_png: str):
        """
        Initializes and loads each charcter of the font into this object.
        
        # IMPORTANT FORMATTING INFO:
        Font PNGs MUST be formatted in the following way:
        Padding of 1px between ALL symbols. No padding on the outlines
        
        Symbols must be in the following order (newlines matter)
        ```
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        abcdefghijklmnopqrstuvwxyz
        ~`0123456789-_+=
        !@#$%^&*()[{]}|\;:'",<.>/?
        ```
        
        Notes: This means font definition images should always be 25 + 26*font_width pixels wide, 
        and 4*font_height + 3 pixels tall. The font size that this function looks for is auto-calculated
        based on the image size. For example, if we find that the image is 155x27,
        we determine that 25+26w=155 => w=5, and 4h+3=27 => h=6.
        
        If the dimensions of the image do not conform to these dimensional constraints, this constructor raises an error.
        """
        
        self.filepath = path_to_font_png
        self.symbols: Dict[str, np.ndarray] = {}
        """ Map of all symbols to their respective images, as 3D numpy arrays. """
        
        # load image into np arr
        img = np.array(Image.open(path_to_font_png))
        
        assert img.shape[0] % 4 == 3, "[Font/__init__]: Font image height must be 4n+3 (for some int n) pixels tall. Got: " + str(img.shape[0])
        assert img.shape[1] % 26 == 25, "[Font/__init__]: Font image width must be 26n+25 (for some int n) pixels wide. Got: " + str(img.shape[1])
        
        self.font_width = (img.shape[1] - 25) // 26
        """ Width of each character, in pixels """
        self.font_height = (img.shape[0] - 3) // 4
        """ Height of each character, in pixels """
        
        for i in range(len(Font.PARSER_FORMAT)):
            
            symbols_to_define = Font.PARSER_FORMAT[i]
            curr_row = img[i*(self.font_height+1):i*(self.font_height+1)+self.font_height]
            
            
            for j in range(len(symbols_to_define)):
                self.symbols[symbols_to_define[j]] = curr_row[:, j*(self.font_width+1):(j+1)*(self.font_width+1)-1]
                
                
        # lastly, define space as just an empty (0,0,0,0) array of same shape as the other symbols
        self.symbols[' '] = np.zeros_like(self.symbols['A'])
    
    def get_width_of(self, num_chars: int) -> int:
        """ Returns the pixel width of a string of len `num_chars` if it were to be drawn in this font. """
        return num_chars*self.font_width + (num_chars-1) # add spacing between characters
       
    def get_height(self) -> int:
        """ Returns the pixel height of all characters in this font. """
        return self.font_height
    
    def __getitem__(self, key: str) -> np.ndarray:
        """
        Returns the image of the symbol specified. KeyError if the symbol does not exist.
        
        Args:
            key: The character (e.g. "a", "*", etc.) to get the image of.
        """
        return self.symbols[key] 
    
    def get(self, key: str) -> np.ndarray:
        """
        Returns the image of the symbol specified. None if the symbol does not exist.
        
        Args:
            key: The character (e.g. "a", "*", etc.) to get the image of.
        """
        return self.symbols.get(key)
    
    def assemble(self, text: str, color: "RGBTuple | RGBATuple" = (255, 255, 255), spacing: int = 1) -> np.ndarray:
        """ Converts some text and a color into a single image of the text, returned as a numpy array of pixels. 
        If `text` contains any characters that are not supported by this font, a ValueError is raised. 
        
        `spacing` specifies how many pixels to put in between characters. Default is 1.
        """
        
        # alloc enough space to accomodate height 
        projected_height = self.font_height
        projected_width = len(text)*self.font_width + (len(text))*spacing
        concat_pixels = np.empty((projected_height, projected_width, 4), dtype=np.uint8)
        
        for i in range(len(text)):
            pixels = self.get(text[i])
            if pixels is None: raise ValueError(f"[Font/assemble]: Can't render unsupported character '{text[i]}' for font @ {self.filepath}")

            # add spacing to the right of the character
            pixels = np.pad(pixels, ((0, 0), (0, spacing), (0, 0)), mode='constant', constant_values=0)
            concat_pixels[:,i*(self.font_width+1):i*(self.font_width+1)+self.font_width+spacing] = pixels
            
        # remove the last spacing
        concat_pixels = concat_pixels[:,:-spacing]
            
        # colorize - replace all non-transparent pixels with the color
        rgba_color = color + (255,) if len(color) == 3 else color
        concat_pixels[concat_pixels[:,:,3] != 0] = rgba_color
        
        return concat_pixels
