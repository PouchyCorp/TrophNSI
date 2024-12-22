from objects.timermanager import TimerManager


class BotDistributor:
    def __init__(self):
        self.theorical_gold = 0
        self.robot_tiers = [1, 5, 10, 50, 100, 500, 1000]

    def add_to_theorical_gold(self, fooo):
        gold_amount = fooo.beauty*2
        self.theorical_gold += gold_amount
        print(self.theorical_gold)
    
    def distribute_to_bot(self, TIMER):
        for tier in reversed(self.robot_tiers): #iterate tiers from most expensive to least expensive
            amount_mod : int = self.theorical_gold//tier #determine how much of a tier we can fit into the theorical gold

            if 3 >= amount_mod >= 1: #checks if you can distribute between 3 and 1 of this tier

                for j in range(amount_mod): #distribute the correct bot tier the proper amount
                    TIMER.create_timer(j*0.5, print, False, [f"distr : {tier}"]) 

                    self.theorical_gold -= tier
                return

class foo:
    def __init__(self):
        self.beauty = 50

TIMER = TimerManager()
bot_distributor = BotDistributor()
fooo = foo()
TIMER.create_timer(1, bot_distributor.add_to_theorical_gold, True, [fooo])
TIMER.create_timer(5, bot_distributor.distribute_to_bot, True, [TIMER], repeat_time_interval=[0,6])

while True:
    TIMER.update()


