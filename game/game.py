
import json
import time
from pprint import pprint
from .dealershoe import DealerShoe
from .gamestate  import GameState
from .exception  import ShuffleShoeException

class Game:
    def __init__(self, opts, players ):
        print( "Game initializing" )
        print(json.dumps(opts, sort_keys=True, indent=4 ))
        self.opts = opts
        self.players = players

        if( len(self.players) > 4 and opts['decks'] == 1 ):
            print("Too many players for 1 deck!!")

        self.gameState = GameState( opts['decks'], opts['insurance'], opts['randomSeats'], players )
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

    def runShoe(self):
        self.shoe.dumpShoe()
        print( "Shoe running" )
        while self.gameState.status != "GAMEOVER":
            try:
                card = self.shoe.nextCard()
            except ShuffleShoeException as e:
                print( "Last hand in shoe!" )
                self.gameState.newShoeFlag = True
                self.gameState.lastHandNotify()
                card = self.shoe.nextCard()

            self.gameState.consumeCard( card )

            if self.opts['verbose']:
                if self.opts['rate'] is not None:
                    time.sleep( self.opts['rate'] )
                self.gameState.printGameTable()
                print()


