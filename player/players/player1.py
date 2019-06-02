
class Agent:
    def __init__(self):
        self.name = "playerOne"

    def placeBet(self, gameStateJson):
        return 5

    def nextAction(self, gameStateJson, myHand):
        pass

    def notifyNewShoe(self):
        pass

    def init(self, gameState):
        print("Hey! I'm %s!" % self.name)
        pass

