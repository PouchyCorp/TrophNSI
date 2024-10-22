from coord import Coord

class Chip:
    def __init__(self, name, price, movement, color, position):
        self.name : str = name
        self.price = price
        self.movement : dict = movement
        self.color : list = color
        self.position : Coord = position
        self.heading : str = "right"

    def forward(tour):
        for k in range(tour):
          if self.heading == "right":
              self.position.x += 1
          if self.heading == "left":
              self.position.x -= 1        
          if self.heading == "up":
              self.position.y += 1
          if self.heading == "left":
              self.position.y -= 1               
        
    def paint(self):
        for action, value in self.movement.items():
            if action == "forward":
                self.forward(value)
            elif action == "turn left":
                self.turn_l(value)
            elif action == "turn right":
                self.turn_r(value)
    
    
