from unittest import TestCase
from charred import CharredFrame, term_height, term_width, adjust_for_anchor

class AutomatedTests(TestCase):
	def test_frame_size(self):
		frame = CharredFrame()
		
		assert frame.pixels.shape[0] == term_height()
		assert frame.pixels.shape[1] == term_width()

	def test_center_anchor(self):
		x = 5
		y = 5
		size_x = 10
		size_y = 12
		topleft_x, topleft_y = adjust_for_anchor(x, y, size_x, size_y, "center")

		assert topleft_x == 0
		assert topleft_y == -1

	def test_bottom_right_anchor(self):
		x = 5
		y = 5
		size_x = 3
		size_y = 3
		topleft_x, topleft_y = adjust_for_anchor(x, y, size_x, size_y, "bottom-right")

		assert topleft_x == 3
		assert topleft_y == 3