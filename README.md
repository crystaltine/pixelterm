# Pixelterm
## Render images, shapes, and videos in the terminal

Pixelterm allows you to draw on modern terminal windows using "pixels" instead of just characters.

The "pixels" Pixelterm uses are exactly 1 character wide and 1/2 of a character tall.

### Features
- Draw lines, boxes, custom fonts*, images, and gradients on "frames" (representations of pixels)
- Optimized rendering between frames (in case of animations/videos)
- Flexible coloring/styling utility for printing text with any foreground/background color and style (bold, italic, underline, etc.)

*All custom fonts must be monospaced, and only one is provided by default. For details on how to create your own, see `pixelterm/font.py`. Note that these fonts will be relatively large because of the low number of pixels that can fit on a terminal screen.

### Installation
```
pip install pixelterm
```

Dependencies: numpy, scikit-image, pillow

### Examples
- Bad Apple!! (`examples/bad_apple`)
- Bad Apple!! w/ transparent DVD screensavers bouncing around (`examples/terrible_apple`)