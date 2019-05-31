
import json
from game.color import color
from game.score import score

class Agent:
    def __init__(self):
        self.disableAutoPlay = False
        self.name = "Stacker"
        self.splitEnabled = True
        self.lastBet = 5

    def placeBet(self, gameStateJson):
        #print( gameStateJson )
        gameState = json.loads(gameStateJson)
        for seat in gameState:
            for player,res in seat.items():
                print( 'player: %s' % player )
                print( 'res: %s' % res['score'] )
                if player == 'player.players.SmartStacker':
                    if self.lastBet <= 40 and res['score'] in [score.blackjack, score.win]:
                        betFactor = 1.5
                        print( "Stacked bet! (%s)" % (self.lastBet*betFactor))
                        self.lastBet = self.lastBet*betFactor
                        return (self.lastBet*betFactor)
                    else:
                        self.lastBet = 5
                        return 5
                else:
                    pass

        dealer = gameState[-1]['dealer']
        self.lastBet = 5
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

