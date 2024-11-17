#test file
from time import time

class _Timer_manager:
    def __init__(self):
        self.timers : list[dict] = []
    
    def create_timer(self,duration : int, func, obj : object | None = None ,repeat : bool = False):
         """duration in miliseconds"""
         self.timers.append({"creation_time" : time(), "duration" : duration, "func" : func, "obj" : obj , "repeat" : repeat})

    def update(self):
        """DO NOT USE OTHER THAN IN THE MAIN LOOP"""
        current_time = time()
        new_list = self.timers.copy()
        for timer in self.timers:
            #check if timer over its duration
            if current_time - timer["creation_time"] >= timer["duration"]:
                if timer['obj']:
                    timer['obj'].timer['func']
                else:
                    timer["func"]
                
                if not timer['repeat']:
                    new_list.remove(timer)
                else:
                    timer['creation_time'] = current_time

        self.timers = new_list
             

TIMER = _Timer_manager()