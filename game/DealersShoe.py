
import random
import pprint

from .deck import Deck
from .exception import ShuffleShoeException

class DealersShoe:
    def __init__(self, deckCount):
        print("Creating dealers shoe with %s decks" % deckCount)
        self.shoe = []
        self.decks = deckCount
        self.sentShuffleNotice = False
        for x in range(0, self.decks):
            self.shoe.extend( Deck.cards() )
        self.shuffle()

    def dumpShoe(self):
        pp = pprint.PrettyPrinter(width=64,compact=True)
        pp.pprint( self.shoe )

    def shuffle(self):
        random.shuffle( self.shoe )

    def nextCard(self):
        if len(self.shoe) > (.2*self.decks*52) or self.sentShuffleNotice:
            return self.shoe.pop()
        else:
            self.sentShuffleNotice = True
            raise ShuffleShoeException("It's time to shuffle!")

