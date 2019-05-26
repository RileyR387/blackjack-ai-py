
from . import Card

class Hand:
    def __init__(self):
        self.cards = []

    def addCard(self, card):
        self.cards.append( card )
        self.cards.sort()

    def __str__(self):
        print( ''.join(self.cards))

    def value(self):
        x = 0
        aceCount = 0
        for card in self.cards:
            cVal = Card.value( card );
            if cVal == 11:
                cVal = 0
                ++aceCount

            x += cVal

        while( aceCount > 0 ):
            if x == 10 and aceCount == 1:
                x += 11
                --aceCount
            elif x > 10-aceCount:
                x += 1
                --aceCount
            else:
                x += 11

        return x

