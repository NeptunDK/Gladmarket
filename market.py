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

    def update_networth(self):
        # todo update to use CURRENT stockprice, instead of share.buyprice
        share_networth = sum(share.vol * share.buyprice for share in self.portfolio)
        self.networth = self.credit + share_networth

    # todo process all stocks

    def process_matched_orders(self):
        # todo update player credit/portfolio in the market class based returned matched orders
        pass


    def modify_order(self, oldorder, neworder):
        # todo player modify order, not sure yet if this is needed or if there is a better way
        # todo unittest
        # order exsist?
        # remove old order
        # add new order
        pass



class TestStock(unittest.TestCase):
    def setUp(self):
        self.teststock = Stock('testStock', 1000)
        # price, volume, player, type
        self.buyorder = Order(100, 1, 'NPC', 'buy')
        self.sellorder = Order(100, 1, 'NPC', 'sell')

    def test_update_networth(self):
        # todo update to use CURRENT stockprice, instead of share.buyprice
        print(repr(self.testplayer.credit))
        self.assertEqual(self.testplayer.networth, 10000)
        self.testplayer.add_share_to_portfolio(self.testshare)
        print(repr(self.testplayer.portfolio))
        self.testplayer.update_networth()
        self.assertEqual(self.testplayer.networth, 10100)
        self.testsharetwo = Share("Sharetest", 2, 33)
        self.testplayer.add_share_to_portfolio(self.testsharetwo)
        self.testplayer.update_networth()
        self.assertEqual(self.testplayer.networth, 10166)
        print('test_update_networth passed.')

if __name__ == '__main__':
    unittest.main()