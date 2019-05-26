
import random
import json
import pprint

from . import Card
from .hand import Hand
from .Dealer import Dealer

class GameState:
    def __init__(self, deckCount, players):
        self.seats = []
        self._currPlayerIndex = -1
        self.newShoeFlag = False

        for player in players.keys():
            print( "Loaded %s" % player )
            self.seats.append({
                'name': player,
                'hand': Hand(),
                'agent': players[player],
            })

        random.shuffle(self.seats)

        self.status = "DEALING_HANDS"

        self.seats.append({
            'name': 'dealer',
            'hand': Hand(),
            'agent': Dealer(),
        })
        print("Creating initial game state for %s players" % len(self.seats))

    def consumeCard(self, card):
        player = self.nextPlayer()
        if self.status == "DEALING_HANDS":
            # Shoe empty and fresh round?
            if( (self._currPlayerIndex == 0 and self.newShoeFlag)
             or len(self.seats) <= 1 ):
                self.status = "GAMEOVER"
                print("Game over!")
                return

            # Player one have enough cards?
            if self._currPlayerIndex == 0 and len(player['hand'].cards) == 2:
                self.status = "DELT"
                print("STATE CHANGE -> DELT")
            else:
                player['hand'].addCard( card )
                #print( "Delt player: %s a %s with value %d" % (player['name'], card, Card.value(card)))
                return

        if self.status == "DELT":
            action = player['agent'].nextAction( self.gameStateJson() )

            if player['name'] == 'dealer':

                if player['hand'].value() >= 17:
                    self._currPlayerIndex = -1
                    self.status = "SCORE"
                else:
                    player['hand'].addCard( card )
                    self._currPlayerIndex -= 1
                    return

            elif action == 'STAND':
                self.consumeCard( card )
                return;
            elif action in ['DOUBLE']:
                player['hand'].addCard( card )
                return;
            elif action in ['HIT','SPLIT']:
                player['hand'].addCard( card )
                self._currPlayerIndex -= 1
                return;
            elif action not in ['STAND','HIT','DOUBLE','SPLIT']:
                #self.kickPlayer(player['name'], action)
                if player['hand'].value() >= 17:
                    self.consumeCard( card )
                    return
                else:
                    player['hand'].addCard( card )
                    self._currPlayerIndex -= 1
                    return

        if self.status == "SCORE":
            print("Scoring Game")
            self.status = "RESET"

        if self.status == "RESET":
            print("Reseting Table")
            for player in self.seats:
                player['hand'] = Hand()
            self.status = "DEALING_HANDS"
            self.consumeCard( card )

    def kickPlayer(self, playerName, action):
        print("Kicking %s, invalid action %s, %s players Remain" % (playerName, action, len(self.seats)-2) )
        self.seats.pop(self._currPlayerIndex)
        self._currPlayerIndex -= 1

    def nextPlayer(self):
        self._currPlayerIndex += 1
        if self._currPlayerIndex >= len(self.seats):
            self._currPlayerIndex = 0
            return self.seats[0]
        else:
            return self.seats[self._currPlayerIndex]

    def gameState(self):
        game = []
        for row in self.seats:
            game.append( { 'name': row['name'], 'hand': str(row['hand']), 'handVal': int(row['hand']), } )
        return game;

    def gameStateJson(self):
        return json.dumps(self.gameState())

    def printGameTable(self):
        gameString = """Name: {name:32s} Hand: {hand}({handVal})"""
        for seat in self.gameState():
            print( gameString.format_map( seat ) )

