from coord import Coord

class Chip:
    def __init__(self, name, price, movement, color, position):
        self.name : str = name
        self.price = price
        self.movement : dict = movement
        self.color : list = color
        self.position : Coord = position
        self.heading : int = 0 
    
    def forward(self,val):
        for k in range(val):
          if self.heading == 0:
              self.position.x += 1
          elif self.heading == 180:
              self.position.x -= 1        
          elif self.heading == 270:
              self.position.y += 1
          elif self.heading == 90:
              self.position.y -= 1               

    def turn_l(self,val,dir):
        for k in range(360/val):
            if dir == "left":
                self.heading -= 90
            elif dir == "right":
                self.heading += 90
        if self.heading > 270:
            self.heading -= 360
        self.heading = abs(self.heading)
    
    def paint(self):
        for act, val in self.movement.items():
            if act == "forward":
                self.forward(val)
            elif act == "turn left":
                self.turn(val,"left")
            elif act == "turn right":
                self.turn(val,"right")
    
    
