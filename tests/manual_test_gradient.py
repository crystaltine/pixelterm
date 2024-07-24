from pixelterm.frame import PixeltermFrame
from time import sleep, perf_counter

def test_gradient():
	frame = PixeltermFrame()
	frame.fill_with_gradient((0, 0, 0), (255, 255, 255))
	frame.render_raw()
	sleep(3)

def test_gradient_vertical():
	frame = PixeltermFrame()
	frame.fill_with_gradient((0, 0, 0), (255, 255, 255), direction='vertical')
	frame.render_raw()
	sleep(3)

def test_animated_gradient():

	start = perf_counter()
	frames_rendered = 0

	color1 = (255, 0, 0)
	color2 = (0, 255, 0)

	prev = PixeltermFrame()
	prev.fill_with_gradient(color1, color2)
	prev.render_raw()
	frames_rendered += 1

	while color1[0] != 0:
		color1 = (color1[0]-1, color1[1], color1[2])
		new_frame = PixeltermFrame()
		new_frame.fill_with_gradient(color1, color2)
		new_frame.render(prev)
		prev = new_frame
		frames_rendered += 1

	end = perf_counter()
	print(f"\x1b[0mtest_animation_gradient: rendered {frames_rendered} frames; {end-start}s ({frames_rendered/(end-start)}fps)")

test_gradient_vertical()