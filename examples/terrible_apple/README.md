# (worse) Bad Apple!! w/ Pixelterm

The iconic Bad Apple!! video, rendered in the terminal at 72p / 30FPS.
#### HOWEVER:
There's already an example for the original Bad Apple!!, so this one shows a bit more of Pixelterm's functionality by drawing random colored shapes and text all over the original video.

Also, the background is a constantly changing red-blue gradient.

### Requires:
- numpy (for frame utils)
- opencv-python (for converting video file to numpy)
- pygame (for audio)
- pixelterm (for rendering)

### How to run:

Open any modern terminal app (Fully tested on Windows Terminal). Make sure Python 3.10 or higher is installed.

NOTE: This assumes you are in the root directory of Pixelterm. If you only have the `terrible_apple` directory, skip the first line of the following commands.

```
cd examples/terrible_apple
pip install requirements.txt
python main.py
```