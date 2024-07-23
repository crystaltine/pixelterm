import cv2
import numpy as np

## READ #################################################
# If you are looking for the Pixelterm Bad Apple!! example, ignore this file
# this simply converts the video file into pixels to paste onto Pixelterm frames.
#########################################################

def extract_frames(video_path, fps=30, width=None, height=None):
    video = cv2.VideoCapture(video_path)
    original_fps = video.get(cv2.CAP_PROP_FPS)
    if fps > original_fps:
        raise ValueError(f"fps must be less than or equal to the original video's FPS ({original_fps})")
    print(f"Extracting frames... original FPS: {original_fps}, Target FPS: {fps}")

    frame_interval = int(original_fps // fps)

    frames = []
    
    frame_count = 0
    while True:
        ret, frame = video.read()
        
        if not ret:
            print(f"\ndone reading frames")
            break
        
        # if the current frame is at the interval, store it
        if frame_count % frame_interval == 0:
            frame_count += 1
            #if width is not None and height is not None:
            #    frame = cv2.resize(frame, (width, height))
            frames.append(frame)
            print(f"recording frame {frame_count}", end="\r")
        else:
            frame_count += 1
            print(f"skipping frame {frame_count}", end="\r")
            continue
    
    video.release()
    
    print("Converting badapple.mp4 to numpy...")
    frames_array = np.array(frames)
    print(f"Done converting badapple.mp4, shape: {frames_array.shape}")
    
    return frames_array

def get_bad_apple() -> np.ndarray:

    video_path = './examples/bad_apple/assets/badapple72p.mp4'
    frames = extract_frames(video_path, fps=30)
    return frames
