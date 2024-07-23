from typing import Tuple, Literal

RGBTuple = Tuple[int, int, int]
RGBATuple = Tuple[int, int, int, int]
Anchor = Literal[
	"top-left", 
	"top-right", 
	"bottom-left", 
	"bottom-right", 
	"center",
	"top",
	"bottom",
	"left",
	"right"
]