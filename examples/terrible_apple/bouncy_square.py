import random
from pixelterm import PixeltermFrame

class BouncySquare:
	"""
	Helper class that handles drawing a DVD-screensaver-like square to Pixelterm frames.
	"""

	COLORS = [(126, 0, 217), (56, 255, 100), (56, 67, 255), (200, 100, 0), (160, 160, 20), (200, 200, 230), (90, 20, 14)]
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

	def __init__(self, width: int, height: int, start_x: int, start_y: int, start_direction: str):
		self.curr_color: tuple = random.choice(BouncySquare.COLORS)
		self.width: int = width
		self.height: int = height
		self.x: int = start_x
		self.y: int = start_y
		self.velocity_x, self.velocity_y = BouncySquare.DIRECTIONS[start_direction]

	# If you're looking for examples for Pixelterm, this function is irrelevant.
	# Instead see BouncySquare.draw_on_frame
	def update(self):
		""" Updates position and velocity of the Bouncy Square. """

		# if the screensaver location is at the edge of the screen, reverse the velocity
		if not BouncySquare.MAX_X - self.width >= self.x >= BouncySquare.MIN_X:
			self.velocity_x *= -1
			self.curr_color = random.choice(BouncySquare.COLORS)
		if not BouncySquare.MAX_Y - self.height >= self.y >= BouncySquare.MIN_Y:
			self.velocity_y *= -1
			self.curr_color = random.choice(BouncySquare.COLORS)

		# move based on velocity
		self.x += self.velocity_x
		self.y += self.velocity_y

	def draw_on_frame(self, pixelterm_frame: PixeltermFrame):
		""" Draws the current Bouncy Square to the frame."""
		pixelterm_frame.add_rect(
			color=(*self.curr_color, 100),
			x=self.x, 
			y=self.y, 
			width=self.width, 
			height=self.height,
			outline_width=2,
			outline_color=(0, 0, 0),
		)

