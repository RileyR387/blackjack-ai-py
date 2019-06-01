#!/usr/bin/env python3

import os
import sys
import argparse
import json

opts = argparse.ArgumentParser(
    description=""
)
opts.add_argument('-i','--interactive',
    action='store_true',
    help='interactive, Enable the human player.')

opts.add_argument('-d','--decks',
    type=int,
    help='Number of decks in each shoe')

opts.add_argument('-s','--shoes',
    type=int, default=10,
    help='Number of shoes (games) to play')

opts.add_argument('-a','--agents',
    type=str, nargs='+', default='',
    help='Agents to enable')

opts.add_argument('-v','--verbose',
    action='store_true',
    help='Agents to enable')

args = opts.parse_args()

import importlib
import pkgutil

import player.players

from game.game   import Game

def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

game_opts = {
    'shoes': args.shoes or 2,
    'decks': args.decks or 6,
    'hitSoft17': True,
    'insurance': True,
    'verbose': args.verbose or False,
}

print( "Loading agents: ", args.agents )

table_seats = {
    name: importlib.import_module(name)
        for finder, name, ispkg in iter_namespace(player.players)
            if( ((name != 'player.players.human' or args.interactive) and len(args.agents) == 0)
                or (name in args.agents and len(args.agents) > 0))
}

game = Game( game_opts, table_seats )

game.play()

