import sys
sys.path.append("../pixelterm")

import traceback
from time import time_ns
from pixelterm import PixeltermFrame, hide_terminal_cursor, show_terminal_cursor
from helpers.vid_to_np import get_bad_apple
from helpers.audio import AudioHandler

audio_handler = AudioHandler("./examples/bad_apple/assets/badapple72p.mp3")
FPS = 30
temp = []

def main():
    
    bad_apple = get_bad_apple()
    
    audio_handler.begin_playing_song()
    start_time = time_ns()

    # always store the previous frame to optimize rendering
    previous_frame: PixeltermFrame = None
    while True:        
        # calculate frame number based on time since start
        frame_number = int((time_ns() - start_time) / (1e9 / FPS)) 
        
        # if the frame number is greater than the number of frames, break (video ended)
        if frame_number >= len(bad_apple):
            break
        
        # create a new frame
        new_frame = PixeltermFrame()

        # paste video onto it
        new_frame.add_image_from_pixels(bad_apple[frame_number], 0, 0)

        # render the new frame, using the previous frame to optimize rendering
        new_frame.render(previous_frame)
        
        # save the new frame so we can use it to optimize rendering of the next one
        previous_frame = new_frame
    
if __name__ == "__main__":
    try:
        # hide cursor to prevent it flickering while rendering frames
        hide_terminal_cursor()
        print("\x1b[0m", end="") # this just resets color codes while telemetry info is printed
        

        main()


        print("\n\x1b[0mThanks for watching! Rendered using PixelTerm", end="")
    
    except Exception as e:
        audio_handler.stop_playing_song()
        print(f"\x1b[31m\nMain Thread exception: {traceback.format_exc()}\x1b[0m\n")
    except KeyboardInterrupt:
        audio_handler.stop_playing_song()
        print(f"\x1b[0m\nUser quit.\n")
    
    show_terminal_cursor()
        