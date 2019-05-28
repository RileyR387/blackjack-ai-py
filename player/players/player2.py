
class Agent:
    def __init__(self):
        self.name = "PlayerDos"

    def nextAction(self, gameStateJson, myHand):
        return 'DOUBLE'

    def init(self, gameState ):
        print("Hello! I'm player2!")
        pass

