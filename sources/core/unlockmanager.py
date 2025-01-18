from ui.confirmationpopup import ConfirmationPopup


class UnlockManager:
   def __init__(self):
      """class to manage all game unlocks, it needs to be fully picklable"""
      self.unlocked_floors = ["0", "1"]
      self.unlocked_features = []
      self.floor_price = {"2" : 10, "3" : 100, "4" : 1000, "5" : 10000}

   def is_floor_unlocked(self, num : int):
      if str(num) in self.unlocked_floors:
         return True
      return False
   
   def is_feature_unlocked(self, feature_name):
      if feature_name in self.unlocked_features:
         return True
      return False
   
   def try_to_unlock_floor(self, num : int, game):
      game.confirmation_popups.append(ConfirmationPopup(game.win, f"Débloquer pour {self.floor_price[str(num)]}¥ ?", self.unlock_floor, yes_func_args=[num, game]) )   
   
   def unlock_floor(self, num : int, game):
      """unlocks the floor if possible and return left money"""
      assert str(num) in self.floor_price, "this should not happend"
      if not self.is_floor_unlocked(num) and game.money-self.floor_price[str(num)] >= 0:
         game.money-= self.floor_price[str(num)]
         self.unlocked_floors.append(str(num))