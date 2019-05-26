
from . import DealersShoe, GameState
from .exception import ShuffleShoeException

class Game:
    def __init__(self, opts, players ):
        print( "Game initializing" )
        self.opts = opts
        self.players = players

        self.gameState = GameState.GameState( opts['decks'], players )
        self.shoe  =  DealersShoe.DealersShoe(opts['decks'])

        self.house = {
            'bankroll': 10^6,
            'minbet': 5,
        }
        print( "Game initialized" )

    def play(self):
        print( "Game running" )

        self.shoe.dumpShoe()

        for player in self.players.keys():
            self.players[player].init( self.gameState )

        try:
            while True:

                card = self.shoe.nextCard()

                self.gameState.consumeCard( card )

                for player in self.players.keys():
                    self.players[player].nextAction( self.gameState )

        except ShuffleShoeException as e:
            print( "Shoe Empty! %s" % str(e) );


