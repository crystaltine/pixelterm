import sys
sys.path.append('../charred')

from charred import CharredFrame, term_width
from time import sleep

def test_line_fully_contained():
	frame = CharredFrame()
	frame.fill((0, 0, 0))
	
	frame.add_line((5, 5), (10, 30), (255, 255, 255))
	frame.render_raw()
	sleep(3)

def test_line_both_endpoints_oob():
	frame = CharredFrame()
	frame.fill((0, 0, 0))
	
	frame.add_line((-5, -20), (100, 300), (255, 0, 255))
	frame.render_raw()
	sleep(3)

def test_line_one_endpoint_oob():
	frame = CharredFrame()
	frame.fill((0, 0, 0))
	
	frame.add_line((5, 10), (100, 300), (255, 0, 255))
	frame.render_raw()
	sleep(3)

def test_thick_line():
	frame = CharredFrame()
	frame.fill((0, 0, 0))
	
	frame.add_line((5, 5), (100, 40), (255, 255, 255), 3)
	frame.render_raw()
	sleep(3)

def test_thick_line_oob():
	frame = CharredFrame()
	frame.fill((0, 0, 0))
	
	frame.add_line((-5, -50), (100, 40), (255, 255, 255), 3)
	frame.render_raw()
	sleep(3)

test_thick_line_oob()

