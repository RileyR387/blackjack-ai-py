
import random
import pprint

from . import Card

class GameState:
    def __init__(self, deckCount, players):
        self.players = players
        print("Creating initial game state for %s players" % len(self.players))

    def consumeCard(self, card):
      print( "Delt %s with value %d" % (card, Card.value(card)))
      pass


    def printGameTable(self):
       pass

