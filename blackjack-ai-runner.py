#!/usr/bin/env python3

import os
import sys

import importlib
import pkgutil

from pprint import pprint

from game   import Game
from player import PlayerModel

import player.players

def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

table_seats = {
    name: importlib.import_module(name)
        for finder, name, ispkg in iter_namespace(player.players)
}

pprint( table_seats )
#pprint( players )
state = {};
for seat in table_seats.keys():
    table_seats[seat].nextAction( state )

#shoe = Game( decks = 6, table );

