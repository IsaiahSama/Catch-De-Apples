import time
import arcade, arcade.sound

from yaml import safe_dump, safe_load
from os import path
from threading import Thread


GRAVITY = 10
MAIN_SONG = ":resources:music/1918.mp3"
APPLE_SOUND = ":resources:sounds/phaseJump1.ogg"
GAME_OVER_SOUND = ":resources:sounds/gameover2.wav"

class Timer:
    """Class used to manage a timer"""
    
    def __init__(self):
        self.timers = {}

    def start_timer(self, obj_id:int, duration_in_seconds:float):
        """Used to start a timer.
        
        Args:
            obj_id (int): The id to use for tracking the object
            duration_in_seconds (float): How long the timer should last before ending"""

        cur_time = time.time()
        self.timers[obj_id] = {"START": cur_time, "END": cur_time + duration_in_seconds}


    def timer_finished(self, obj_id:int) -> bool:
        """Used to check if a timer is finished. If the timer is finished or does not exist, return True. Otherwise False.
        
        Args:
            obj_id (int): The id of the object to check.
            
        Returns:
            bool"""
        if not self.timer_exists(obj_id:int): return True
        self.timers[obj_id]['CURRENT'] = time.time()
        if (self.timers[obj_id]["END"] - self.timers[obj_id]["CURRENT"]) <= 0:
            return True

        return False 

    def timer_exists(self, obj_id:int) -> bool:
        """Used to check if a timer with a given id exists
        
        Args:
            obj_id (int): The id to check for
            
        Returns:
            bool"""
        return obj_id in self.timers

songs_playing = {}

def manage_songs():
    while True:
        for song, d in songs_playing.items():
            if song.is_complete(d["PLAYER"]): del songs_playing[song]
        time.sleep(0.2)

manage_song = Thread(target=manage_songs, daemon=True)
manage_song.start()

class SoundManager:
    """Used to manage all songs currently being played
    
    Attrs:
        None
    
    Methods:
        is_playing(song_name:str): Whether the song with the given name is playing or not.
        start_playing(song_path:str, stream:bool, volume:float, loop:bool): Used to start playing a song
        stop_playing(song_path:str): Used to stop playing a song """

    @staticmethod
    def is_playing(song_name:str) -> bool:
        """Used to check whether a given song name is currently being played
        
        Args:
            song_name (str): The name of the song to check for
        """
        
        for k, d in songs_playing.items():
            if song_name == d["NAME"]:
                return [k, d]
        return None

    @staticmethod
    def start_playing(song_path:str, stream:bool=False, volume:float=1.0, loop:bool=False) -> None:
        """Used to start playing a song.
        
        Args:
            song_path (str): The path to the song
            stream (bool): Whether to stream the song or load it into memory
            volume (float): The volume for the song
            loop (bool): Whether to loop the song or not"""

        sound = arcade.sound.load_sound(song_path, stream)
        player = arcade.sound.play_sound(sound, volume, looping=loop)
        songs_playing[sound] = {"PLAYER": player, "NAME": song_path}
        
    @staticmethod
    def stop_playing(song_path:str) -> None:
        """Used to stop a current song from playing
        
        Args:
            song_path (str): The path to the song you want to check"""
        
        songs = SoundManager.is_playing(song_path)
        if songs:
            song, d = songs
            del songs_playing[song]
            song.stop(d["PLAYER"])


class ViewManager:
    """Class used to switch from one view to another easily."""

    @staticmethod
    def load_view(view:arcade.View, **kwargs):
        window = arcade.get_window()

        new_view = view(**kwargs)
        if hasattr(new_view, "setup"):
            new_view.setup()

        window.show_view(new_view)
        

default_state = {
    "LEVEL": 1,
    "POINTS": 0
}

class SaveStateManager:
    """Class used to manage save states and their information.
    
    Attrs:
        None        
    Methods: 
        save_state(): Used to save the state of the game.
        load_state(): Used to load the state of the game"""

    @staticmethod
    def save_state(game_state:dict):
        """Used to save the current state of the game"""
        with open("savefile.yaml", "w") as fp:
            safe_dump(game_state, fp, indent=4)

    @staticmethod
    def update_state(game_state:dict,**kwargs):
        """Used to update a given game state with provided kwargs."""
        for k, v in kwargs.items():
            game_state[k.upper()] = v

        return game_state

    @staticmethod
    def load_state():
        """Used to load the current state of the game"""

        def is_state_valid(game_state):
            for key in default_state.keys():
                if key not in game_state.keys(): return False

            return True

        try:
            with open("savefile.yaml") as fp:
                temp_state = safe_load(fp)
        except Exception as err:
            print(err)
            return default_state

        return temp_state if is_state_valid(temp_state) else default_state

level_info = {
    1: {
        "GOAL": 200
    },
    2: {
        "GOAL": 350
    }
}