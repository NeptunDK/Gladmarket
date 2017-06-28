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

    def process_orders(self):
        # todo still unsure if this should be here or in the stock class?
        # todo FIFO

        # todo loop to match if there is buy orders matching
        for order in self.orders['buy']:
            if order.price >= self.price:
                logging.warning(f"{order} matched price of: {self.price}")
                # todo update player credit/portfolio
                self.remove_order(order)

        # todo loop to match if there is sell orders matching
        for order in self.orders['sell']:
            if order.price <= self.price:
                logging.warning(f"{order} matched price of: {self.price}")
                # todo update player credit/portfolio
                self.remove_order(order)

        # todo match buy with sell orders


    def remove_order(self, order):
        # todo alter to work with process_orders / complete orders in market class
        if order in self.orders[order.order_type]:
            self.orders[order.order_type].remove(order)
            # todo if buy order, require full buy amount to be put in escrow refund money to player
            # todo if sell order, return stocks to player's portfolio
            logging.warning(f"{order} removed.")
        else:
            logging.warning(f"{order} not found!")


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

    def test_process_orders(self):
        # todo add Player class instance, to test credit/portfolio updates,
        # or maybe have that part in a different test/class
        teststock = Stock('testStock', 1000)
        self.assertEqual(teststock.price, 1000)
        buyorder = Order(900, 1, 'NPC', 'buy')
        sellorder = Order(1100, 1, 'NPC', 'sell')
        teststock.add_order_to_escrow(buyorder)
        teststock.add_order_to_escrow(sellorder)
        teststock.process_orders()
        self.assertIn(buyorder, teststock.orders['buy'])
        self.assertIn(sellorder, teststock.orders['sell'])
        teststock.price = 900
        self.assertEqual(teststock.price, 900)
        teststock.process_orders()
        self.assertNotIn(buyorder, teststock.orders['buy'])
        self.assertIn(sellorder, teststock.orders['sell'])
        teststock.price = 1100
        self.assertEqual(teststock.price, 1100)
        teststock.process_orders()
        self.assertNotIn(buyorder, teststock.orders['buy'])
        self.assertNotIn(sellorder, teststock.orders['sell'])
        print('test_process_orders passed.')

if __name__ == '__main__':
    unittest.main()