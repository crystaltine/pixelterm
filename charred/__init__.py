import atexit
from .charred_types import *
from .font import *
from .frame import *
from .render_utils import (
	term_width,
	term_height,
	move_xy,
	fcode,
	blend_rgba_img_onto_rgb_img
)

from cursor import hide, show
hide()

def on_exit():
	show()
	print("\r\x1b[0m", end="")

atexit.register(on_exit)