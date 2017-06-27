#!/usr/bin/python3
__author__ = 'NeptunDK'

import unittest
from stock import Stock
from player import Player
from helpers import Order, Share

class Market:
    def __init__(self, name):
        self.name = name
        self.stocks = {}

    # todo process all stocks
    #
