#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest
import logging
from helpers import Order, gen_random_order
import random


class Stock:
    def __init__(self, name, price):
        self.name = name
        self.price = price  # todo Trending?
        self.high_price = price  # todo do intervals like last hour/daily?
        self.low_price = price  # todo do intervals like last hour/daily?
        self.orders = {'buy': [], 'sell': []}
        # todo orderID, added to Order namedtuple?

    def __repr__(self):
        return f"{self.name} @ {self.price}"

    def place_order(self, order):
        if order.order_type == 'buy' and self.price <= order.price:
            logging.info(f"{order.player} bought {order.vol} shares of {self.name} "
                            f"for a price of {order.price} each, total of {order.vol * order.price}.")
            return True
        elif order.order_type == 'sell' and self.price >= order.price:
            logging.info(f"{order.player} sold {order.vol} shares of {self.name} "
                            f"for a price of {order.vol * order.price}.")
            return True
        else:
            self.add_order_to_escrow(order)
            return False

    def add_order_to_escrow(self, order):
        similar_order = self.list_similar_player_order(order)

        if not similar_order:
            self.orders[order.order_type].append(order)
            logging.info(f"{order} added.")
        else:
            # update similar order
            current_volume = similar_order[0].vol
            player, order_type, vol, stockname, price = order
            vol += current_volume
            updated_order = Order(player, order_type, vol, stockname, price)
            self.orders[order.order_type].remove(similar_order[0])
            self.orders[order.order_type].append(updated_order)
            logging.info(f"{order} combined with old oder: {similar_order[0]} into: {updated_order}.")

    def list_similar_player_order(self, order):
        return [match for match in self.orders[order.order_type]
                if (match.price == order.price) and (match.player == order.player)]

    def list_player_buy_orders(self, player):
        return [match for match in self.orders['buy'] if match.player == player]

    def list_player_sell_orders(self, player):
        return [match for match in self.orders['sell'] if match.player == player]

    def list_buy_orders(self):
        return self.orders['buy']

    def list_sell_orders(self):
        return self.orders['sell']

    def match_orders(self):
        matched_orders = []  # todo better off being self.matched_orders?

        # buy orders matching current stock price or higher
        for buy_order in self.orders['buy']:
            if buy_order.price >= self.price:
                logging.info(f"{buy_order} matched price of: {self.price}")
                matched_orders.append(buy_order)

        # sell orders matching current stock price or lower
        for sell_order in self.orders['sell']:
            if sell_order.price <= self.price:
                logging.info(f"{sell_order} matched price of: {self.price}")
                matched_orders.append(sell_order)

        for order in matched_orders:
            if order.order_type == 'buy' and order in self.orders['buy']:
                self.orders['buy'].remove(order)
            if order.order_type == 'sell' and order in self.orders['sell']:
                self.orders['sell'].remove(order)
        return matched_orders  # todo update player credit/portfolio

    def cancel_order(self, order):
        # this can't be in match_orders as a canceled buy order returns credits to player
        # and canceled sell order returns shares to player
        # todo if buy order is canceled return credit to player
        # todo if sell order is canceled return shares to player's portfolio
        if order in self.orders[order.order_type]:
            self.orders[order.order_type].remove(order)
            logging.info(f"{order} cancelled.")
            return True
        else:
            logging.warning(f"{order} not found!")
            return False

    def update_low_high_price(self):
        if self.price > self.high_price:
            self.high_price = self.price
        if self.price < self.low_price:
            self.low_price = self.price

    def ranwalk_price(self):
        # todo not sure yet if it should be here or in the market class
        # todo unittest
        pass

    # todo if price == 0 -> out of buisness -> remove from market? Might be more suited in the Market class.
    # todo stock price history?
    # todo logging?

    # todo split, only needed if I implement limited number of shares?
    # todo split order method needed? maybe not if buy orders always take the player credit in escrow
    # might only be needed if there is support for buy under current price or sell over current price between players
    # or if there is a limited supply/demand


