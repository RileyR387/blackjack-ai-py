
import json
from pprint import pprint
from .dealershoe import DealerShoe
from .gamestate  import GameState
from .exception  import ShuffleShoeException

class Game:
    def __init__(self, opts, players ):
        print( "Game initializing" )
        pprint( opts )
        self.opts = opts
        self.players = players

        self.gameState = GameState( opts['decks'], opts['insurance'], players )
        self.shoe  =  DealerShoe(opts['decks'])

        self.house = {
            'bankroll': 10^6,
            'minbet': 5,
        }
        print( "Game initialized" )

    def play(self):
        self.shoe.dumpShoe()
        print( "Game running" )
        ##
        # Play!
        while self.gameState.status != "GAMEOVER":
            try:
                card = self.shoe.nextCard()
            except ShuffleShoeException as e:
                print( "Last hand in shoe!" )
                self.gameState.newShoeFlag = True
                card = self.shoe.nextCard()

            self.gameState.consumeCard( card )

            if self.opts['verbose']:
                self.gameState.printGameTable()
                print()

        ##
        # Game Over
        print( self.gameState.statsJson() )

