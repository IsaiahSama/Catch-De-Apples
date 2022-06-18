import time


GRAVITY = 10

class Timer:
    """Class used to manage a timer"""
    
    def __init__(self):
        self.timers = {}

    def start_timer(self, obj_id, duration_in_seconds):
        cur_time = time.time()
        self.timers[obj_id] = {"START": cur_time, "END": cur_time + duration_in_seconds}


    def timer_finished(self, obj_id):
        if obj_id not in self.timers: return None
        self.timers[obj_id]['CURRENT'] = time.time()
        if (self.timers[obj_id]["END"] - self.timers[obj_id]["CURRENT"]) <= 0:
            return True

        return False 