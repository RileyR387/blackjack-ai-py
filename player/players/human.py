
import json
from game.color import color

class Agent:
    def __init__(self):
        self.disableAutoPlay = False
        self.name = "PartHuman"

    def nextAction(self, gameStateJson, myHand):
        gameState = json.loads(gameStateJson)

        if myHand.canSplit() or self.disableAutoPlay:
            self.disableAutoPlay = True
            #print( gameStateJson )
            key = input(("(S)Stand|(H)Hit|(D)Double|(P)Split: (default (S)): \n " + color.GREEN + " %s " + color.END + " :") % myHand)
            if key in ['A','a','auto']:
                self.disableAutoPlay = False
                return self.nextAction( gameStateJson, myHand )
            if key in ['S','s','stand']:
                return 'STAND'
            elif key in ['H','h','hit']:
                return 'HIT'
            elif key in ['D','d','double','dub']:
                return 'DOUBLE'
            elif key in ['P','p','split','2','Y','y']:
                if myHand.canSplit():
                    return 'SPLIT'
                else:
                    return 'STAND'
            else:
                return 'STAND'
        else:
            if( myHand.value() >=17
             or (myHand.value() > 11 and not myHand.isSoft() and gameState[-1]['dealer']['handVal'] < 7)
             or len(myHand.cards) > 4
            ):
                return 'STAND'
            else:
                return 'HIT'

    def init(self, gameState):
        print("Hello! I'm part human!")
        pass

