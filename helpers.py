#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest
from collections import namedtuple

Order = namedtuple('Order', ['price', 'vol', 'player', 'order_type'])
Share = namedtuple('Share', ['stockname', 'vol', 'buyprice'])

def convert_to_share(stock, order):
    return Share(stock.name, order.vol, order.price)

def convert_share_to_order():
    pass




def valid_order_tuple(self, order):
    # type, price, volume, player
    # check order input
    pass



def valid_order_dict(self, order):
    # type, price, volume, player
    # check order input
    pass



class TestHelpers(unittest.TestCase):
    def setUp(self):
        from stock import Stock
        from player import Player

        self.testplayer = Player('Player1', 10000, 'Is only a test.')
        self.teststock = Stock("teststock", 1000)
        self.buyorder = Order(100, 1, 'Player1', 'buy')
        self.sellorder = Order(100, 1, 'Player1', 'sell')
        self.testshare = Share(self.teststock.name, self.buyorder.vol , self.buyorder.price)

    def test_convert_to_share(self):
        self.assertEqual(convert_to_share(self.teststock, self.buyorder), self.testshare)
        print('test_convert_to_share passed.')

#
#
#     def test_valid_order_tuple(self):
#         valid_buy_order = ('buy', 100, 1, 'NPC')
#         valid_sell_order = ('sell', 100, 1, 'NPC')
#         invalid_order = (100, 1, 'NPC')
#
#         self.assert
#
#         def test_valid_order_dict(self):
#             valid_buy_order = (type'buy', 100, 1, 'NPC')
#             valid_sell_order = ('sell', 100, 1, 'NPC')
#             invalid_order = (100, 1, 'NPC')
#
#             self.
#             assert
#
