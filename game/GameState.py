
import random
import json
import pprint

from . import Card
from .hand import Hand
from .Dealer import Dealer
from .color import color

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
                'stats': {
                   'bjs': 0,
                   'wins': 0,
                   'pushes': 0,
                   'loses': 0,
                   'busts': 0,
                },
            })

        random.shuffle(self.seats)

        self.status = "DEALING_HANDS"

        self.seats.append({
            'name': 'dealer',
            'hand': Hand(),
            'agent': Dealer(),
                'stats': {
                   'bjs': 0,
                   'wins': 0,
                   'pushes': 0,
                   'loses': 0,
                   'busts': 0,
                },
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
                self.printGameTable()
                self.status = "DELT"
                print("STATE CHANGE -> DELT")
            else:
                player['hand'].addCard( card )
                #print( "Delt player: %s a %s with value %d" % (player['name'], card, Card.value(card)))
                return

        if self.status == "DELT":
            action = player['agent'].nextAction( self.gameStateJson(), player['hand'] )

            if player['name'] == 'dealer':
                if player['hand'].value() >= 17 or not self.playersRemain():
                    self._currPlayerIndex = -1
                    print("STATE CHANGE -> SCORE")
                    self.status = "SCORE"
                else:
                    player['hand'].addCard( card )
                    #if not player['hand'].hasBusted():
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
                if not player['hand'].hasBusted() and player['hand'].value() != 21:
                    self._currPlayerIndex -= 1
                return;
            elif action not in ['STAND','HIT','DOUBLE','SPLIT']:
                if player['hand'].value() >= 17:
                    self.consumeCard( card )
                    return
                else:
                    player['hand'].addCard( card )
                    if not player['hand'].hasBusted():
                        self._currPlayerIndex -= 1
                    return

        if self.status == "SCORE":
            self.printGameTable()
            self.status = "RESET"

        if self.status == "RESET":
            #print("\nReseting Table")
            for player in self.seats:
                player['hand'] = Hand()
            #print("STATE CHANGE -> DEALING_HANDS")
            print("Dealing...")
            self.status = "DEALING_HANDS"
            self._currPlayerIndex = -1
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
        if self.status == "SCORE":
            dealer = self.getDealerHand()
            for seat in self.seats:
                if( seat['hand'].value() == 21 and (dealer.value() != 21 or seat['name'] == 'dealer') and len(seat['hand'].cards) == 2):
                    score = '*!BlackJack!*'
                    seat['stats']['wins'] +=1
                    seat['stats']['bjs']  +=1
                elif seat['name'] == 'dealer':
                    score = ''
                elif( seat['hand'].value() > 21):
                    score = ''
                    seat['stats']['busts'] +=1
                elif( dealer.value() > 21 and seat['hand'].value() < 22):
                    score = 'Winner!'
                    seat['stats']['wins'] +=1
                elif( seat['hand'].value() < 22 and seat['hand'].value() > dealer.value() ):
                    score = 'Winner!'
                    seat['stats']['wins'] +=1
                elif( seat['hand'].value() < 22 and seat['hand'].value() == dealer.value() ):
                    score = 'push'
                    seat['stats']['pushes'] +=1
                elif( seat['hand'].value() < 22 and seat['hand'].value() < dealer.value() ):
                    score = 'LOSER'
                    seat['stats']['loses'] +=1


                game.append( { 'name': seat['name'], 'hand': str(seat['hand']), 'handVal': int(seat['hand']), 'score': score } )
        else:
            for seat in self.seats:
                if seat['name'] in ['dealer','Dealer']:
                    game.append( { 'name': seat['name'], 'hand': seat['hand'].dealerHand(), 'handVal': '?', 'score': ''} )
                else:
                    game.append( { 'name': seat['name'], 'hand': str(seat['hand']), 'handVal': int(seat['hand']), 'score': ''} )

        return game;

    def playersRemain(self):
        for seat in self.seats:
            if seat['name'] != 'DEALER' and not seat['hand'].hasBusted():
                return True

    def gameStateJson(self):
        return json.dumps(self.gameState())

    def getDealerHand(self):
        return self.seats[-1]['hand']

    def printGameTable(self):
        for idx, seat in enumerate(self.gameState()):
            if seat['name'] in ['dealer','Dealer']:
                gameStringDealer = color.BOLD + color.RED + "Name: {name:32s} Hand: " + color.PURPLE + "{hand}" + color.END + "{score}" + color.END + color.END
                print( gameStringDealer.format_map( seat ) )
            else:
                gameString = color.iterable[idx] + "Name: {name:32s} Hand: {hand}{score}" + color.END
                print( gameString.format_map( seat ) )






