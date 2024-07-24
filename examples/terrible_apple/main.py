import traceback
from time import time_ns
from pixelterm import PixeltermFrame, Font, hide_terminal_cursor, show_terminal_cursor
from bouncy_square import BouncySquare
from bouncy_text import BouncyText
from helpers.vid_to_np import get_bad_apple
from helpers.audio import AudioHandler

audio_handler = AudioHandler("./examples/bad_apple/assets/badapple72p.mp3")
FPS = 30

bouncy_square_1 = BouncySquare(34, 31, 10, 40, "bottomright")
bouncy_square_2 = BouncySquare(30, 10, 60, 4, "bottomleft")
bouncy_square_3 = BouncySquare(5, 20, 50, 50, "topleft")

DVD_TEXT = "[>DVD<]"
bouncy_text_background = BouncySquare(Font.font1.get_width_of(len(DVD_TEXT)), Font.font1.get_height(), 10, 10, "bottomleft")
bouncy_text_1 = BouncyText(DVD_TEXT, 10, 10, "bottomleft")

def main():
    
    bad_apple = get_bad_apple(FPS)
    
    audio_handler.begin_playing_song()
    start_time = time_ns()

    # always store the previous frame to optimize rendering
    previous_frame: PixeltermFrame = None
    
    last_frame_that_updated_gradient = -1
    last_frame_that_updated_screensavers = -1

    current_red_amount = 255
    change_red_by = -5
    last_rendered_frame_number = -1
    while True:        
        # calculate frame number based on time since start
        frame_number = int((time_ns() - start_time) / (1e9 / FPS))

        # skip all this if the frame is the exact same
        if frame_number == last_rendered_frame_number: continue
        
        # if the frame number is greater than the number of frames, break (video ended)
        if frame_number >= len(bad_apple):
            break
        
        # create a new frame
        new_frame = PixeltermFrame()

        # shenanigans below
        # change the gradient in the background slightly every 3 frames
        if frame_number - last_frame_that_updated_gradient >= 3:
            if current_red_amount == 0: change_red_by = 5
            elif current_red_amount == 255: change_red_by = -5
            
            current_red_amount += change_red_by
            last_frame_that_updated_gradient = frame_number

        # Add gradient to the frame
        new_frame.fill_with_gradient(
            (current_red_amount, 0, 0), 
            (current_red_amount//3, 0, 150)
        )

        # Update bouncy squares every 2 frames
        if frame_number - last_frame_that_updated_screensavers >= 2:
            bouncy_square_1.update()
            bouncy_square_2.update()
            bouncy_square_3.update()
            bouncy_text_background.update()
            bouncy_text_1.update()

            last_frame_that_updated_screensavers = frame_number

        # paste the actual video frame onto the Pixelterm frame
        new_frame.add_image_from_pixels(bad_apple[frame_number], 0, 0)

        # Draw the current squares - see ./bouncy_square.py
        bouncy_square_1.draw_on_frame(new_frame)
        bouncy_square_2.draw_on_frame(new_frame)
        bouncy_square_3.draw_on_frame(new_frame)
        bouncy_text_background.draw_on_frame(new_frame)
        bouncy_text_1.draw_on_frame(new_frame)

        # render the new frame, using the previous frame to optimize rendering
        new_frame.render(previous_frame)
        
        # save the new frame so we can use it to optimize rendering of the next one
        previous_frame = new_frame
        last_rendered_frame_number = frame_number

if __name__ == "__main__":
    try:
        # hide cursor to prevent it flickering while rendering frames
        hide_terminal_cursor()
        print("\x1b[0m", end="") # this just resets color codes while telemetry info is printed
        

        main()


        print("\n\x1b[0mThanks for watching! Rendered using PixelTerm", end="")
    
    except Exception as e:
        print(f"\x1b[31m\nMain Thread exception: {traceback.format_exc()}\x1b[0m\n")
        audio_handler.stop_playing_song()
    except KeyboardInterrupt:
        audio_handler.stop_playing_song()
        print(f"\x1b[0m\nUser quit.\n")
    
    show_terminal_cursor()
        