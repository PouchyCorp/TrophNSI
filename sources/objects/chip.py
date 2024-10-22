from coord import Coord

class Chip:
    def __init__(self, name, price, movement, color, position):
        self.name : str = name
        self.price = price
        self.movement : dict = movement
        self.color : list = color
        self.position : Coord = position
        self.heading : str = "right"
    
    def forward(self,val):
        for k in range(val):
          if self.heading == "right":
              self.position.x += 1
          elif self.heading == "left":
              self.position.x -= 1        
          elif self.heading == "up":
              self.position.y += 1
          elif self.heading == "down":
              self.position.y -= 1               

    def turn_l(self,val):
        for k in range(360/val):
          if self.heading == "right":
              self.heading == "up"
          elif self.heading == "left":
              self.heading == "down"       
          elif self.heading == "up":
              self.heading == "left"
          elif self.heading == "down":
              self.heading == "right"

    
    def paint(self):
        for act, val in self.movement.items():
            if act == "forward":
                self.forward(val)
            elif act == "turn left":
                self.turn_l(val)
            elif act == "turn right":
                self.turn_r(val)
    
    
