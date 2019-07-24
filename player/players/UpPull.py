
import json
from game.color import color
from game.score import score

from pprint import pprint

class Agent:
    def __init__(self, opts):
        self.disableAutoPlay = False
        self.name = "UpPull"
        self.splitEnabled = True
        self.defaultBet = 10
        self.lastBet = self.defaultBet
        self.stackFactor = 2
        self.riskLevel = 1
        self.maxRisk = 10

        self.winStreak = 0
        self.lossStreak = 0
        self.minBet = 5
        #self.betProgression = [2,1,2,3,4,3,4,5,4,5,6,5,6,7,6,7,8,7,8,9,8,9,10,9,10,11,12,11,12]
        self.betProgression = [2,1,2,3,4,5,6,7,8,9,10,5,7,10,15,10,15,20,15,20,25,20,25,30,25,30]

    def notifyNewShoe(self):
        pass

    def placeBet(self, gameStateJson):
        if gameStateJson is None or gameStateJson == '':
            return self.minBet*2;

        gameState = json.loads(gameStateJson)
        dealer = gameState[-1]['dealer']
        myHands = self._myHands(gameState)

        lossFound = False
        for mySeat in myHands:
            if mySeat['score'] not in [score.blackjack, score.win]:
                lossFound = True
                if self.winStreak > 5:
                    self.winStreak -4
                else:
                    self.winStreak = 0

                self.lossStreak += 1
            else:
                self.lossStreak = 0
                self.winStreak  += 1

        if self.winStreak > 0 and self.lossStreak < 3:
            if self.winStreak >= len(self.betProgression):
                self.winStreak = len(self.betProgression)-1;
            return  self.betProgression[self.winStreak]*self.minBet

        if self.lossStreak > 0 and self.lossStreak%2 == 0:
            return self.minBet*2
        else:
            return self.minBet

    def _myHands(self, gameState):
        hands = []
        for seat in gameState:
            for player,res in seat.items():
                if player == 'player.players.UpPull':
                    hands.append( res )
        return hands

    def nextAction(self, gameStateJson, myHand):
        gameState = json.loads(gameStateJson)
        dealer = gameState[-1]['dealer']
        if( self.riskLevel < self.maxRisk and self.splitEnabled and
            myHand.canSplit() and
            (
                myHand.value() < 18
             or
                (myHand.value() in [18,20] and (dealer['handVal'] in [2,3,4] or dealer['handVal'] == 11) )
            )
        ):
            print("%s: action: SPLIT" % self.name)
            self.riskLevel *= 2
            return 'SPLIT'

        if self.riskLevel < self.maxRisk and myHand.value() in [10,11] and myHand.canDouble():
            print("%s: action: DOUBLE" % self.name)
            self.riskLevel *= 2
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

