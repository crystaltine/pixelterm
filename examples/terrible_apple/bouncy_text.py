import random
from pixelterm import PixeltermFrame, Font, RGBATuple, RGBTuple

class BouncyText:
	"""
	Helper class that handles drawing a DVD-screensaver-like text that bounced around to Pixelterm frames.

	Note that this is EXTREMELY similar to ./bouncy_square.py
	"""

	COLORS = [(226, 100, 255), (156, 255, 200), (156, 190, 255), (255, 200, 100), (255, 255, 120), (255, 255, 255), (190, 120, 114)]
	DIRECTIONS = {
		"bottomright": (1, 1),
		"bottomleft": (-1, 1),
		"topleft": (-1, -1),
		"topright": (1, -1),
	}

	# bad apple is 4:3, the example uses 72p
	# but we have to pad by 1px because of the outline
	MIN_X = 1
	MIN_Y = 1
	MAX_X = 95
	MAX_Y = 71

	def __init__(self, text: str, start_x: int, start_y: int, start_direction: str):
		self.text = text
		self.curr_color: tuple = random.choice(BouncyText.COLORS)
		self.width: int = Font.font1.get_width_of(len(text))
		self.height: int = Font.font1.get_height()
		self.x: int = start_x
		self.y: int = start_y
		self.velocity_x, self.velocity_y = BouncyText.DIRECTIONS[start_direction]

	# If you're looking for examples for Pixelterm, this function is irrelevant.
	# Instead see BouncyText.draw_on_frame
	def update(self):
		""" Updates position and velocity of the Bouncy Square. """

		# if the screensaver location is at the edge of the screen, reverse the velocity
		if not BouncyText.MAX_X - self.width >= self.x >= BouncyText.MIN_X:
			self.velocity_x *= -1
			self.curr_color = random.choice(BouncyText.COLORS)
		if not BouncyText.MAX_Y - self.height >= self.y >= BouncyText.MIN_Y:
			self.velocity_y *= -1
			self.curr_color = random.choice(BouncyText.COLORS)

		# move based on velocity
		self.x += self.velocity_x
		self.y += self.velocity_y

	def draw_on_frame(self, pixelterm_frame: PixeltermFrame):
		""" Draws the current Bouncy Square to the frame."""
		pixelterm_frame.add_large_text(
			x=self.x,
			y=self.y,
			font=Font.font1,
			text=self.text,
			anchor="top-left",
			color=self.curr_color,
		)

