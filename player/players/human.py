
from game.color import color

def nextAction(gameStateJson, myHand):
    key = input(("(S)Stand|(H)Hit|(D)Double|(P)Split: (default (S)): \n " + color.GREEN + " %s " + color.END + " :") % myHand)
    if key in ['S','s','stand']:
        return 'STAND'
    elif key in ['H','h','hit']:
        return 'HIT'
    elif key in ['D','d','double','dub']:
        return 'DOUBLE'
    elif key in ['P','p','split','2','Y','y']:
        return 'SPLIT'
    else:
        return 'STAND'

def init( gameState ):
    print("Hello! I'm player2!")
    pass

def name():
    return "PlayerDos"
