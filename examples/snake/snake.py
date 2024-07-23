from random import randint
from collections import deque
from typing import Tuple, Literal
from pixelterm import PixeltermFrame
from blessed.keyboard import Keystroke

class Snake:
	""" Pixelterm snake game backend class to handle game logic. """

	DIRS = {
		"up": (0, -1),
		"down": (0, 1),
		"left": (-1, 0),
		"right": (1, 0)
	}

	COLOR1 = (255, 255, 255)
	COLOR2 = (60, 140, 40)

	def __init__(self, board_x: int, board_y: int):
		self.board_x = board_x
		self.board_y = board_y
		self.snake_body = deque(maxlen=board_x*board_y)
		""" Snake head @ left, tail @ right. """

		self.snake_head = (board_x // 2, board_y // 2)
		self.snake_len = 3
		
		# initialize snake with length 
		for i in range(self.snake_len):
			self.snake_body.append((self.snake_head[0] - i, self.snake_head[1]))

		self.direction = Snake.DIRS["right"]
		self.food_location = self.get_food_location()

		self.dead = False
		self.won = False

	def tick(self) -> Literal["dead", "won", None]:
		""" Run one tick of the game, moving the snake forward. 
		Returns 'dead' if snake crashed, 'won' if snake fills whole board, None if game continues. """
		if self.dead or self.won:
			return

		new_head = (self.snake_head[0] + self.direction[0], self.snake_head[1] + self.direction[1])

		# crashed into self
		if new_head in self.snake_body:
			self.dead = True
			return "dead"

		# oob
		if not ((0 <= new_head[0] <= self.board_x) and (0 <= new_head[1] <= self.board_y)):
			self.dead = True
			return "dead"

		if new_head == self.food_location:
			self.snake_len += 1
			self.snake_body.appendleft(self.snake_head)
			self.snake_head = new_head
			self.food_location = self.get_food_location()
		else:
			self.snake_body.appendleft(self.snake_head)
			self.snake_head = new_head
			self.snake_body.pop()

		if len(self.snake_body) == self.board_x * self.board_y:
			self.won = True
			return "won"
		
		return None

	def get_food_location(self) -> Tuple[int, int]:
		""" Spawn a food at a random location. TODO - make sure it doesn't spawn on the snake. """
		return randint(0, self.board_x-1), randint(0, self.board_y-1)

	def draw_on_frame(self, frame: PixeltermFrame) -> None:
		""" Draw the snake and food on the frame. """

		# Draw the food as a single pixel on the frame.
		# This uses the indexing feature of Pixelterm frames to set the color of a pixel
		# at a specific [y, x] < NOTICE HOW ITS NOT (x, y).
		frame[self.food_location[1], self.food_location[0]] = (255, 50, 10)

		# Draw each pixel of the snake body on the frame.

		num_snake_pixels_drawn = 0
		for x, y in self.snake_body:

			# Alternate snake colors every 2 pixels
			frame[y, x] = (
				Snake.COLOR1 if num_snake_pixels_drawn//2 % 2 == 0 else Snake.COLOR2
			)
			num_snake_pixels_drawn += 1

	def handle_keypress(self, keystroke: Keystroke):
		match keystroke.name:
			case "KEY_UP":
				if self.direction != Snake.DIRS["down"]:
					self.direction = Snake.DIRS["up"]
			case "KEY_DOWN":
				if self.direction != Snake.DIRS["up"]:
					self.direction = Snake.DIRS["down"]
			case "KEY_LEFT":
				if self.direction != Snake.DIRS["right"]:
					self.direction = Snake.DIRS["left"]
			case "KEY_RIGHT":
				if self.direction != Snake.DIRS["left"]:
					self.direction = Snake.DIRS["right"]
