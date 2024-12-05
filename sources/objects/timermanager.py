#test file
from time import time

class TimerManager:
    def __init__(self):
        self.timers : list[dict] = []
    
    def create_timer(self,duration : float, func, repeat : bool = False, arguments : tuple = ()):
        """duration in seconds (accepts float)"""
        self.timers.append({"creation_time" : time(), "duration" : duration, "func" : func, "repeat" : repeat, "args" : arguments})

    def update(self):
        """DO NOT USE OTHER THAN IN THE MAIN LOOP"""
        current_time = time()
        timers_to_suppr = []
        for timer in self.timers:
            #check if timer over its duration
            if current_time - timer["creation_time"] >= timer["duration"]:
                if not timer['repeat']:
                    timers_to_suppr.append(timer)
                else:
                    timer['creation_time'] = current_time

                timer["func"](*timer["args"])

        for timer in timers_to_suppr:
            self.timers.remove(timer)
        
        

TIMER = TimerManager()