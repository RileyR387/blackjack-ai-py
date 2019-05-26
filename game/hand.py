
from . import Card

class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        BUSTED = ""
        if self.value() > 21:
            BUSTED = "BUSTED"
        return "%-32s %4s %s" % (
                    ' '.join(self.cards),
                    '('+str(self.value())+')',
                    BUSTED
                )

    def __int__(self):
        return self.value()

    def addCard(self, card):
        self.cards.append( card )

    def hasBusted(self):
        if self.value() > 21:
            return True
        else:
            return False

    def dealerHand(self):
        return "%-32s %4s " % (
                    self.cards[0] + " XXX",
                    '(??)'
                )



    def value(self):
        x = 0
        aceCount = 0
        for card in self.cards:
            cVal = Card.value( card );
            if cVal == 11:
                cVal = 0
                aceCount += 1

            x += cVal

        while( aceCount > 0 ):
            if x == 10 and aceCount == 1:
                x += 11
                aceCount -= 1
            elif x > 10-aceCount:
                x += 1
                aceCount -= 1
            else:
                x += 11
                aceCount -= 1

        return x

