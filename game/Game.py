
from . import DealersShoe, GameState

class Game:
    def __init__(self, opts, seats ):
        print( "Game initializing" )
        self.opts = opts
        self.seats = seats
        self.gameState = GameState.GameState( opts['decks'], len(seats) )
        self.shoe = DealersShoe.DealersShoe(opts['decks'])
        self.house = {
            'bankroll': 10^6,
            'minbet': 5,
        }
        print( "Game initialized" )

    def play(self):
        print( "Game running" )
        self.shoe.dumpShoe()
        for seat in self.seats.keys():
            self.seats[seat].init( self.gameState )
        try:
            #while () is not None:
            while True:
                card = self.shoe.nextCard()
                self.gameState.consumeCard( card )
                for seat in self.seats.keys():
                    self.seats[seat].nextAction( self.gameState )
        except Exception as e:
            print( "Shoe Empty! %s" % str(e) );


