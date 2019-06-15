
import json
from game.color import color
from game.score import score

import game.card as Card

from pprint import pprint

class Agent:
    def __init__(self, opts):
        self.name = "Player2"
        self.newShoeFlag = False

        self.splitEnabled = True
        self.doubleEnabled = True

        self.defaultBet = 10
        self.lastBet = self.defaultBet

        self.cardsCounted = 0
        self.currCards = 0
        self.currHandCount = 0
        self.lastHandCount = 0
        self.shoeCount = 0

    def notifyNewShoe(self):
        self.newShoeFlag = True

    def placeBet(self, gameStateJson):
        if gameStateJson is None or gameStateJson == '':
            return self.lastBet

        gameState = json.loads(gameStateJson)
        dealer = gameState[-1]['dealer']
        myHands = self._myHands(gameState)

        if not self.newShoeFlag:
            self._countRound(gameState)
            self.lastHandCount = self.currHandCount
            self.shoeCount += self.currHandCount
            self.currHandCount = 0
        else:
            print("%s - Reset count for new shoe!" % self.name)
            self.newShoeFlag = False
            self.currHandCount = 0
            self.lastHandCount = 0
            self.shoeCount = 0
            self.lastBet = self.defaultBet

        print("%s - Bet(%s) - Shoe Count: %s" % (self.name, self.lastBet, self._getCount()))
        return self.lastBet

    def nextAction(self, gameStateJson, myHand):
        gameState = json.loads(gameStateJson)
        dealer = gameState[-1]['dealer']
        self._countRound(gameState)
        print("%s - NextAction - Shoe Count: %s" % (self.name, self._getCount()))
        pass

    def init(self, gameState):
        print("Hello! I'm %s!" % self.name)
        pass

    def _countRound(self, gameState):
        self.currHandCount = 0
        for seat in gameState:
            for player, hand in seat.items():
                for card in hand['hand']:
                    if Card.value(card) in [10,11]:
                        self.currHandCount -= 1
                    elif Card.value(card) not in [7,8,9]:
                        self.currHandCount += 1

    def _getCount(self):
        return self.shoeCount + self.currHandCount

    def _myHands(self, gameState):
        hands = []
        for seat in gameState:
            for player,res in seat.items():
                if player == 'player.players.player2':
                    hands.append( res )
        return hands

