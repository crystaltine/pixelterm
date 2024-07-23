import sys
sys.path.append('../charred')

from charred import CharredFrame, Font
from time import sleep

def test_frame_fill():

	font1 = Font("./charred/fonts/small1.png")

	frame = CharredFrame()
	frame.fill((255, 255, 0))
	frame.add_large_text(2, 2, font1, "topleft@2,2", anchor='top-left', color=(0, 0, 100))
	frame.render_raw() 
	sleep(3)

test_frame_fill()