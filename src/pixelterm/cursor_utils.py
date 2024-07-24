import sys, os
import atexit

if os.name == 'nt':
    from ctypes import c_int, c_byte, Structure, windll, byref

    class CursorStruct(Structure):
        _fields_ = [
			("size", c_int),
			("visible", c_byte)
		]

def hide_terminal_cursor(stream = sys.stdout) -> None:
	""" Hide cursor in terminal. It is recommended to use this before
	rendering anything with pixelterm (otherwise you'll see a blinking ghost
	running around your screen while rendering.)
	
	Credit to [this StackOverflow answer](https://stackoverflow.com/a/10455937/21385219)
	for implementation.
	"""
	if os.name == 'nt':
		ci = CursorStruct()
		handle = windll.kernel32.GetStdHandle(-11)
		windll.kernel32.GetConsoleCursorInfo(handle, byref(ci))
		ci.visible = False
		windll.kernel32.SetConsoleCursorInfo(handle, byref(ci))
	elif os.name == 'posix': # this also works on windows, but keeping above just for compat.
		stream.write("\033[?25l")
		stream.flush()

def show_terminal_cursor(stream = sys.stdout) -> None:
	""" Show cursor in terminal. It is recommended to re-enable
	this after a program running pixelterm terminates (provided that the cursor
	was hidden before)
	
	Credit to [this StackOverflow answer](https://stackoverflow.com/a/10455937/21385219)
	for implementation.
	"""
	if os.name == 'nt':
		ci = CursorStruct()
		handle = windll.kernel32.GetStdHandle(-11)
		windll.kernel32.GetConsoleCursorInfo(handle, byref(ci))
		ci.visible = True
		windll.kernel32.SetConsoleCursorInfo(handle, byref(ci))
	elif os.name == 'posix': # this also works on windows, but keeping above just for compat.
		stream.write("\033[?25h")
		stream.flush()

def cleanup_after_termination(set_to_false: bool = False) -> None:
	""" If setting to true, will run the following code when
	the main program exits successfully:
	```python
	pixelterm.show_terminal_cursor() # makes cursor appear again if it was disabled earlier
	sys.stdout.write("\r\x1b[0m", end="") # gets rid of any leftover color/style codes
	```
	"""
	def on_exit():
		show_terminal_cursor()
		sys.stdout.write("\r\x1b[0m")

	atexit.register(on_exit) if not set_to_false else atexit.unregister(on_exit)
