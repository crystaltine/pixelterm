from pixelterm import PixeltermFrame, cleanup_after_termination
from time import sleep, perf_counter

cleanup_after_termination()

def test_normal_rect():
	frame = PixeltermFrame()
	frame.fill((255, 255, 0))
	frame.add_rect((0, 0, 0), 5, 5, 10, 10)
	frame.render()
	sleep(3)

def test_normal_rect_centered():
	frame = PixeltermFrame()
	frame.fill((255, 255, 0))
	frame.add_rect((0, 0, 0), 5, 5, 20, 20, anchor="center")
	frame.render()
	sleep(3)

def test_oversize_rect():
	frame = PixeltermFrame()
	frame.fill((255, 255, 0))
	frame.add_rect((0, 0, 255), 5, 5, 200, 200)
	frame.render()
	sleep(3)

def test_perfectly_centered_rect():
	frame = PixeltermFrame()
	frame.fill((255, 255, 0))

	frame.add_rect((255, 0, 255), frame.width//2, frame.height//2, frame.width//2, frame.height//2, anchor="center")
	frame.render()
	sleep(3)

def test_bottomright_rect():
	frame = PixeltermFrame()
	frame.fill((255, 255, 0))

	frame.add_rect((255, 0, 90), frame.width, frame.height, frame.width//2, frame.height//2, anchor="bottom-right")
	frame.render()
	sleep(3)

test_perfectly_centered_rect()