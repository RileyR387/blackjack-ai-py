
from . import GameState

class Game:
    def __init__(self, opts, seats ):
        print( "Game initializing" )
        self.opts = opts
        self.seats = seats
        self.gameState = GameState.GameState(opts['decks'])
        print( "Game initialized" )

    def run(self):
        print( "Game running" )
        self.gameState.dumpShoe()
        for seat in self.seats.keys():
            self.seats[seat].nextAction( self.gameState )

