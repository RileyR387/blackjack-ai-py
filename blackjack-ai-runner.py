#!/usr/bin/env python3

import os
import sys
import argparse

opts = argparse.ArgumentParser(
    description=""
)
opts.add_argument('-i','--interactive',
    action='store_true',
    help='interactive, Enable the human player.')

opts.add_argument('-r','--rate',
    type=float,
    help='Rate of play in seconds (time to deal 1 card, requires interaction.')

opts.add_argument('-d','--decks',
    type=int,
    help='Number of decks in each shoe')

opts.add_argument('-s','--shoes',
    type=int, default=5,
    help='Number of shoes (games) to play')

opts.add_argument('-a','--agents',
    type=str, nargs='+', default='',
    help='Agents to enable')

opts.add_argument('-z','--randomSeatOrder',
    action='store_true',
    help='Randomize table seats at start of run.')

opts.add_argument('-u','--urwidUI',
    action='store_true',
    help='Enable Urwid, pythons console UI library')

opts.add_argument('-v','--verbose',
    action='store_true',
    help='Print table as each card is delt')

args = opts.parse_args()

import importlib
import pkgutil
import player.players

def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")
table_seats = {}

if len(args.agents) == 0:
    table_seats = {
        name: importlib.import_module(name)
            for finder, name, ispkg in iter_namespace(player.players)
                if(
                    ((name != 'player.players.human' or args.interactive) and len(args.agents) == 0)
                 or
                    ((name.split('.')[2] in args.agents or name in args.agents )and len(args.agents) > 0)
                )
    }
else:
    table_seats = {
        name: importlib.import_module('player.players.' + name)
            for name in args.agents
    }

game_opts = {
    'shoes': args.shoes or 2,
    'decks': args.decks or 6,
    'rate': args.rate or None,
    'randomSeats': args.randomSeatOrder or False,
    'hitSoft17': True,
    'insurance': True,
    'urwidUI': args.urwidUI or False,
    'verbose': args.verbose or False,
}

from game.game import Game
game = Game( game_opts, table_seats )
game.play()

