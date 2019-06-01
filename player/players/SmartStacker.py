
import json
from game.color import color
from game.score import score

from pprint import pprint

class Agent:
    def __init__(self):
        self.disableAutoPlay = False
        self.name = "Stacker"
        self.splitEnabled = True
        self.defaultBet = 10
        self.lastBet = self.defaultBet
        self.stackFactor = 1.5

    def placeBet(self, gameStateJson):
        #print( gameStateJson )
        if gameStateJson is None or gameStateJson == '':
            return self.lastBet
        gameState = json.loads(gameStateJson)
        dealer = gameState[-1]['dealer']
        myHands = self._myHands(gameState)

        lossFound = False
        for mySeat in myHands:
            if mySeat['score'] not in [score.blackjack, score.win]:
                lossFound = True

        if not lossFound and self.lastBet <= 40:
            self.lastBet = self.lastBet*self.stackFactor
            print( "Stacked bet! (%s)" % self.lastBet)
        else:
            self.lastBet = self.defaultBet

        return self.lastBet

    def _myHands(self, gameState):
        hands = []
        for seat in gameState:
            for player,res in seat.items():
                if player == 'player.players.SmartStacker':
                    hands.append( res )
        return hands

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
            print("%s: action: DOUBLE" % self.name)
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

