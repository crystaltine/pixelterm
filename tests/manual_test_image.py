import numpy as np

from pixelterm import PixeltermFrame, term_width
from time import sleep

def test_image_from_file_normal():
	frame = PixeltermFrame()
	frame.fill((255, 0, 255))
	
	frame.add_image_from_filepath("tests/assets/image.png", 5, 5)
	frame.render_raw()
	sleep(3)

def test_image_from_file_clipped_topleft():
	frame = PixeltermFrame()
	frame.fill((255, 0, 255))
	
	frame.add_image_from_filepath("tests/assets/image.png", -1, -4)
	frame.render_raw()
	sleep(3)

def test_image_from_file_oob():
	frame = PixeltermFrame()
	frame.fill((255, 0, 255))
	
	frame.add_image_from_filepath("tests/assets/image.png", 0, -100)
	frame.render_raw()
	sleep(3)

def test_image_from_file_clipped_right():
	frame = PixeltermFrame()
	frame.fill((255, 0, 255))
	
	frame.add_image_from_filepath("tests/assets/image.png", term_width()-3, 0)
	frame.render_raw()
	sleep(3)

def test_image_from_pixels():
	frame = PixeltermFrame()
	frame.fill((255, 0, 255))
	
	image = np.array([
		[[255, 255, 0], [255, 0, 0]], 
		[[100, 0, 100], [255, 255, 0]]
	])

	frame.add_image_from_pixels(image, 1, 1)
	frame.render_raw()
	sleep(3)

def test_image_anchored_center():
	frame = PixeltermFrame()
	frame.fill_with_gradient((0, 0, 0), (90, 0, 90))
	
	image = np.array([
		[[0, 0, 255], [0, 0, 255], [0, 0, 255]], 
		[[0, 0, 255], [255, 255, 0], [0, 0, 255]],
		[[0, 0, 255], [0, 0, 255], [0, 0, 255]], 
	])

	frame.add_image_from_pixels(image, 2, 2, "center")
	frame.render_raw()
	sleep(3)

def test_image_anchored_bottomright():
	frame = PixeltermFrame()
	frame.fill((255, 0, 255))
	
	image = np.array([
		[[255, 255, 0], [255, 0, 0]], 
		[[100, 0, 100], [255, 255, 0]]
	])

	frame.add_image_from_pixels(image, 1, 1, "bottom-right")
	frame.render_raw()
	sleep(3)

test_image_anchored_center()