
import json
from . import DealersShoe, GameState
from .exception import ShuffleShoeException

class Game:
    def __init__(self, opts, players ):
        print( "Game initializing" )
        self.opts = opts
        self.players = players

        self.gameState = GameState.GameState( opts['decks'], opts['insurance'], players )
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

        while self.gameState.status != "GAMEOVER":
            try:
                card = self.shoe.nextCard()
            except ShuffleShoeException as e:
                print( "Last hand in shoe!" )
                self.gameState.newShoeFlag = True
                card = self.shoe.nextCard()

            self.gameState.consumeCard( card )

            #if self.gameState.status != "DEALING_HANDS":
            #    self.gameState.printGameTable()

        ##
        # Game Over
        print( self.gameState.statsJson() )

