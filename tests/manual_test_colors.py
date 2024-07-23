import sys
sys.path.append('../pixelterm')

from pixelterm import fcode, text_style

def test_text_styles():
	""" Outputs a lot of test strings to terminal, verify colors/styles manually """
	print(f">>> fcode() tests:")
	print(f"{fcode(fg=(255, 100, 100), bg=(0, 0, 255))}Should be light red text on pure blue background")
	print(f"{fcode(fg=(0, 0, 0), bg=(200, 200, 200))}Should be black text on light gray background")
	print(f"{fcode(fg=(0, 0, 0), bg=(0, 0, 0))}How are you reading this??\x1b[0m <- should be fully black (black text on black bg)")
	print(f"{fcode(fg=(255, 255, 255), bg=(255, 255, 255))}How are you reading this??\x1b[0m <- should be fully white (white text on black bg)")
	print(f"{fcode(fg=(255, 0, 255))}Didn't set bg color, should be transparent, since bg was cleared to write the text on the prev line")

	print(f"\x1b[0m\n>>> text_style() tests:")
	print(f"{text_style(foreground="black", background="#ff9900", style="bold italic")}Bold,italic black text on orange background, note bold doesnt work on win terminal")
	print(f"{text_style(foreground="af8", background="0f0", style="underline")}Underlined light green text on bright green background")
	print(f"{text_style(foreground="olive", background=(255, 150, 150), style="underline")}Underlined olive (dark yellow) text on light red background")

	print("\x1b[0m") # reset colors
test_text_styles()