class TestStock(unittest.TestCase):
    def setUp(self):
        self.teststock = Stock('Teststock', 1000)
        # price, volume, player, type
        self.buyorder = Order('NPC', 'buy', 1, 'Teststock', 100)
        self.buyorder_two = Order('NPC', 'buy', 1, 'Teststock', 1100)
        self.sellorder = Order('NPC', 'sell', 1, 'Teststock', 100)
        self.sellorder_two = Order('NPC', 'sell', 1, 'Teststock', 1100)

    def test_create_stock(self):
        self.assertEqual(self.teststock.name, 'Teststock') and self.assertEqual(self.teststock.price, 1000)
        self.assertEqual((self.teststock.name, self.teststock.price), ('Teststock', 1000))
        print('test_create_stock passed.')

    def test___repr__(self):
        self.assertEqual(repr(self.teststock), 'Teststock @ 1000')
        print('test___repr__ passed.')

    def test_alterprice(self):
        self.teststock.price = 1200
        self.assertEqual(self.teststock.price, 1200)
        print('test_alterprice passed.')

    def test_place_order_buy(self):
        self.assertTrue(self.teststock.place_order(Order('NPC', 'buy', 1, 'Teststock', 1000)))
        self.assertTrue(self.teststock.place_order(Order('NPC', 'buy', 1, 'Teststock', 1100)))
        self.assertFalse(self.teststock.place_order(Order('NPC', 'buy', 1, 'Teststock', 100)))
        self.assertIn(Order('NPC', 'buy', 1, 'Teststock', 100), self.teststock.list_buy_orders())
        print('test_place_order_buy passed.')

    def test_place_order_sell(self):
        self.assertTrue(self.teststock.place_order(Order('NPC', 'sell', 1, 'Teststock', 1000)))
        self.assertTrue(self.teststock.place_order(Order('NPC', 'sell', 1, 'Teststock', 100)))
        self.assertFalse(self.teststock.place_order(Order('NPC', 'sell', 1, 'Teststock', 1100)))
        self.assertIn(Order('NPC', 'sell', 1, 'Teststock', 1100), self.teststock.list_sell_orders())
        print('test_place_order_sell passed.')

    def test_add_order(self):
        # setup
        self.teststock.add_order_to_escrow(Order('NPC', 'buy', 5, 'Teststock', 100))
        self.teststock.add_order_to_escrow(Order('NPC', 'buy', 5, 'Teststock', 200))
        self.teststock.add_order_to_escrow(Order('Neptun', 'buy', 5, 'Teststock', 100))
        self.teststock.add_order_to_escrow(Order('NPC', 'buy', 1, 'Teststock', 100))
        # checks
        self.valid_new_order = Order('NPC', 'buy', 6, 'Teststock', 100)
        self.assertIn(self.valid_new_order, self.teststock.orders['buy'])
        self.assertIn(Order('NPC', 'buy', 5, 'Teststock', 200), self.teststock.orders['buy'])
        self.assertIn(Order('Neptun', 'buy', 5, 'Teststock', 100), self.teststock.orders['buy'])
        self.assertNotIn(Order('NPC', 'buy', 5, 'Teststock', 100), self.teststock.orders['buy'])
        self.assertNotIn(Order('NPC', 'buy', 1, 'Teststock', 100), self.teststock.orders['buy'])
        print('test_add_order passed.')

    def test_add_buy_order(self):
        self.teststock.add_order_to_escrow(self.buyorder)
        self.assertIn(self.buyorder, self.teststock.orders['buy'])
        print('test_add_buy_order passed.')

    def test_add_sell_order(self):
        self.teststock.add_order_to_escrow(self.sellorder)
        self.assertIn(self.sellorder, self.teststock.orders['sell'])
        print('test_add_sell_order passed.')

    def test_list_player_buy_orders(self):
        self.teststock.add_order_to_escrow(self.sellorder)
        self.assertNotIn(self.sellorder, self.teststock.list_player_buy_orders(self.sellorder.player))
        self.teststock.add_order_to_escrow(self.buyorder)
        self.assertIn(self.buyorder, self.teststock.list_player_buy_orders(self.buyorder.player))
        print('test_list_player_buy_orders passed.')

    def test_list_player_sell_orders(self):
        self.teststock.add_order_to_escrow(self.buyorder)
        self.assertNotIn(self.buyorder, self.teststock.list_player_sell_orders(self.sellorder.player))
        self.teststock.add_order_to_escrow(self.sellorder)
        self.assertIn(self.sellorder, self.teststock.list_player_sell_orders(self.buyorder.player))
        print('test_list_player_buy_orders passed.')

    def test_list_similar_player_buy_order(self):
        existing_order = Order('NPC', 'buy', 5, 'IBM', 100)
        existing_order2 = Order('NPC', 'buy', 5, 'IBM', 200)
        existing_order3 = Order('Neptun', 'buy', 5, 'IBM', 100)
        new_order = Order('NPC', 'buy', 1, 'IBM', 100)
        self.teststock.add_order_to_escrow(existing_order)
        self.assertIn(existing_order, self.teststock.orders['buy'])
        self.teststock.add_order_to_escrow(existing_order2)
        self.assertIn(existing_order2, self.teststock.orders['buy'])
        self.teststock.add_order_to_escrow(existing_order3)
        self.assertIn(existing_order3, self.teststock.orders['buy'])
        self.assertIn(existing_order, self.teststock.list_similar_player_order(new_order))
        self.assertNotIn(existing_order3, self.teststock.list_similar_player_order(new_order))
        print('test_player_similar_buy_order passed.')

    def test_add_duplicate_buy_order(self):
        self.teststock.add_order_to_escrow(self.buyorder)
        self.teststock.add_order_to_escrow(self.buyorder)
        duplicate_order = Order('NPC', 'buy', 2, 'Teststock', 100)
        self.assertIn(duplicate_order, self.teststock.orders['buy'])
        self.assertTrue(len(self.teststock.orders['buy']) == 1)
        print('test_add_duplicate_buy_orders passed.')

    def test_cancel_order(self):
        self.teststock.add_order_to_escrow(self.buyorder)
        self.assertIn(self.buyorder, self.teststock.orders['buy'])
        self.teststock.cancel_order(self.buyorder)
        self.assertNotIn(self.buyorder, self.teststock.orders['buy'])
        self.assertTrue(len(self.teststock.orders['buy']) == 0)
        print('test_cancel_order passed.')

    def test_add_1337_similar_orders(self):
        bigorder = Order('NPC', 'buy', 1337, 'Teststock', 100)
        for i in range(1337):
            self.teststock.add_order_to_escrow(self.buyorder)
        self.assertIn(bigorder, self.teststock.orders['buy'])
        self.assertEqual(len(self.teststock.orders['buy']), 1)
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

    def test_match_orders(self):
        # todo
        # todo add Player class instance, to test credit/portfolio updates,
        # or maybe have that part in a different test/class
        self.assertEqual(self.teststock.price, 1000)
        buyorder = Order('NPC', 'buy', 1, 'Teststock', 900)
        sellorder = Order('NPC', 'sell', 1, 'Teststock', 1100)
        self.teststock.add_order_to_escrow(buyorder)
        self.teststock.add_order_to_escrow(sellorder)
        self.teststock.match_orders()
        self.assertIn(buyorder, self.teststock.orders['buy'])
        self.assertIn(sellorder, self.teststock.orders['sell'])
        self.teststock.price = 900
        self.assertEqual(self.teststock.price, 900)
        self.teststock.match_orders()
        self.assertNotIn(buyorder, self.teststock.orders['buy'])
        self.assertIn(sellorder, self.teststock.orders['sell'])
        self.teststock.price = 1100
        self.assertEqual(self.teststock.price, 1100)
        self.teststock.match_orders()
        self.assertNotIn(buyorder, self.teststock.orders['buy'])
        self.assertNotIn(sellorder, self.teststock.orders['sell'])
        print('test_match_orders passed.')

    def test_match_orders_sellorders_not_empty(self):
        random.seed(1337)  # really important!
        teststock = Stock('DELL', 9)

        for e in range(14):
            teststock.place_order(gen_random_order(stockname=teststock.name))

        self.assertIn(Order(player='NPC', order_type='sell', vol=10, stockname='DELL', price=10),
                      teststock.list_sell_orders())

        self.assertIn(Order(player='Player2', order_type='sell', vol=1, stockname='DELL', price=10),
                      teststock.list_sell_orders())

        teststock.price = 10
        self.assertEqual(teststock.price, 10)
        teststock.match_orders()
        self.assertNotIn(Order(player='Player2', order_type='sell', vol=1, stockname='DELL', price=10), teststock.list_sell_orders())
        # print('buy10:', teststock.orders)

        teststock.price = 7
        self.assertEqual(teststock.price, 7)
        teststock.match_orders()
        self.assertIn(Order(player='NPC', order_type='buy', vol=6, stockname='DELL', price=2), teststock.orders['buy'])
        # print('buy7', teststock.orders)

        teststock.price = 4
        self.assertEqual(teststock.price, 4)
        teststock.match_orders()
        self.assertIn(Order(player='NPC', order_type='buy', vol=6, stockname='DELL', price=2), teststock.orders['buy'])
        # print('buy4', teststock.orders)

        teststock.price = 2
        self.assertEqual(teststock.price, 2)
        teststock.match_orders()
        self.assertNotIn(Order(player='NPC', order_type='buy', vol=6, stockname='DELL', price=2), teststock.orders['buy'])
        # print('buy2', teststock.orders)
        print('test_match_orders_sellorders_not_empty passed.')

if __name__ == '__main__':
    unittest.main()
