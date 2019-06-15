
import json
import game.card as Card
from game.color import color

class Agent:
    def __init__(self):
        self.disableAutoPlay = True
        self.newShoeFlag = False
        self.name = "PartHuman"
        self.defaultBet = 5
        self.lastBet = self.defaultBet
        self.currHandCount = 0
        self.currCardCount = 0
        self.lastHandCount = 0
        self.shoeCount = 0
        self.cardCount = 0
        self.gameDecks = 6

    def placeBet(self, gameStateJson):
        gameState = None
        if gameStateJson is None or gameStateJson == '':
            pass
        else:
            gameState = json.loads(gameStateJson)

        if not self.newShoeFlag and gameState is not None:
            self._countRound(gameState)
            self.lastHandCount = self.currHandCount
            self.shoeCount += self.currHandCount
            self.cardCount += self.currCardCount
            self.currHandCount = 0
            self.currCardCount = 0
        else:
            print("Reset count for new shoe!")
            self.newShoeFlag = False
            self.currCardCount = 0
            self.currHandCount = 0
            self.lastHandCount = 0
            self.shoeCount = 0
            self.cardCount = 0
            self.lastBet = self.defaultBet

        print("%s - RemDecks:  %s" % (self.name, self._decksRemaining()))
        print("%s - delt: %s/%s cards(%2.2f%%)" % (
            self.name, self._cardCount(), self.gameDecks*52, 100*(self._cardCount()/(self.gameDecks*52)) ) )
        print("%s - CardCount: %s" % (self.name, self._getCount()))
        print("%s - TrueCount: %s" % (self.name, self._trueCount()))
        nextBet = input(("Place bet (%s) : " % self.lastBet))
        try:
            nextBet = int(nextBet)
            if nextBet > 0:
                self.lastBet = nextBet
            else:
                nextBet = self.lastBet
        except Exception as e:
           nextBet = self.lastBet

        return nextBet

    def notifyNewShoe(self):
        self.newShoeFlag = True
        input("press [enter] to Ack end of shoe!")

    def _trueCount(self):
        return int(self._getCount()/self._decksRemaining())

    def _getCount(self):
        return self.shoeCount + self.currHandCount

    def _cardCount(self):
        return self.cardCount + self.currCardCount

    def _decksRemaining(self):
        decksRemaining = int(self.gameDecks-(self._cardCount()/52))
        if decksRemaining < 1:
            return 1
        return decksRemaining

    def _countRound(self, gameState):
        self.currHandCount = 0
        self.currCardCount = 0
        for seat in gameState:
            for player, hand in seat.items():
                for card in hand['hand']:
                    self.currCardCount += 1
                    if Card.value(card) in [10,11]:
                        self.currHandCount -= 1
                    elif Card.value(card) not in [7,8,9]:
                        self.currHandCount += 1

    def nextAction(self, gameStateJson, myHand):
        gameState = json.loads(gameStateJson)
        dealer = gameState[-1]['dealer']
        self._countRound(gameState)

        print("%s - RemDecks:  %s" % (self.name, self._decksRemaining()))
        print("%s - delt: %s/%s cards(%2.2f%%)" % (
            self.name, self._cardCount(), self.gameDecks*52, 100*(self._cardCount()/(self.gameDecks*52)) ) )
        print("%s - CardCount: %s" % (self.name, self._getCount()))
        print("%s - TrueCount: %s" % (self.name, self._trueCount()))
        print("%s - Bet(%s)" % (self.name, self.lastBet))

        if myHand.canSplit() or self.disableAutoPlay:
            self.disableAutoPlay = True
            #print( gameStateJson )
            key = input(("(S)Stand|(H)Hit|(D)Double|(P)Split|(Y)SplitOrHit: (default (S)): \n " + color.GREEN + " %s " + color.END + " :") % myHand)
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
            elif key in ['Y','y']:
                if myHand.canSplit():
                    return 'SPLIT'
                else:
                    return 'HIT'
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

    def _myHands(self, gameState):
        hands = []
        for seat in gameState:
            for player,res in seat.items():
                if player == 'player.players.CountingStacker2':
                    hands.append( res )
        return hands

    def init(self, gameState):
        print("Hello! I'm part human!")
        pass

