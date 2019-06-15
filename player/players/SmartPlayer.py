
import json
from game.color import color

class Agent:
    def __init__(self, opts):
        self.disableAutoPlay = False
        self.name = "Smarty"
        self.splitEnabled = True

    def notifyNewShoe(self):
        pass

    def placeBet(self, gameStateJson):
        return 5

    def nextAction(self, gameStateJson, myHand):
        gameState = json.loads(gameStateJson)
        dealer = gameState[-1]['dealer']

        if( self.splitEnabled and
            myHand.canSplit() and
            (
                myHand.value() < 18
             or
                (myHand.value() in range(18,21) and (dealer['handVal'] in range(2,7) or dealer['handVal'] == 11) )
            )
        ):
            print("%s: action: SPLIT" % self.name)
            return 'SPLIT'

        if myHand.value() in [9,10,11] and myHand.canDouble():
            return 'DOUBLE'

        if( myHand.value() >=17
         or (myHand.value() > 11 and not myHand.isSoft() and dealer['handVal'] < 7)
         or len(myHand.cards) > 4
        ):
            return 'STAND'
        else:
            return 'HIT'

    def init(self, gameState):
        print("Hello! I'm smartish!")
        pass

