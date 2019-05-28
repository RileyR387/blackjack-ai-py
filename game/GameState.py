
import random
import json
import pprint

from . import Card
from .hand import Hand
from .Dealer import Dealer
from .color import color

class GameState:
    def __init__(self, deckCount, insurance, players):
        self.seats = []
        self._currPlayerIndex = -1
        self._enableInsurance = insurance
        self._MIN_BET = 5
        self.newShoeFlag = False

        for player in players.keys():
            print( "Loaded %s" % player )
            self.seats.append({
                'name': player,
                'hand': Hand(),
                'bet': 0,
                'agent': players[player].Agent(),
                'handsPlayed': 0,
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
            'bet': 0,
            'agent': Dealer(),
            'handsPlayed': 0,
                'stats': {
                   'bjs': 0,
                   'wins': 0,
                   'pushes': 0,
                   'loses': 0,
                   'busts': 0,
                },
        })
        print("Created initial game state for %s players" % (len(self.seats)-1))

    def consumeCard(self, card):
        player = self.nextPlayer()
        if self.status == "DEALING_HANDS":
            if self._dealHand( player, card ) is not None:
                self.status = 'DELT'
                pass
            else:
                return

        if self.status == "DELT":
            if self._queryPlayers( player, card) is not None:
                self.status = 'SCORE'
                pass
            else:
                return

        if self.status == "SCORE":
            self._score()
            self.printGameTable()
            #input()
            if self._clearRound():
                self._takeBets()
                self.consumeCard( card )
                return
            else:
                print("Game over!")
                self.status = 'GAMEOVER'
                return

    def _clearRound(self):
        for player in self.seats:
            player['hand'] = Hand()
        if not self.newShoeFlag:
            self.status = "DEALING_HANDS"
            self._currPlayerIndex = -1
            return True
        else:
            return False

    def _takeBets(self):
        for player in self.seats:
            try:
                player['bet'] = player['agent'].placeBet( self.gameStateJson() )
            except Exception as e:
                player['bet'] = self._MIN_BET

    def _queryPlayers( self, player, card):
         action = None
         if not self._roundCanStart(player, card):
             return 'SCORE'

         if player['name'] == 'dealer':
             dealerHand = self.getDealerHand()
             if(   self.playersRemain()
               and ((dealerHand.value() == 17 and dealerHand.isSoft())
               or dealerHand.value() < 17)
             ):
                 player['hand'].addCard( card )
                 self._currPlayerIndex -= 1
                 return
             else:
                 dealerHand.isFinal = True
                 self._currPlayerIndex = -1
                 print("STATE CHANGE -> SCORE")
                 self.status = "SCORE"
                 return 'SCORE'
         elif player['hand'].value != 21 and not player['hand'].hasBusted():
             self._handleAction( player, card )
         else:
             self.consumeCard( card )
             return

    def _roundCanStart(self, player, card):
        if self._currPlayerIndex == 0 and len(player['hand'].cards) == 2:
            dealerHand = self.getDealerHand()
            if dealerHand.offerInsurance() and self._enableInsurance:
                print("Offering Insurance...")
                for seat in self.seats:
                    try:
                        if seat['agent'].takeInsurance( self.gameStateJson(), player['hand'] ):
                            #TODO: account for insurance
                            pass
                    except Exception as e:
                        pass
                if dealerHand.isBlackjack():
                    print("Dealer Blackjacked!")
                    self.status = "SCORE"
                    return False
                else:
                    pass
            else:
                pass
        else:
            pass
        return True

    def _handleAction(self, player, card):

        thisHand = self._nextHand(player, card)

        if thisHand is None:
            return

        action = player['agent'].nextAction( self.gameStateJson(), thisHand )
        if action == 'STAND':
            thisHand.isFinal = True
            while thisHand.nextHand is not None:
                if thisHand.nextHand.isFinal == False:
                    self._currPlayerIndex -= 1
                    break

            self.consumeCard( card )
            return
        elif action in ['DOUBLE']:
            thisHand.addCard( card )
            thisHand.isFinal = True
            return
        elif action in ['HIT']:
            thisHand.addCard( card )
            if( (not thisHand.hasBusted() and thisHand.value() != 21)
                or ( thisHand.nextHand is not None and thisHand.nextHand.isFinal == False )
                ):
                self._currPlayerIndex -= 1
            else:
                thisHand.isFinal = True
            return
        elif action in ['SPLIT']:
            if thisHand.canSplit():
                thisHand.splitHand()
                thisHand.addCard( card )
                if( (not thisHand.hasBusted() and thisHand.value() != 21)
                    or ( thisHand.nextHand is not None and thisHand.nextHand.isFinal == False )
                    ):
                    self._currPlayerIndex -= 1
                else:
                    thisHand.isFinal = True
                return
            else:
                thisHand.addCard( card )
                if( (not thisHand.hasBusted() and thisHand.value() != 21)
                    or ( thisHand.nextHand is not None and thisHand.nextHand.isFinal == False )
                    ):
                    self._currPlayerIndex -= 1
                else:
                    thisHand.isFinal = True
                return
        elif action not in ['STAND','HIT','DOUBLE','SPLIT']:
            if thisHand.value() >= 17:
                thisHand.isFinal = True
                self.consumeCard( card )
                return
            else:
                thisHand.addCard( card )
                if( (not thisHand.hasBusted() and thisHand.value() != 21)
                    or ( thisHand.nextHand is not None and thisHand.nextHand.isFinal == False )
                    ):
                    self._currPlayerIndex -= 1
                else:
                    thisHand.isFinal = True
                return

    def _nextHand(self, player, card):
        thisHand = player['hand']
        if thisHand.isFinal and thisHand.nextHand is not None:
            while thisHand.nextHand is not None:
                thisHand = thisHand.nextHand
                if len(thisHand.cards) is 1:
                    thisHand.addCard( card )
                    self._currPlayerIndex -= 1
                    return None
                if thisHand.isFinal == False:
                    return thisHand
        return thisHand

    def _dealHand(self, player, card):
        # Shoe empty and fresh round?
        if( self._currPlayerIndex == 0 and len(player['hand'].cards) == 0):
            self._takeBets()
            print("Dealing...")

        # Player one have enough cards?
        if self._currPlayerIndex == 0 and len(player['hand'].cards) == 2:
            self.printGameTable()
            self.status = "DELT"
            print("STATE CHANGE -> DELT")
            return True;
        else:
            player['hand'].addCard( card )
            return None

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
                seat['handsPlayed'] += 1
                if( (seat['hand'].value() == 21 and (dealer.value() != 21 or seat['name'] == 'dealer') and len(seat['hand'].cards) == 2)
                 or (seat['name'] != 'dealer' and seat['hand'].value() == 21 and len(seat['hand'].cards) == 2 and dealer.value() == 21 and len(dealer.cards) > 2)
                ):
                    score = '*!BlackJack!*'
                    seat['stats']['wins'] +=1
                    seat['stats']['bjs']  +=1
                elif seat['name'] == 'dealer':
                    if not seat['hand'].hasBusted():
                        if not self.playersRemain():
                            score = 'Winner!'
                            seat['stats']['wins'] += 1
                        else:
                            score = ''
                    else:
                        score = ''
                        seat['stats']['busts'] += 1
                elif( seat['hand'].value() > 21):
                    score = ''
                    seat['stats']['busts'] +=1
                elif( dealer.value() > 21 and seat['hand'].value() < 22):
                    score = 'Winner!'
                    seat['stats']['wins'] +=1
                elif( seat['hand'].value() < 22 and seat['hand'].value() > dealer.value() ):
                    score = 'Winner!'
                    seat['stats']['wins'] +=1
                    self.getDealer()['stats']['loses'] += 1
                elif( seat['hand'].value() < 22 and seat['hand'].value() == dealer.value() ):
                    score = 'push'
                    self.getDealer()['stats']['pushes'] += 1
                    seat['stats']['pushes'] +=1
                elif( seat['hand'].value() < 22 and seat['hand'].value() < dealer.value() ):
                    score = 'LOSER'
                    seat['stats']['loses'] +=1

                game.append({
                  seat['name']:
                    {
                      'name': seat['name'],
                      'handStr': str(seat['hand']),
                      'hand': seat['hand'].cards,
                      'handVal': int(seat['hand']),
                      'score': score,
                    }
                })
        else:
            for seat in self.seats:
                if seat['name'] in ['dealer','Dealer']:
                    game.append({
                      seat['name']:
                      {
                        'name': seat['name'],
                        'hand': seat['hand'].cards[0],
                        'handStr': seat['hand'].dealerHand(),
                        'handVal': Card.value(seat['hand'].cards[0]),
                        'score': ''
                      }
                    })
                else:
                    game.append({
                      seat['name']:
                        {
                          'name': seat['name'],
                          'handStr': str(seat['hand']),
                          'hand': seat['hand'].cards,
                          'handVal': int(seat['hand']),
                          'score': '',
                        }
                    })

        return game;

    def playersRemain(self):
        for seat in self.seats:
            if seat['name'] != 'DEALER' and not seat['hand'].hasBusted():
                return True
        return False

    def gameStateJson(self):
        return json.dumps(self.gameState(), sort_keys=True, indent=4 )

    def getDealer(self):
        return self.seats[-1]

    def getDealerHand(self):
        return self.getDealer()['hand']

    def statsJson(self):
        statsArray = []
        statsStr = '';
        for idx, player in enumerate(self.seats):
            statsArray.append(
                json.dumps( {
                  'name': player['name'],
                  'seat': idx,
                  'handsPlayed': player['handsPlayed'],
                  'stats': player['stats']
                }, sort_keys=True, indent=4 )
            )
        return '[' + ',\n'.join(statsArray) + "]\n"

    def _score(self):
        pass

    def printGameTable(self):
        for idx, seat in enumerate(self.gameState()):
            for playerName, player in seat.items():
                if player['name'] in ['dealer','Dealer']:
                    gameStringDealer = (color.BOLD + color.RED + "Name: {name:32s} Hand: " +
                        color.PURPLE + "{handStr}" + color.END + "{score}" + color.END + color.END)
                    print( gameStringDealer.format_map( player ) )
                else:
                    gameString = color.iterable[idx] + "Name: {name:32s} Hand: {handStr}{score}" + color.END
                    print( gameString.format_map( player ) )


