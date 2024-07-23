import sys
sys.path.append('../pixelterm')

from pixelterm import move_xy

def test_move_1():
	print(f"{move_xy(5, 5)}_ <- (5, 5)")

def test_move_2():
	print(f"{move_xy(0, 0)}_ <- (0, 0)")
