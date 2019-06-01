
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

        print( "Game initialized" )

    def play(self):
        print( "Game running" )
        for itr in range(0, self.opts['shoes']):
            if itr > 0:
                self.shoe = DealerShoe(self.opts['decks'])
                self.gameState.newShoeFlag = False
                self.gameState.status = 'DEALING_HANDS'
            self.runShoe()
            print( self.gameState.statsJson() )

        ##
        # Game Over
        #print( self.gameState.statsJson() )

    def runShoe(self):
        self.shoe.dumpShoe()
        print( "Shoe running" )
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


