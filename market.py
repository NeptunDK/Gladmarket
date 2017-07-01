#!/usr/bin/python3
__author__ = 'NeptunDK'

import unittest
from stock import Stock
from player import Player
from helpers import Order, Share

class Market:
    def __init__(self, name):
        self.name = name
        self.stocks = set()
        self.players = set()

    def update_networth(self, player):
        share_networth = sum(share.vol * stock.price for share in player.portfolio
                             for stock in self.stocks if share.stockname == stock.name)

        player.networth = player.credit + share_networth

    def list_stocks(self):
        return {repr(stock) for stock in self.stocks}
        # return {f"{stock.name} @ {stock.price}" for stock in self.stocks}




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
        self.testmarket = Market('GladDAQ')
        self.testmarket.stocks.add(Stock('testStock', 1000))
        self.testmarket.stocks.add(Stock('IBM', 133))
        self.testplayer = Player('Player1')

    def test_list_stocks(self):
        self.assertIn('testStock @ 1000', self.testmarket.list_stocks())
        self.assertIn('IBM @ 133', self.testmarket.list_stocks())
        print('test_list_stocks passed.')

    def test_update_networth(self):
        self.testmarket.update_networth(self.testplayer)
        self.assertEqual(self.testplayer.networth, 10000)
        self.testplayer.add_share_to_portfolio(Share('testStock', 1, 133))
        self.testmarket.update_networth(self.testplayer)
        self.assertEqual(self.testplayer.networth, 11000)
        self.testplayer.add_share_to_portfolio(Share('IBM', 1, 133))
        self.testmarket.update_networth(self.testplayer)
        self.assertEqual(self.testplayer.networth, 11133)
        print(repr(self.testplayer.portfolio))
        print(repr(self.testmarket.list_stocks()))
        print('test_update_networth passed.')

if __name__ == '__main__':
    unittest.main()