import time


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

class SoundManager:
    """Class created to manage sounds.
    
    Attrs:
        None
        
    Methods:
        create_sound(filename:str, loop:bool)"""

    def __init__(self) -> None:
        pass
