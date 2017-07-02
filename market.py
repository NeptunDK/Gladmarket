#!/usr/bin/python3
__author__ = 'NeptunDK'

import unittest
from stock import Stock
from player import Player
from helpers import Order


class Market:
    def __init__(self, name):
        self.name = name
        self.stocks = set()
        self.players = set()

    def update_networth(self, player):
        stocks_networth = sum(share.vol * stock.price for share in player.portfolio
                             for stock in self.stocks if share.stockname == stock.name)

        player.networth = player.credit + stocks_networth

    def list_stocks(self):
        return {repr(stock) for stock in self.stocks}
        # return {f"{stock.name} @ {stock.price}" for stock in self.stocks}

    def offer_bid(self):
        # buy 1 IBM
        pass

    def offer_ask(self):
        pass

    # todo process all stocks

    def complete_stock_orders(self):
        # todo update player credit/portfolio, based on the stock returned matched orders
        pass

    def modify_order(self, oldorder, neworder):
        # todo player modify order, not sure yet if this is needed or if there is a better way
        # todo unittest
        # order exsist?
        # remove old order
        # add new order
        pass

    # todo market fees?


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
        self.testplayer.add_to_portfolio(Order(self.testplayer.name, 'buy', 1, 'testStock', 133))
        self.testmarket.update_networth(self.testplayer)
        self.assertEqual(self.testplayer.networth, 11000)
        self.testplayer.add_to_portfolio(Order(self.testplayer.name, 'buy', 1, 'IBM', 133))
        self.testmarket.update_networth(self.testplayer)
        self.assertEqual(self.testplayer.networth, 11133)
        print(repr(self.testplayer.portfolio))
        print(repr(self.testmarket.list_stocks()))
        print('test_update_networth passed.')

    def test_buy_shares(self):
        print(self.testplayer)
        self.testmarket.offer_bid()
        print('test_buy_shares passed.')

if __name__ == '__main__':
    unittest.main()
