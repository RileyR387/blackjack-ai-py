
import random
import json
import pprint

import game.card as Card

from .hand import Hand
from .dealer import Dealer
from .color import color

THREE_TO_TWO = 1.5
TWO_TO_ONE = 2

class GameState:
    def __init__(self, deckCount, insurance, randomSeats, players):
        self.seats = []
        self.players = players
        self._currPlayerIndex = -1
        self._enableInsurance = insurance
        self._MIN_BET = 5
        self.newShoeFlag = False
        self.priorGameStateJson = ''

        print( "Loading agents: \n%s" % json.dumps([ player for player in self.players.keys() ], sort_keys=True, indent=4 ) )
        for player in self.players.keys():
            print( "Loaded %s" % player )
            self.seats.append({
                'name': player,
                'hands': [Hand()],
                'agent': players[player].Agent(),
                'roundsPlayed': 0,
                'handsPlayed': 0,
                'bankRoll': 200,
                'stats': {
                   'bjs': 0,
                   'wins': 0,
                   'splits': 0,
                   'doubles': 0,
                   'pushes': 0,
                   'loses': 0,
                   'busts': 0,
                },
            })

        if randomSeats:
            random.shuffle(self.seats)

        self.status = "DEALING_HANDS"

        self.seats.append({
            'name': 'dealer',
            'hands': [Hand()],
            'agent': Dealer(),
            'roundsPlayed': 0,
            'handsPlayed': 0,
            'bankRoll': 100000,
            'stats': {
               'bjs': 0,
               'wins': 0,
               'splits': 0,
               'doubles': 0,
               'pushes': 0,
               'loses': 0,
               'busts': 0,
            },
        })
        print("Created initial game state for %s players" % (len(self.seats)-1))

    def consumeCard(self, card):
        #self.printBankrollsBets();
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
            self.printGameTable()
            #input()
            if self._clearRound():
                self.consumeCard( card )
                return
            else:
                print("Game over!")
                self.status = 'GAMEOVER'
                return


    def printBankrollsBets(self):
        for player in self.seats:
            for hand in player['hands']:
                print("player %s bankroll %s bet %s" % (player['name'], player['bankRoll'], hand._bet) )

    def _clearRound(self):
        self.priorGameStateJson = self.gameStateJson()
        for player in self.seats:
            player['hands'] = [Hand()]
        if not self.newShoeFlag:
            self.status = "DEALING_HANDS"
            self._currPlayerIndex = -1
            return True
        else:
            return False

    def _takeBets(self):
        for player in self.seats:
            for hand in player['hands']:
                if player['name'] not in ['Dealer','dealer']:
                    try:
                        hand._bet = player['agent'].placeBet( self.priorGameStateJson )
                        player['bankRoll'] -= hand._bet
                    except Exception as e:
                        print( "%s failed to placeBet(), using minimums of %s"%( player['name'], self._MIN_BET))
                        hand._bet = self._MIN_BET
                        player['bankRoll'] -= hand._bet

    def lastHandNotify(self):
        for player in self.seats:
            for hand in player['hands']:
                if player['name'] not in ['Dealer','dealer']:
                    try:
                        player['agent'].notifyNewShoe()
                    except Exception as e:
                        print( "%s missing notifyNewShoe()" % player['name'])

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
                 dealerHand.addCard( card )
                 return
             else:
                 dealerHand.isFinal = True
                 print("STATE CHANGE -> SCORE")
                 self.status = "SCORE"
                 return 'SCORE'
         else:
            thisHand = self._nextHand(player)
            if thisHand is None:
                self.consumeCard( card )
                return
            if len(thisHand.cards) < 2:
                thisHand.addCard( card )
                return

            action = player['agent'].nextAction( self.gameStateJson(), thisHand )
            self._handleAction( player, card, thisHand, action )

    def _roundCanStart(self, player, card):
        if( self._currPlayerIndex == 0
          and len(player['hands'][0].cards) == 2
          and len(player['hands']) == 1
          ):
            dealerHand = self.getDealerHand()
            if dealerHand.offerInsurance() and self._enableInsurance:
                print("Offering Insurance...")
                for seat in self.seats:
                    try:
                        if seat['agent'].takeInsurance( self.gameStateJson(), player['hands'][0] ):
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

    def _handleAction(self, player, card, thisHand, action):
        if action == 'STAND':
            thisHand.isFinal = True
            self.consumeCard( card )
            return
        elif action in ['DOUBLE']:

            if thisHand.canDouble():
                thisHand.addCard( card )
                player['stats']['doubles'] += 1
                player['bankRoll'] -= thisHand._bet
                thisHand._bet = thisHand._bet*2
                thisHand.isFinal = True
            else:
                thisHand.addCard( card )

            if thisHand.hasBusted() or thisHand.value() == 21:
                thisHand.isFinal = True

        elif action in ['HIT']:
            thisHand.addCard( card )
            if thisHand.hasBusted() or thisHand.value() == 21:
                thisHand.isFinal = True
        elif action in ['SPLIT']:
            if not self.newShoeFlag and thisHand.canSplit():
                player['stats']['splits'] += 1
                player['bankRoll'] -= thisHand._bet
                nextHand = thisHand.splitHand()
                nextHand._bet = thisHand._bet
                player['hands'].append(nextHand)
                thisHand.addCard( card )
                if thisHand.hasBusted() or thisHand.value() == 21:
                    thisHand.isFinal = True
                return
            else:
                thisHand.addCard( card )
                if thisHand.hasBusted() or thisHand.value() == 21:
                    thisHand.isFinal = True
                return
        elif action not in ['STAND','HIT','DOUBLE','SPLIT']:
            if thisHand.value() >= 17:
                thisHand.isFinal = True
                self.consumeCard( card )
                return
            else:
                thisHand.addCard( card )
                if thisHand.hasBusted() or thisHand.value() == 21:
                    thisHand.isFinal = True
                return

    def _nextHand(self, player):
        for thisHand in player['hands']:
            if thisHand.isFinal or thisHand.hasBusted():
                pass
            else:
                return thisHand
        return None

    def _dealHand(self, player, card):
        # Shoe empty and fresh round?
        thisHand = player['hands'][0]
        if( self._currPlayerIndex == 0 and len(thisHand.cards) == 0):
            self._takeBets()
            print("Dealing...")

        # Player one have enough cards?
        if self._currPlayerIndex == 0 and len(thisHand.cards) == 2:
            self.printGameTable()
            self.status = "DELT"
            print("STATE CHANGE -> DELT")
            return True
        else:
            thisHand.addCard( card )
            return None

    def kickPlayer(self, playerName, action):
        print("Kicking %s, invalid action %s, %s players Remain" % (playerName, action, len(self.seats)-2) )
        self.seats.pop(self._currPlayerIndex)
        self._currPlayerIndex -= 1

    def nextPlayer(self):
        if self.status == "DEALING_HANDS":
            self._currPlayerIndex += 1
            if self._currPlayerIndex >= len(self.seats):
                self._currPlayerIndex = 0
                return self.seats[0]
            else:
                return self.seats[self._currPlayerIndex]

        thisHand = self._nextHand(self.seats[self._currPlayerIndex])
        if thisHand is None:
            self._currPlayerIndex += 1

        if self._currPlayerIndex >= len(self.seats):
            self._currPlayerIndex = 0
            return self.seats[0]
        else:
            return self.seats[self._currPlayerIndex]

    def gameState(self):
        game = []
        #pprint.pprint(self.seats)
        if self.status == "SCORE":
            dealer = self.getDealerHand()
            for seat in self.seats:
                seat['roundsPlayed'] += 1
                for hand in seat['hands']:
                    seat['handsPlayed'] += 1
                    startBalance = seat['bankRoll'];
                    ##
                    # Blackjack
                    if( (hand.value() == 21 and (dealer.value() != 21 or seat['name'] == 'dealer') and len(hand.cards) == 2)
                     or (seat['name'] != 'dealer' and hand.value() == 21 and len(hand.cards) == 2 and dealer.value() == 21 and len(dealer.cards) > 2)
                    ):
                        score = '*!BlackJack!*'
                        seat['stats']['bjs']  +=1
                        seat['stats']['wins'] +=1
                        seat['bankRoll'] += ((hand._bet * THREE_TO_TWO) + hand._bet)
                        self.getDealer()['bankRoll'] -= (hand._bet * THREE_TO_TWO)
                        self.getDealer()['stats']['loses'] += 1
                        hand._bet = 0
                    ##
                    # Dealer
                    elif seat['name'] == 'dealer':
                        if not hand.hasBusted():
                            if not self.playersRemain():
                                score = 'Winner!'
                                seat['stats']['wins'] += 1
                            else:
                                score = ''
                        else:
                            score = ''
                            seat['stats']['busts'] += 1
                    ##
                    # Busts
                    elif( hand.value() > 21):
                        score = ''
                        seat['stats']['busts'] += 1
                        self.getDealer()['bankRoll'] += hand._bet
                        hand._bet = 0
                    ##
                    # Wins
                    elif(
                        (dealer.value() > 21 and hand.value() < 22)
                      or
                        (hand.value() < 22 and hand.value() > dealer.value())
                      ):
                        score = 'Winner!'
                        seat['stats']['wins'] +=1
                        seat['bankRoll'] += (hand._bet*2)
                        ## Deailer
                        self.getDealer()['bankRoll'] -= hand._bet
                        self.getDealer()['stats']['loses'] += 1
                        ## Reset
                        hand._bet = 0
                    ##
                    # Pushes
                    elif( hand.value() < 22 and hand.value() == dealer.value() ):
                        score = 'push'
                        self.getDealer()['stats']['pushes'] += 1
                        seat['stats']['pushes'] += 1
                        seat['bankRoll'] += hand._bet
                        hand._bet = 0
                    elif( hand.value() < 22 and hand.value() < dealer.value() ):
                        score = 'LOSER'
                        seat['stats']['loses'] += 1
                        self.getDealer()['stats']['wins'] += 1
                        self.getDealer()['bankRoll'] += hand._bet
                        hand._bet = 0

                    game.append({
                      seat['name']:
                        {
                          'name': seat['name'],
                          'agent': seat['agent'].name,
                          'hand': hand.cards,
                          'handStr': str(hand),
                          'handVal': int(hand),
                          'amt': (seat['bankRoll'] - startBalance),
                          'score': score,
                          'bankRoll': seat['bankRoll'],
                        }
                    })
        else: # Not scoring...
            for seat in self.seats:
                for hand in seat['hands']:
                    if len(hand.cards) > 0:
                        if seat['name'] in ['dealer','Dealer']:
                            game.append({
                              seat['agent'].name:
                                {
                                  'name': seat['name'],
                                  'agent': seat['agent'].name,
                                  'hand': [ hand.cards[0] ],
                                  'handStr': hand.dealerHand(),
                                  'handVal': Card.value(hand.cards[0]),
                                  'score': '',
                                  'amt': hand._bet,
                                  'bankRoll': seat['bankRoll'],
                                }
                            })
                        else:
                            game.append({
                              seat['agent'].name:
                                {
                                  'name': seat['name'],
                                  'agent': seat['agent'].name,
                                  'handStr': str(hand),
                                  'hand': hand.cards,
                                  'handVal': int(hand),
                                  'score': '',
                                  'amt': hand._bet,
                                  'bankRoll': seat['bankRoll'],
                                }
                            })

        return game;

    def playersRemain(self):
        for seat in self.seats:
            if seat['name'] != 'DEALER':
                for hand in seat['hands']:
                    if not hand.hasBusted():
                        return True
        return False

    def gameStateJson(self):
        return json.dumps(self.gameState(), sort_keys=True, indent=4 )

    def getDealer(self):
        return self.seats[-1]

    def getDealerHand(self):
        return self.getDealer()['hands'][0]

    def statsJson(self):
        statsArray = []
        statsStr = '';
        for idx, player in enumerate(self.seats):
            statsArray.append(
                json.dumps( {
                  'name': player['name'],
                  'seat': idx,
                  'roundsPlayed': player['roundsPlayed'],
                  'handsPlayed': player['handsPlayed'],
                  'bankRoll': player['bankRoll'],
                  'stats': player['stats']
                }, sort_keys=True, indent=4 )
            )
        return '[' + ',\n'.join(statsArray) + "]\n"

    def printGameTable(self):
        for idx, seat in enumerate(self.gameState()):
            for playerName, player in seat.items():
                if player['name'] in ['dealer','Dealer']:
                    gameStringDealer = (color.BOLD + color.RED + "{bankRoll:10.2f} Name: {name:32s} Hand: " +
                        "{handStr}" + color.END + "{score}" + color.END + color.END)
                    print( gameStringDealer.format_map( player ) )
                else:
                    gameString = "" + color.iterable[(idx % len(color.iterable))] + "{bankRoll:10.2f} Name: {name:32s} Hand: {handStr}{score} {amt}" + color.END
                    print( gameString.format_map( player ) )


