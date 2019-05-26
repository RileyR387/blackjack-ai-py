
import random
import pprint

from . import deck

class DealersShoe:
    def __init__(self, deckCount):
        print("Creating dealers shoe with %s decks" % deckCount)
        self.shoe = []
        self.decks = deckCount
        for x in range(0, self.decks):
            self.shoe.extend( deck.cards() )
        self.shuffle()

    def dumpShoe(self):
        pp = pprint.PrettyPrinter(width=64,compact=True)
        pp.pprint( self.shoe )

    def shuffle(self):
        random.shuffle( self.shoe )

    def nextCard(self):
        if len(self.shoe) > (.2*self.decks*52):
            return self.shoe.pop()
        else:
            raise ShuffleShoeException

