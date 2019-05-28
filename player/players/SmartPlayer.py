
import json
from game.color import color

class Agent:
    def __init__(self):
        self.disableAutoPlay = False
        self.name = "Smarty"

    def nextAction(self, gameStateJson, myHand):
        gameState = json.loads(gameStateJson)

        if myHand.value() in [9,10,11] and myHand.canSplit():
            return 'SPLIT'

        if myHand.value() in [9,10,11] and myHand.canDouble():
            return 'DOUBLE'

        if( myHand.value() >=17
         or (myHand.value() > 11 and not myHand.isSoft() and gameState[-1]['dealer']['handVal'] < 7)
         or len(myHand.cards) > 4
        ):
            return 'STAND'
        else:
            return 'HIT'

    def init(self, gameState):
        print("Hello! I'm smartish!")
        pass

