#!/usr/bin/env python3

import os
import sys
import argparse
import json
#from yaml import load

opts = argparse.ArgumentParser(
    description=""
)
opts.add_argument('-i','--interactive', action='store_true',
    help='interactive, Enable the human player.')

args = opts.parse_args()

import importlib
import pkgutil

from game   import Game
from player import PlayerModel

import player.players

def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

game_opts = {
    'decks': 6,
    'hitSoft17': True,
    'insurance': True,
}

table_seats = {
    name: importlib.import_module(name)
        for finder, name, ispkg in iter_namespace(player.players)
            if name != 'player.players.human' or args.interactive
}

game = Game.Game( game_opts, table_seats )

game.play()

