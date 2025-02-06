r"""
              _            _
             | |          | |
  _   _ _ __ | | ___   ___| | __   _ __ ___   __ _ _ __   __ _  __ _  ___ _ __
 | | | | '_ \| |/ _ \ / __| |/ /  | '_ ` _ \ / _` | '_ \ / _` |/ _` |/ _ \ '__|
 | |_| | | | | | (_) | (__|   <   | | | | | | (_| | | | | (_| | (_| |  __/ |
  \__,_|_| |_|_|\___/ \___|_|\_\  |_| |_| |_|\__,_|_| |_|\__,_|\__, |\___|_|
                                                                __/ |
                                                               |___/

Key Features:
-------------
- Keeps a record of unlocked floors and features.
- Fully serializable using Pickle
- Uses confirmation popups to prompt the user before unlocking.
- Handles the constraints (costs) associated with unlocking floors and features.
- Triggers sound effects and notifications upon unlocking.
"""

from ui.confirmationpopup import ConfirmationPopup
from ui.infopopup import InfoPopup
from utils.sound import SoundManager


class UnlockManager:
    def __init__(self) -> None:
        """class to manage all game unlocks, it needs to be fully picklable"""
        self.unlocked_floors = ["0", "1"]
        self.unlocked_features = []
        self.floor_price = {"2": 10, "3": 100, "4": 1000, "5": 10000}
        self.feature_price = {"other_feature": 500, "Auto Cachier": 5000}

    def is_floor_unlocked(self, num: int):
        if str(num) in self.unlocked_floors:
            return True
        return False

    def is_feature_unlocked(self, feature_name):
        if feature_name in self.unlocked_features:
            return True
        return False

    def try_to_unlock_floor(self, num: int, game):
        game.confirmation_popups.append(ConfirmationPopup(game.win, f"Débloquer pour {self.floor_price[str(num)]}¥ ?", self.unlock_floor, yes_func_args=[num, game]))

    def try_to_unlock_feature(self, name, game):
        game.confirmation_popups.append(ConfirmationPopup(game.win, f"Débloquer pour {self.feature_price[name]}¥ ?", self.unlock_feature, yes_func_args=[name, game]))

    def unlock_floor(self, num: int, game):
        """unlocks the floor if possible and return left money"""
        assert str(num) in self.floor_price, "this should not happend"
        if not self.is_floor_unlocked(num) and game.money-self.floor_price[str(num)] >= 0:
            game.money -= self.floor_price[str(num)]
            self.unlocked_floors.append(str(num))
            game.popups.append(InfoPopup(f"Vous avez débloqué l'étage {num} !"))
            game.sound_manager.achieve.play()
        else:
            game.popups.append(
                InfoPopup("Pas assez d'argent pour débloquer l'étage :("))
            game.sound_manager.incorrect.play()

    def unlock_feature(self, feature_name, game):
        """unlocks the floor if possible and return left money"""
        assert feature_name in self.feature_price, "this should not happend"
        if not self.is_feature_unlocked(feature_name) and game.money-self.feature_price[feature_name] >= 0:
            game.money -= self.feature_price[feature_name]
            self.unlocked_features.append(feature_name)

            match feature_name:
                case "Auto Cachier":
                    game.timer.create_timer(3, game.accept_bot, True)

            game.popups.append(InfoPopup(f"Vous avez débloqué {feature_name} !"))
            game.sound_manager.achieve.play()

        else:
            game.popups.append(
                InfoPopup(f"Pas assez d'argent pour débloquer {feature_name} :("))
            game.sound_manager.incorrect.play()