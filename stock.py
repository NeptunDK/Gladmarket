#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest
import logging
from collections import namedtuple
# import helpers

Order = namedtuple('Order', ['price', 'vol', 'player', 'order_type'])

class Stock:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.high_price = price
        self.low_price = price
        self.orders = {'buy': [], 'sell': []} #hmmm set or list????

    def add_order(self, neworder):
        similar_order = self.player_similar_order(neworder)

        if not similar_order:
            self.orders[neworder.order_type].append(neworder)
        else:
            #update similar order
            current_volume = similar_order[0].vol
            price, vol, player, order_type = neworder
            vol += current_volume
            updated_order = Order(price, vol, player, order_type)
            self.orders[neworder.order_type].remove(similar_order[0])
            self.orders[neworder.order_type].append(updated_order)

        # todo on buy check if offer price is higher than current price = instant buy
        # todo      if lower price put in buy_orders

        # todo maybe change input to keywords
        # todo add_buy_order(self, price=100, volume=10, player='NPC')

        # todo maybe change to dict id : (price, vol, player) ... might be better for keeping track
        # todo maybe change to dict (price, player) : vol ... easy to find values


    def player_similar_order(self, Order):
        return [match for match in self.orders[Order.order_type]
                if (match.price == Order.price) and (match.player == Order.player)]


    # todo on sell check if offer price is lower than current price = instant sell
    # todo      if higher put in sell_orders

    # todo loop to match if there is buy orders matching
    # todo loop to match if there is sell orders matching

    # todo trending? daily/week high/low?


    def remove_buy_order(self, order):
        #todo need updating to new namedtuple format
        if order in self.buy_orders:
            self.buy_orders.remove(order)

    def player_buy_orders(self, player):
        # todo need updating to new namedtuple format
        return [order for order in self.buy_orders if order[2] == player]

    def player_similar_buy_order(self, neworder):
        # todo need updating to new namedtuple format
        price, volume, player = neworder
        return [order for order in self.player_buy_orders(player) if order[0] == price]

    # todo player cancle order
    # todo player modify order

    # split order method needed? maybe not if buy orders always take the player credit in escrow
    # might only be needed if there is support for buy under current price or sell over current price between players

    # if price == 0 -> out of buisness -> remove from market?

    # stock price history
    # logging?

    # split, only needed if I implement limited number of shares


class TestStock(unittest.TestCase):
    def setUp(self):
        self.teststock = Stock('testStock', 1000)
        # price, volume, player
        self.buyorder = Order(100, 1, 'NPC', 'buy')
        self.sellorder = Order(100, 1, 'NPC', 'buy')

    def test_create_stock(self):
        self.assertEqual(self.teststock.name, 'testStock') and self.assertEqual(self.teststock.price, 1000)
        self.assertEqual((self.teststock.name, self.teststock.price), ('testStock', 1000))
        print('test_create_stock passed.')

    def test_alterprice(self):
        self.teststock.price = 1200
        self.assertEqual(self.teststock.price, 1200)
        print('test_alterprice passed.')

    def test_add_order(self):
        #setup
        self.teststock.add_order(Order(100, 5, 'NPC', 'buy'))
        self.teststock.add_order(Order(200, 5, 'NPC', 'buy'))
        self.teststock.add_order(Order(100, 5, 'Neptun', 'buy'))
        self.teststock.add_order(Order(100, 1, 'NPC', 'buy'))
        #checks
        self.valid_new_order = Order(100, 6, 'NPC', 'buy')
        self.assertIn(self.valid_new_order, self.teststock.orders['buy'])
        self.assertIn(Order(200, 5, 'NPC', 'buy'), self.teststock.orders['buy'])
        self.assertIn(Order(100, 5, 'Neptun', 'buy'), self.teststock.orders['buy'])
        self.assertNotIn(Order(100, 5, 'NPC', 'buy'), self.teststock.orders['buy'])
        self.assertNotIn(Order(100, 1, 'NPC', 'buy'), self.teststock.orders['buy'])





    def test_add_buy_order(self):
        # todo need updating to new namedtuple format
        self.teststock.add_buy_order(self.order)
        self.assertIn(self.order, self.teststock.buy_orders)
        print('test_add_buy_order passed.')

    def test_player_buy_orders(self):
        # todo need updating to new namedtuple format
        order = (100, 1, 'NPC')
        self.teststock.add_buy_order(self.order)
        self.assertIn(self.order, self.teststock.player_buy_orders(order[2]))
        print('test_player_buy_orders passed.')

    def test_player_similar_buy_order(self):
        # todo need updating to new namedtuple format
        teststock = Stock('testStock', 1000)
        existing_order = (100, 5, 'NPC')
        existing_order2 = (200, 5, 'NPC')
        existing_order3 = (100, 5, 'Neptun')
        new_order = (100, 1, 'NPC')
        teststock.add_buy_order(existing_order)
        self.assertIn(existing_order, teststock.buy_orders)
        teststock.add_buy_order(existing_order2)
        self.assertIn(existing_order2, teststock.buy_orders)
        teststock.add_buy_order(existing_order3)
        self.assertIn(existing_order3, teststock.buy_orders)
        self.assertIn(existing_order, teststock.player_similar_buy_order(new_order))
        print('test_player_similar_buy_order passed.')

    def test_player_similar_buy_order2(self):
        # todo need updating to new namedtuple format
        existing_order = (100, 5, 'NPC')
        existing_order2 = (200, 5, 'NPC')
        existing_order3 = (100, 5, 'Neptun')
        new_order = (100, 1, 'Neptun')
        self.teststock.add_buy_order(existing_order)
        self.assertIn(existing_order, self.teststock.buy_orders)
        self.teststock.add_buy_order(existing_order2)
        self.assertIn(existing_order2, self.teststock.buy_orders)
        self.teststock.add_buy_order(existing_order3)
        self.assertIn(existing_order3, self.teststock.buy_orders)
        self.assertIn(existing_order3, self.teststock.player_similar_buy_order(new_order))
        print('test_player_similar_buy_order2 passed.')

    def test_add_duplicate_buy_order(self):
        # todo need updating to new namedtuple format
        self.teststock.add_buy_order(self.order)
        self.teststock.add_buy_order(self.order)
        self.assertIn((100, 2, 'NPC'), self.teststock.buy_orders)
        self.assertTrue(len(self.teststock.buy_orders) == 1)
        print('test_add_duplicate_buy_orders passed.')

    def test_remove_buy_order(self):
        # todo need updating to new namedtuple format
        self.teststock.add_buy_order(self.order)
        self.assertIn(self.order, self.teststock.buy_orders)
        self.teststock.remove_buy_order(self.order)
        self.assertNotIn(self.order, self.teststock.buy_orders)
        self.assertTrue(len(self.teststock.buy_orders) == 0)
        print('test_remove_buy_order passed.')

    def test_add_1337_similar_orders(self):
        # todo need updating to new namedtuple format
        bigorder = (100, 1337, 'NPC')
        for i in range(1337):
            self.teststock.add_buy_order(self.order)
        self.assertIn(bigorder, self.teststock.buy_orders)
        print('test_add_1337_similar_orders passed.')

    def test_add_sell_order(self):
        pass
        print('test_add_sell_order passed.')

    def test_update_low_high_price(self):
        pass
        print('test_update_low_high_price passed.')

    def test_process_orders(self):
        pass
        print('test_process_orders passed.')

if __name__ == '__main__':
    unittest.main()


