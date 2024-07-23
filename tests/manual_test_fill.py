import sys
sys.path.append('../charred')

from charred import CharredFrame, term_height, term_width
from time import sleep, perf_counter

def test_frame_fill():
	frame = CharredFrame()
	frame.fill((255, 255, 0))
	frame.render_raw()
	sleep(3)

def test_animated_fill():
	start = perf_counter()
	frames_rendered = 0

	color1 = (255, 0, 0)

	prev = CharredFrame()
	prev.fill(color1)
	prev.render_raw()
	frames_rendered += 1

	while color1[0] != 0:
		color1 = (color1[0]-1, color1[1], color1[2])
		new_frame = CharredFrame()
		new_frame.fill(color1)
		new_frame.render(prev)
		prev = new_frame
		frames_rendered += 1

	end = perf_counter()
	print(f"\x1b[0mtest_animated_fill: rendered {frames_rendered} frames; {end-start}s ({frames_rendered/(end-start)}fps)")

test_animated_fill()