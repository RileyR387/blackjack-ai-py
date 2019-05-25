
import random
from pprint import pprint

class GameState:
    def __init__(self, deckCount):
        print("Creating initial game state with %s decks" % deckCount)

        self.shoe = [];

        for x in range(0,deckCount):
            self.shoe.extend( self.deck() );

        self.shuffle()

    def dumpShoe(self):
        pprint( self.shoe )

    def shuffle(self):
        random.shuffle( self.shoe )

    def deck(self):
        return [
          'A' + u"\u2663", 'A' + u"\u2664", 'A' + u"\u2665", 'A' + u"\u2666",
          '2' + u"\u2663", '2' + u"\u2664", '2' + u"\u2665", '2' + u"\u2666",
          '3' + u"\u2663", '3' + u"\u2664", '3' + u"\u2665", '3' + u"\u2666",
          '4' + u"\u2663", '4' + u"\u2664", '4' + u"\u2665", '4' + u"\u2666",
          '5' + u"\u2663", '5' + u"\u2664", '5' + u"\u2665", '5' + u"\u2666",
          '6' + u"\u2663", '6' + u"\u2664", '6' + u"\u2665", '6' + u"\u2666",
          '7' + u"\u2663", '7' + u"\u2664", '7' + u"\u2665", '7' + u"\u2666",
          '8' + u"\u2663", '8' + u"\u2664", '8' + u"\u2665", '8' + u"\u2666",
          '9' + u"\u2663", '9' + u"\u2664", '9' + u"\u2665", '9' + u"\u2666",
          '10' + u"\u2663", '10' + u"\u2664", '10' + u"\u2665", '10' + u"\u2666",
          'J' + u"\u2663", 'J' + u"\u2664", 'J' + u"\u2665", 'J' + u"\u2666",
          'Q' + u"\u2663", 'Q' + u"\u2664", 'Q' + u"\u2665", 'Q' + u"\u2666",
          'K' + u"\u2663", 'K' + u"\u2664", 'K' + u"\u2665", 'K' + u"\u2666",
        ]

