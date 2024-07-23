# Basic Snake game w/ Pixelterm

The classic snake game.
Control the snake with arrow keys/WASD. Eat the food to grow longer. Don't run into the walls or yourself.

The game field will be the size of the terminal on game start, and 
will stay constant regardless of how the terminal is resized.

### Requires:
- blessed (for keyboard input)
- pixelterm (for rendering)

### How to run:
Open any modern terminal app (Fully tested on Windows Terminal). Make sure Python 3.10 or higher is installed.

NOTE: This assumes you are in the root directory of Pixelterm. If you only have the `snake` directory, skip the first line of the following commands.

```
cd examples/snake
pip install requirements.txt
python main.py
```