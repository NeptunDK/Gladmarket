#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest
from collections import namedtuple



Order = namedtuple('Order', ['price', 'vol', 'player', 'order_type'])

p = Order(2,4, 'NPC', 'buy')
q = Order(2,4, 'NPC', 'sell')
print(p)
print(p.vol)
print(type(p))
print(q)
print(q.vol)
print(type(q))


print(dir(Order))
print(Order.count())


def valid_order_tuple(self, order):
    # type, price, volume, player
    # check order input
    pass



def valid_order_dict(self, order):
    # type, price, volume, player
    # check order input
    pass



# class TestHelpers(unittest.TestCase):
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
