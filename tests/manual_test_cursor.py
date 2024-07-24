import sys
import time

from pixelterm import hide_terminal_cursor, show_terminal_cursor, cleanup_after_termination

def test_hide_and_show_cursor():
	hide_terminal_cursor()
	print("Cursor hidden. Waiting for 3 seconds...")
	sys.stdout.flush()
	time.sleep(3)
	
	show_terminal_cursor()
	print("Cursor shown. Waiting for 3 seconds to show that nice blinking square...")
	sys.stdout.flush()
	time.sleep(3)

def test_cleanup():
	print(f"\x1b[33mYellow text!!")
	print("no color code in this string, but still yellow because color wasnt reset")
	cleanup_after_termination()
	print("Cleanup set. Waiting for 3 seconds... check if colors are normal after this")
	time.sleep(3)

test_cleanup()
