
import game.card as Card

class Hand:
    def __init__(self):
        self._handIsSoft = False
        self.cards = []
        self.nextHand = None
        self.isFinal = False
        self._bet = 0

    def __str__(self):
        status = ''
        if self.value() > 21:
            status = "BUSTED"

        if self.value() <= 21 and not self.isFinal and len(self.cards) >= 2:
            status = "active"

        return "%-32s %4s %s" % (
                    ' '.join(self.cards),
                    '('+str(self.value())+')',
                    status
                )

    def __int__(self):
        return self.value()

    def addCard(self, card):
        self.cards.append( card )
        if self.value() >= 21:
            self.isFinal = True
        return self.isFinal

    def hasBusted(self):
        if self.value() > 21:
            return True
        else:
            return False

    def isSoft(self):
        return self._handIsSoft

    def isBlackjack(self):
        if self.value() == 21 and len(self.cards) == 2:
            return True
        else:
            return False

    def canSplit(self):
        if len(self.cards) == 2 and Card.value(self.cards[0]) == Card.value(self.cards[1]):
            return True
        else:
            return False
    def canDouble(self):
        if len(self.cards) == 2:
            return True
        else:
            return False

    def splitHand(self):
        nextHand = Hand()
        nextHand.addCard( self.cards.pop() )
        return nextHand

    def offerInsurance(self):
        if Card.value(self.cards[0]) == 11 and len(self.cards) == 2:
            return True
        else:
            return False

    def dealerHand(self):
        return "%-32s %4s " % (
                    self.cards[0] + " XXX",
                    '('+str(Card.value(self.cards[0]))+')'
                )

    def value(self):
        x = 0
        aceCount = 0
        self._handIsSoft = False
        for card in self.cards:
            cVal = Card.value( card );
            if cVal == 11:
                cVal = 0
                aceCount += 1

            x += cVal

        while( aceCount > 0 ):
            if x == 10 and aceCount == 1:
                self._handIsSoft = True
                x += 11
                aceCount -= 1
            elif x > 10-aceCount:
                x += 1
                aceCount -= 1
            else:
                self._handIsSoft = True
                x += 11
                aceCount -= 1

        return x

