
import json
from .dealershoe import DealerShoe
from .gamestate  import GameState
from .exception  import ShuffleShoeException

class Game:
    def __init__(self, opts, players ):
        print( "Game initializing" )
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
        print( "Game running" )

        self.shoe.dumpShoe()
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
            #self.gameState.printGameTable()
        ##
        # Game Over
        print( self.gameState.statsJson() )

