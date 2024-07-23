import sys
sys.path.append("../pixelterm")

from pixelterm import PixeltermFrame, Font, term_width, term_height, hide_terminal_cursor, show_terminal_cursor
from snake import Snake
from time import sleep
from threading import Thread
import blessed
import traceback

class SnakeVars:
	TICKRATE = 7
	term = blessed.Terminal()
	stop_game = False
	stop_game_reason: str | None = None
	prev_frame: PixeltermFrame = None
	snake = Snake(term_width(), term_height())

def tick_thread():
	""" Step/tick the snake game. Ticking the game should be almost instant
	as opposed to rendering so the tickrate should be almost exact. """

	try:
		while not SnakeVars.stop_game:
			result = SnakeVars.snake.tick()

			if result is not None: 
				SnakeVars.stop_game = True
				SnakeVars.stop_game_reason = result
				break

			sleep(1 / SnakeVars.TICKRATE)
	except:
		SnakeVars.stop_game = True
		SnakeVars.stop_game_reason = "error"
		print(f"\x1b[31m\nTICK THREAD EXCEPTION: {traceback.format_exc()}\x1b[0m")

def render_thread():
	""" Draws the current state of snake to the screen """

	try:
		while not SnakeVars.stop_game:
			new_frame = PixeltermFrame()

			# fill the map background
			new_frame.add_rect((178, 208, 136), 0, 0, SnakeVars.snake.board_x, SnakeVars.snake.board_y)
			
			# Draw the snake on the frame (see ./snake.py)
			SnakeVars.snake.draw_on_frame(new_frame)

			# Render the frame
			new_frame.render(SnakeVars.prev_frame)
			SnakeVars.prev_frame = new_frame

	except:
		SnakeVars.stop_game = True
		SnakeVars.stop_game_reason = "error"
		print(f"\x1b[31m\nRENDER THREAD EXCEPTION: {traceback.format_exc()}\x1b[0m")

def main():

	# Start the tick and render threads
	Thread(target=tick_thread).start()
	Thread(target=render_thread).start()

	with SnakeVars.term.cbreak():
		while not SnakeVars.stop_game:
			try:
				key = SnakeVars.term.inkey(0.01)

				if key.code == SnakeVars.term.KEY_ESCAPE:
					SnakeVars.stop_game = True
					SnakeVars.stop_game_reason = "quit"
					break
				if key is not None:
					SnakeVars.snake.handle_keypress(key)

			except KeyboardInterrupt: # catch ctrl+c
				SnakeVars.stop_game = True
				SnakeVars.stop_game_reason = "quit"
				break

if __name__ == "__main__":
	try:
		hide_terminal_cursor()
		main()
		show_terminal_cursor()
		SnakeVars.stop_game = True
		
		# Draw a centered background rect behind the text
		SnakeVars.prev_frame.add_rect((0, 0, 0), SnakeVars.prev_frame.width//2, SnakeVars.prev_frame.height//2, Font.font1.get_width_of(len(SnakeVars.stop_game_reason))+2, Font.font1.get_height()+2, anchor="center")
		
		# Draw status text
		SnakeVars.prev_frame.add_large_text(SnakeVars.prev_frame.width//2, SnakeVars.prev_frame.height//2, Font.font1, SnakeVars.stop_game_reason, anchor="center")

		# Render frame to screen
		SnakeVars.prev_frame.render()

		# print(f"\n\x1b[30mExited Snake Game - reason: {SnakeVars.stop_game_reason}\x1b[0m")
	except:
		show_terminal_cursor()
		SnakeVars.stop_game = True
		SnakeVars.stop_game_reason = "error"

		# Drawing status text to screen - same as in the try: block above
		SnakeVars.prev_frame.add_rect((0, 0, 0), SnakeVars.prev_frame.width//2, SnakeVars.prev_frame.height//2, Font.font1.get_width_of(len(SnakeVars.stop_game_reason))+2, Font.font1.get_height()+2, anchor="center")
		SnakeVars.prev_frame.add_large_text(SnakeVars.prev_frame.width//2, SnakeVars.prev_frame.height//2, Font.font1, SnakeVars.stop_game_reason, anchor="center")
		SnakeVars.prev_frame.render()

		print(f"\x1b[31m\nMAIN THREAD EXCEPTION: {traceback.format_exc()}\x1b[0m")