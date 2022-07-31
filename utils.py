import time
import arcade

from yaml import safe_dump, safe_load
from os import path


GRAVITY = 10
MAIN_SONG = ":resources:music/1918.mp3"
APPLE_SOUND = ":resources:sounds/phaseJump1.ogg"
GAME_OVER_SOUND = ":resources:sounds/gameover2.wav"

class Timer:
    """Class used to manage a timer"""
    
    def __init__(self):
        self.timers = {}

    def start_timer(self, obj_id, duration_in_seconds):
        cur_time = time.time()
        self.timers[obj_id] = {"START": cur_time, "END": cur_time + duration_in_seconds}


    def timer_finished(self, obj_id):
        if not self.timer_exists(obj_id): return True
        self.timers[obj_id]['CURRENT'] = time.time()
        if (self.timers[obj_id]["END"] - self.timers[obj_id]["CURRENT"]) <= 0:
            return True

        return False 

    def timer_exists(self, obj_id):
        return obj_id in self.timers

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