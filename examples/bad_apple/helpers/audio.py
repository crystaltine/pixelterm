from pygame import mixer
from threading import Thread
import time

mixer.init()

## READ #################################################
# If you are looking for the Pixelterm Bad Apple!! example, ignore this file
# This file just handles the video music.
#########################################################

class AudioHandler:
    """ Class used to play music, recycled from [the vis Geometry Dash project](https://github.com/crystaltine/vis/blob/main/gd/audio.py) """
    
    AUDIO_VOLUME = 0.4

    def __init__(self, song_filepath: str, start_offset: float = 0, loops: int = 0):
        """ To play a song indeifnitely, pass in `loops = -1`."""
        self.song_filepath = song_filepath
        self.start_offset = start_offset
        self.song_playing = False
        self.loops = loops
        self.thread: Thread = None
        """ The thread object the music is playing on. Is None until begin_playing_song is called at least once. """
        
        mixer.music.set_volume(AudioHandler.AUDIO_VOLUME)

    def begin_playing_song(self) -> None:
        """ Begins playing the song from the start offset using this instance's decicated thread. """
        
        self.stop_playing_song()
        
        def play():
            try:
                mixer.music.load(self.song_filepath)
            except FileNotFoundError as e:
                return
            mixer.music.play(start=self.start_offset, loops=self.loops)
            self.song_playing = True
            
            while mixer.music.get_busy() and self.song_playing:
                time.sleep(0.01)
        
        self.thread = Thread(target=play)
        self.thread.start()
        
    def stop_playing_song(self) -> None:
        """ Stops playing the current song. This also ends the thread. """
        mixer.music.stop()
        self.song_playing = False
        
    def pause_playing_song(self) -> None:
        """ Pauses the current song. """
        mixer.music.pause()
        
    def resume_playing_song(self) -> None:
        """ Resumes the current song. """
        mixer.music.unpause()
