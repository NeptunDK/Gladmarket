#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest


class Stock:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.high_price = price
        self.low_price = price
        self.buy_orders = set() # todo list or ordered to ensure first buy order gets matched first FIFO
        self.sell_orders = set() # todo list or ordered to ensure first buy order gets matched first FIFO

    # todo add wrapping method to switch between buy/sell

    # todo on sell check if offer price is higher than current price = instant sell
    # todo      if lower put in sell_orders

    # todo loop to match if there is buy and sell orders matching

    # todo trending? daily/week high/low?

    def add_buy_order(self, neworder):
        # price, volume, player

        # todo on buy check if offer price is lower than current price = instant buy
        # todo      if higher put in buy_orders

        #todo maybe change input to keywords
        #todo add_buy_order(self, price=100, volume=10, player='NPC')

        similar_order = self.player_similar_buy_order(neworder)
        if not similar_order:
            self.buy_orders.add(neworder)
        else:
            _, new_volume, _ = neworder
            price, volume, player = similar_order[0]
            updated_order = price, volume + new_volume, player
            self.remove_buy_order(similar_order[0])
            self.buy_orders.add(updated_order)

    def remove_buy_order(self, order):
        if order in self.buy_orders:
            self.buy_orders.remove(order)

    def player_buy_orders(self, player):
        return [order for order in self.buy_orders if order[2] == player]

    def player_similar_buy_order(self, neworder):
        price, volume, player = neworder
        return [order for order in self.player_buy_orders(player) if order[0] == price]

    # if price == 0 -> out of buisness -> remove from market?

    # stock price history
    # logging?

    # split


class TestStock(unittest.TestCase):
    def setUp(self):
        self.teststock = Stock('testStock', 1000)
        #price, volume, player
        self.order = (100, 1, 'NPC')

    def test_create_stock(self):
        self.assertEqual(self.teststock.name, 'testStock') and self.assertEqual(self.teststock.price, 1000)
        self.assertEqual((self.teststock.name, self.teststock.price), ('testStock', 1000))
        print('test_create_stock passed.')

    def test_alterprice(self):
        self.teststock.price = 1200
        self.assertEqual(self.teststock.price, 1200)
        print('test_alterprice passed.')

    def test_add_buy_order(self):
        self.teststock.add_buy_order(self.order)
        self.assertIn(self.order, self.teststock.buy_orders)
        print('test_add_buy_order passed.')

    def test_player_buy_orders(self):
        order = (100, 1, 'NPC')
        self.teststock.add_buy_order(self.order)
        self.assertIn(self.order, self.teststock.player_buy_orders(order[2]))
        print('test_player_buy_orders passed.')

    def test_player_similar_buy_order(self):
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
        self.teststock.add_buy_order(self.order)
        self.teststock.add_buy_order(self.order)
        self.assertIn((100, 2, 'NPC'), self.teststock.buy_orders)
        print('test_add_duplicate_buy_orders passed.')

    def test_remove_buy_order(self):
        self.teststock.add_buy_order(self.order)
        self.assertIn(self.order, self.teststock.buy_orders)
        self.teststock.remove_buy_order(self.order)
        self.assertNotIn(self.order, self.teststock.buy_orders)
        print('test_remove_buy_order passed.')

    def test_add_1337_similar_orders(self):
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


