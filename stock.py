#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest
import logging
from helpers import Order


class Stock:
    def __init__(self, name, price):
        self.name = name
        self.price = price  # Trending?
        self.high_price = price  # daily, alltime?
        self.low_price = price  # daily, alltime?
        self.orders = {'buy': [], 'sell': []}  # hmmm set or list????

    def add_order(self, neworder):
        # todo on buy check if offer price is higher than current price = instant buy
        # todo      if lower price put in buy_orders

        # todo on sell check if offer price is lower than current price = instant sell
        # todo      if higher put in sell_orders
        similar_order = self.list_similar_player_order(neworder)

        if not similar_order:
            self.orders[neworder.order_type].append(neworder)
        else:
            # update similar order
            current_volume = similar_order[0].vol
            price, vol, player, order_type = neworder
            vol += current_volume
            updated_order = Order(price, vol, player, order_type)
            self.orders[neworder.order_type].remove(similar_order[0])
            self.orders[neworder.order_type].append(updated_order)

    def list_similar_player_order(self, order):
        return [match for match in self.orders[order.order_type]
                if (match.price == order.price) and (match.player == order.player)]

    def list_player_buy_orders(self, player):
        return [match for match in self.orders['buy'] if match.player == player]

    def list_player_sell_orders(self, player):
        return [match for match in self.orders['sell'] if match.player == player]

    def remove_order(self, order):
        if order in self.orders[order.order_type]:
            self.orders[order.order_type].remove(order)
            # todo if buy order require full buy amount to be put in escrow refund money to player
            # todo if sell order return stocks to player's portfolio
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

    def process_orders(self):
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

        # todo match buy with sell orders?

    def update_low_high_price(self):
        if self.price > self.high_price:
            self.high_price = self.price
        if self.price < self.low_price:
            self.low_price = self.price

    # todo split, only needed if I implement limited number of shares?
    # todo split order method needed? maybe not if buy orders always take the player credit in escrow
    # might only be needed if there is support for buy under current price or sell over current price between players
    # or if there is a limited supply/demand

    # todo stock price history?
    # todo logging?

    # todo if price == 0 -> out of buisness -> remove from market? Might be more suited in the Market class.


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
        teststock.add_order(buyorder)
        teststock.add_order(sellorder)
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

    def test_create_stock(self):
        self.assertEqual(self.teststock.name, 'testStock') and self.assertEqual(self.teststock.price, 1000)
        self.assertEqual((self.teststock.name, self.teststock.price), ('testStock', 1000))
        print('test_create_stock passed.')

    def test_alterprice(self):
        self.teststock.price = 1200
        self.assertEqual(self.teststock.price, 1200)
        print('test_alterprice passed.')

    def test_add_order(self):
        # setup
        self.teststock.add_order(Order(100, 5, 'NPC', 'buy'))
        self.teststock.add_order(Order(200, 5, 'NPC', 'buy'))
        self.teststock.add_order(Order(100, 5, 'Neptun', 'buy'))
        self.teststock.add_order(Order(100, 1, 'NPC', 'buy'))
        # checks
        self.valid_new_order = Order(100, 6, 'NPC', 'buy')
        self.assertIn(self.valid_new_order, self.teststock.orders['buy'])
        self.assertIn(Order(200, 5, 'NPC', 'buy'), self.teststock.orders['buy'])
        self.assertIn(Order(100, 5, 'Neptun', 'buy'), self.teststock.orders['buy'])
        self.assertNotIn(Order(100, 5, 'NPC', 'buy'), self.teststock.orders['buy'])
        self.assertNotIn(Order(100, 1, 'NPC', 'buy'), self.teststock.orders['buy'])
        print('test_add_order passed.')

    def test_add_buy_order(self):
        self.teststock.add_order(self.buyorder)
        self.assertIn(self.buyorder, self.teststock.orders['buy'])
        print('test_add_buy_order passed.')

    def test_add_sell_order(self):
        self.teststock.add_order(self.sellorder)
        self.assertIn(self.sellorder, self.teststock.orders['sell'])
        print('test_add_sell_order passed.')

    def test_list_player_buy_orders(self):
        self.teststock.add_order(self.sellorder)
        self.assertNotIn(self.sellorder, self.teststock.list_player_buy_orders(self.sellorder.player))
        self.teststock.add_order(self.buyorder)
        self.assertIn(self.buyorder, self.teststock.list_player_buy_orders(self.buyorder.player))
        print('test_list_player_buy_orders passed.')

    def test_list_player_sell_orders(self):
        self.teststock.add_order(self.buyorder)
        self.assertNotIn(self.buyorder, self.teststock.list_player_sell_orders(self.sellorder.player))
        self.teststock.add_order(self.sellorder)
        self.assertIn(self.sellorder, self.teststock.list_player_sell_orders(self.buyorder.player))
        print('test_list_player_buy_orders passed.')

    def test_list_similar_player_buy_order(self):
        existing_order = Order(100, 5, 'NPC', 'buy')
        existing_order2 = Order(200, 5, 'NPC', 'buy')
        existing_order3 = Order(100, 5, 'Neptun', 'buy')
        new_order = Order(100, 1, 'NPC', 'buy')
        self.teststock.add_order(existing_order)
        self.assertIn(existing_order, self.teststock.orders['buy'])
        self.teststock.add_order(existing_order2)
        self.assertIn(existing_order2, self.teststock.orders['buy'])
        self.teststock.add_order(existing_order3)
        self.assertIn(existing_order3, self.teststock.orders['buy'])
        self.assertIn(existing_order, self.teststock.list_similar_player_order(new_order))
        self.assertNotIn(existing_order3, self.teststock.list_similar_player_order(new_order))
        print('test_player_similar_buy_order passed.')

    def test_add_duplicate_buy_order(self):
        self.teststock.add_order(self.buyorder)
        self.teststock.add_order(self.buyorder)
        duplicate_order = Order(100, 2, 'NPC', 'buy')
        self.assertIn(duplicate_order, self.teststock.orders['buy'])
        self.assertTrue(len(self.teststock.orders['buy']) == 1)
        print('test_add_duplicate_buy_orders passed.')

    def test_remove_buy_order(self):
        self.teststock.add_order(self.buyorder)
        self.assertIn(self.buyorder, self.teststock.orders['buy'])
        self.teststock.remove_order(self.buyorder)
        self.assertNotIn(self.buyorder, self.teststock.orders['buy'])
        self.assertTrue(len(self.teststock.orders['buy']) == 0)
        print('test_remove_buy_order passed.')

    def test_add_1337_similar_orders(self):
        # todo need updating to new namedtuple format
        bigorder = Order(100, 1337, 'NPC', 'buy')
        for i in range(1337):
            self.teststock.add_order(self.buyorder)
        self.assertIn(bigorder, self.teststock.orders['buy'])
        print('test_add_1337_similar_orders passed.')

    def test_update_low_high_price(self):
        self.teststock.price = 1000
        self.assertEqual(self.teststock.price, 1000)
        self.teststock.update_low_high_price()
        self.assertEqual(self.teststock.price, 1000)
        self.assertEqual(self.teststock.high_price, 1000)
        self.assertEqual(self.teststock.low_price, 1000)
        self.teststock.price = 1100
        self.teststock.update_low_high_price()
        self.assertEqual(self.teststock.price, 1100)
        self.assertEqual(self.teststock.high_price, 1100)
        self.assertEqual(self.teststock.low_price, 1000)
        self.teststock.price = 900
        self.teststock.update_low_high_price()
        self.assertEqual(self.teststock.price, 900)
        self.assertEqual(self.teststock.high_price, 1100)
        self.assertEqual(self.teststock.low_price, 900)
        self.teststock.price = 1000
        self.teststock.update_low_high_price()
        self.assertEqual(self.teststock.price, 1000)
        self.assertEqual(self.teststock.high_price, 1100)
        self.assertEqual(self.teststock.low_price, 900)
        print('test_update_low_high_price passed.')

if __name__ == '__main__':
    unittest.main()


