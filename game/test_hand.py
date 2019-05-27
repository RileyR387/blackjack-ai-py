
from .hand import Hand
from .deck import Deck

cards = Deck.cards()

ACE  = cards[0]
TWO  = cards[(2-1)*4]
FIVE = cards[(5-1)*4]
NINE = cards[(9-1)*4]
TEN  = cards[(10-1)*4]

hand = Hand()
for idx in range(0,10):
    hand.addCard( cards[idx%4] )

print(hand)
print('Soft: ', hand.isSoft())
hand.addCard( ACE );
print(hand)
print('Soft: ', hand.isSoft())
hand.addCard( ACE );
print(hand)
print('Soft: ', hand.isSoft())

hand.addCard( FIVE );
print(hand)
print('Soft: ', hand.isSoft())

hand.addCard( FIVE );
print(hand)
print('Soft: ', hand.isSoft())

hand = Hand()
hand.addCard( ACE );
hand.addCard( FIVE );
print(hand)
print('Soft: ', hand.isSoft())

hand.addCard( ACE );
print(hand)
print('Soft: ', hand.isSoft())

hand = Hand()
hand.addCard( ACE );
hand.addCard( NINE );
print(hand)
print('Soft: ', hand.isSoft())

hand.addCard( TWO );
print(hand)
print('Soft: ', hand.isSoft())

hand.addCard( ACE );
print(hand)
print('Soft: ', hand.isSoft())

