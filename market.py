#!/usr/bin/python3
__author__ = 'NeptunDK'

import unittest
from stock import Stock
from player import Player
from helpers import Order, Share

class Market:
    def __init__(self, name):
        self.name = name
        self.stocks = None

    # todo figure out good layout of orders.
        # could be market.orders['buy'], market.buyorders, market.stocks.orders['buy']
    # todo maybe most of the order methods under a stock should be here?!









