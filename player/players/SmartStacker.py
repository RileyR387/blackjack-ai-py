
import json
from game.color import color
from game.score import score

class Agent:
    def __init__(self):
        self.disableAutoPlay = False
        self.name = "Stacker"
        self.splitEnabled = True

    def placeBet(self, gameStateJson):
        #print( gameStateJson )
        gameState = json.loads(gameStateJson)
        dealer = gameState[-1]['dealer']
        return 5

    def nextAction(self, gameStateJson, myHand):
        gameState = json.loads(gameStateJson)
        dealer = gameState[-1]['dealer']

        if( self.splitEnabled and
            myHand.canSplit() and
            (
                myHand.value() < 18
             or
                (myHand.value() in [18,20] and (dealer['handVal'] in [2,3,4,5,6] or dealer['handVal'] == 11) )
            )
        ):
            print("%s: action: SPLIT" % self.name)
            return 'SPLIT'

        if myHand.value() in [10,11] and myHand.canDouble():
            return 'DOUBLE'

        if( myHand.value() >=17
         or (myHand.value() > 11 and not myHand.isSoft() and dealer['handVal'] < 7)
         or len(myHand.cards) > 4
        ):
            return 'STAND'
        else:
            return 'HIT'

    def init(self, gameState):
        print("Hello! I'm %s!" % self.name)
        pass

