#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest
from collections import namedtuple
import random


Order = namedtuple('Order', 'player order_type vol stockname price')


def gen_random_order(player=None, order_type=None, vol=None, stockname=None, price=None):
    if not player:
        player = random.choice(['Player1', 'Player2', 'NPC'])
    if not order_type:
        order_type = random.choice(('buy', 'sell'))
    if not vol:
        vol = random.randint(1, 10)
    if not stockname:
        stockname = random.choice(['IMB', 'DELL', 'HP', 'GOOGLE'])
    if not price:
        price = random.randint(1, 10)

    return Order(player, order_type, vol, stockname, price)


def orders_mergable(order1, order2):
    return (order1.player == order2.player) and (order1.order_type == order2.order_type) \
           and (order1.stockname == order2.stockname) and (order1.price == order2.price)


class TestHelpers(unittest.TestCase):
    def setUp(self):
        # todo
        self.buyorder = Order('NPC', 'buy', 1, 'Teststock', 100)
        self.buyorder_two = Order('NPC', 'buy', 1, 'Teststock', 1100)
        self.sellorder = Order('NPC', 'sell', 1, 'Teststock', 100)
        self.sellorder_two = Order('NPC', 'sell', 1, 'Teststock', 1100)

    def test_Order(self):
        # todo make test_Order unittest
        print('test_Order passed.')

    def test_gen_random_order(self):
        # todo make test_Order unittest
        print('test_gen_random_order passed.')


if __name__ == '__main__':
    unittest.main()
