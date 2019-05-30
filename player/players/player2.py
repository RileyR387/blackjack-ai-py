
from game.hand import Hand

class Agent:
    def __init__(self):
        self.name = "PlayerDos"

    def nextAction(self, gameStateJson, myHand):
        if myHand.value() in range(9,12):
            return 'DOUBLE'
        elif( myHand.value()  >= 17 ):
            return 'STAND'
        else:
            return 'HIT'

    def init(self, gameState ):
        print("Hello! I'm player2! I always double...")
        pass

