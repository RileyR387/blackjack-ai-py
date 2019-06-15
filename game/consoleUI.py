
import json
import curses
import sys
import locale

from pprint import pprint

from .color import color

class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-30:])
    def get_text(self,beg,end):
        return '\n'.join(self.text.split('\n')[beg:end])

class ConsoleUI:
    def __init__(self):
        self.gameState = None
        self.enabled = False
        self.running = False
        locale.setlocale(locale.LC_ALL, '')
        print( "My local is: %s" % locale.getpreferredencoding() )
        self.stdscr = None

    def start(self):
        if not self.running and self.enabled:
            mystdout = StdOutWrapper()
            sys.stdout = mystdout
            sys.stderr = mystdout
            self.stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()

            curses.start_color()
            curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_BLACK)
            curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_RED)
            self.stdscr.keypad(True)
            self.running = True

    def disable(self):
        curses.echo()
        self.running = False
        self.enabled = False
        screen.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdout.write(mystdout.get_text())

    def enable(self):
        if self.stdscr is not None:
            curses.noecho()
        self.enabled = True

    def update(self, gameStateJson):
        if not self.enabled or gameStateJson is None or gameStateJson == '':
            pass
        else:
            self.gameState = json.loads(gameStateJson)

        self.stdscr.clear()

        for idx, seat in enumerate(self.gameState):
            for player, hand in seat.items():
                if player in ['dealer','Dealer']:
                    gameStringDealer = u"{bankRoll:10.2f} Name: {name:32s} Hand: {handStr}{score}"
                    self.stdscr.addstr(
                        curses.LINES-len(self.gameState)+idx-4, 0,
                        gameStringDealer.format_map( hand ),
                        curses.color_pair( 7 )
                    )

                else:
                    gameString = u"{bankRoll:10.2f} Name: {name:32s} Hand: {handStr}{score} {amt}"
                    self.stdscr.addstr(
                        curses.LINES-len(self.gameState)+idx-4, 0,
                        gameString.format_map( hand ),
                        curses.color_pair( (idx%6)+1 )
                    )
        self.stdscr.addstr(curses.LINES-1,curses.COLS-1,'', curses.COLOR_RED)
        self.stdscr.refresh()

    def terminate(self):
        self.disable()
        curses.endwin()
        self.running = False
        pass

    def _debug(self):
        self.stdscr.addstr( 10, 0, "My local is: %s" % locale.getpreferredencoding() )
        for idx, line in enumerate(gameStateJson.split('\n')):
            if idx < 30:
                self.stdscr.addstr( 12+idx, 0, line )
        self.stdscr.addstr(3, 0, u"\u2660".encode('UTF-8'))

