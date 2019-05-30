
from .hand import Hand

class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.name = 'dealer'
        pass

    def nextAction(self, state, myHand):
        #print( state )
        pass

    def name(self):
        return "TheDealer"
