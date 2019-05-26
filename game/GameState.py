
import random
import pprint

from . import Card
from .hand import Hand
from .Dealer import Dealer

class GameState:
    def __init__(self, deckCount, players):
        self.seats = []
        self.currPlayerIndex = 0;

        for player in players.keys():
            print( "Loaded %s" % player )
            self.seats.append({
                'name': player,
                'hand': Hand(),
                'agent': players[player],
            })

        random.shuffle(self.seats)

        self.seats.append({
            'name': 'dealer',
            'hand': Hand(),
            'agent': Dealer(),
        })
        print("Creating initial game state for %s players" % len(self.seats))

    def consumeCard(self, card):
        player = self.nextPlayer()
        player['hand'].addCard( card )
        print( "Delt player: %s a %s with value %d" % (player['name'], card, Card.value(card)))

    def nextPlayer(self):
        if self.currPlayerIndex+1 >= len(self.seats):
            self.currPlayerIndex = 0
            return self.seats[0]
        else:
            self.currPlayerIndex += 1
            return self.seats[self.currPlayerIndex]

    def printGameTable(self):
        pass

