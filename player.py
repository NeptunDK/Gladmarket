#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest
from helpers import Order
import logging
from operator import attrgetter


class Player:  # could also be called wallet, then a player/firm/company/bot could have a wallet
    def __init__(self, name, starting_credits=10000, description=None):
        self.name = name
        self.description = description
        self.credit = starting_credits
        self.portfolio = []
        self.networth = self.credit
        self.salary = 5000

    def __repr__(self):
        return f"{self.name} has {self.credit} GladCoins, and is worth {self.networth}."

    def add_salary(self):
        # is it safe to have this here?
        self.credit += self.salary
        self.networth += self.salary

    def add_to_portfolio(self, order):
        similar = self.list_similar(order)

        if not similar:
            self.portfolio.append(order)
        else:
            new_volume = similar[0].vol + order.vol
            updated_order = Order(order.player, order.order_type, new_volume, order.stockname, order.price)
            self.portfolio.remove(similar[0])
            self.portfolio.append(updated_order)
            logging.info(f"New order: {order} combined with old: {similar[0]} into: {updated_order}.")

    def remove_from_portfolio(self, order):
        if order in self.portfolio:
            self.portfolio.remove(order)
            logging.info(f"{order} removed from portfolio.")
        else:
            similar = self.list_similar(order)[0]
            neworder = Order(order.player, order.order_type, similar.vol - order.vol, order.stockname, order.price)
            self.portfolio[self.portfolio.index(similar)] = neworder
            logging.info(f"{similar} updated to {neworder} in portfolio.")

    def list_similar(self, order):
        return [match for match in self.portfolio
                if (match.stockname == order.stockname) and (match.price == order.price)]

    def sort_portfolio(self):
        self.portfolio = sorted(self.portfolio, key=attrgetter('vol'), reverse=True)  # secondary key
        self.portfolio = sorted(self.portfolio, key=attrgetter('stockname',))  # primary key

    def flatten_portfolio(self):
        # Ignores price to remove clutter
        new_portfolio = self.portfolio
        self.portfolio = []

        for order in new_portfolio:
            self.add_to_portfolio(Order(order.player, order.order_type, order.vol, order.stockname, 0))

    def list_portfolio(self):
        # todo sort? (self, sortkey=None)
        # todo support amount?(self, amount=None)
        return self.portfolio

    # sell stocks/shares
    # on the market instead?

    # purchase/selling history here or somewhere else?
    # self.transactions_log

    # out of buisness / game over / start over

    # login
    # save/load user
    # todo is this the correct place?


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.testplayer = Player('Player1', 10000, 'Is only a test.')
        self.buyorder = Order('player1', 'buy', 1, 'Teststock', 100)

    def test_player(self):
        self.assertEqual(self.testplayer.name, 'Player1')
        self.assertEqual(self.testplayer.description, 'Is only a test.')
        self.assertEqual(self.testplayer.credit, 10000)
        self.assertListEqual(self.testplayer.portfolio, [])
        print('test_player passed.')

    def test___repr__(self):
        print(self.testplayer)
        self.assertEqual(f'{self.testplayer.name} has {self.testplayer.credit} GladCoins, '
                         f'and is worth {self.testplayer.networth}.', repr(self.testplayer))
        print('test___repr__ passed.')


    def test_add_sallery(self):
        self.testplayer.add_salary()
        self.assertEqual(self.testplayer.credit, 15000)
        self.testplayer.credit += 4000
        self.assertEqual(self.testplayer.credit, 19000)
        print('test_add_sallery passed.')

    def test_add_to_portfolio(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_to_portfolio(self.buyorder)
        self.assertIn(self.buyorder, self.testplayer.portfolio)
        self.testplayer.add_to_portfolio(self.buyorder)
        combined = Order('player1', 'buy', 2, 'Teststock', 100)
        self.assertIn(combined, self.testplayer.portfolio)
        print('test_add_to_portfolio passed.')

    def test_add_to_portfolio2(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 1, 'DELL', 1000))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 8, 'DELL', 1000))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 1, 'DELL', 5000))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 1, 'DELL', 1000))
        print('name')
        print(self.testplayer.portfolio)
        self.assertIn(Order('player1', 'buy', 10, 'DELL', 1000), self.testplayer.portfolio)
        self.assertIn(Order('player1', 'buy', 1, 'DELL', 5000), self.testplayer.portfolio)
        print('test_add_to_portfolio2 passed.')

    def test_list_similar(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.portfolio.append(self.buyorder)
        self.assertIn(self.buyorder, self.testplayer.portfolio)
        self.assertEqual([self.buyorder], self.testplayer.list_similar(self.buyorder))
        print('test_list_similar passed.')

    def test_remove_from_portfolio(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_to_portfolio(self.buyorder)
        self.assertIn(self.buyorder, self.testplayer.portfolio)
        self.testplayer.remove_from_portfolio(self.buyorder)
        self.assertNotIn(self.buyorder, self.testplayer.portfolio)
        combined = Order('player1', 'buy', 2, 'Teststock', 100)
        self.testplayer.add_to_portfolio(combined)
        self.assertIn(combined, self.testplayer.portfolio)
        self.testplayer.remove_from_portfolio(self.buyorder)
        self.assertIn(self.buyorder, self.testplayer.portfolio)
        print('test_remove_from_portfolio passed.')

    def test_list_portfolio(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_to_portfolio(self.buyorder)
        self.assertIn(self.buyorder, self.testplayer.portfolio)
        print(self.testplayer.list_portfolio()[0])
        print('test_list_portfolio passed.')

    def test_sort_portfolio(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 3, 'IBM', 150))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 2, 'IBM', 75))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 1, 'DELL', 1000))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 8, 'DELL', 1000))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 1, 'DELL', 5000))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 1, 'DELL', 1000))
        self.assertIn(Order('player1', 'buy', 3, 'IBM', 150), self.testplayer.portfolio)
        self.assertIn(Order('player1', 'buy', 2, 'IBM', 75), self.testplayer.portfolio)
        self.assertIn(Order('player1', 'buy', 10, 'DELL', 1000), self.testplayer.portfolio)
        self.assertIn(Order('player1', 'buy', 1, 'DELL', 5000), self.testplayer.portfolio)
        self.testplayer.sort_portfolio()
        self.assertEqual([Order('player1', 'buy', 10, 'DELL', 1000),
                          Order('player1', 'buy', 1, 'DELL', 5000),
                          Order('player1', 'buy', 3, 'IBM', 150),
                          Order('player1', 'buy', 2, 'IBM', 75)], self.testplayer.portfolio)
        print('test_sort_portfolio passed.')

    def test_flatten_portfolio(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 3, 'IBM', 150))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 2, 'IBM', 75))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 1, 'DELL', 1000))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 8, 'DELL', 1000))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 1, 'DELL', 5000))
        self.testplayer.add_to_portfolio(Order('player1', 'buy', 1, 'DELL', 1000))
        self.testplayer.flatten_portfolio()
        self.assertIn(Order('player1', 'buy', 11, 'DELL', 0), self.testplayer.portfolio)
        self.assertIn(Order('player1', 'buy', 5, 'IBM', 0), self.testplayer.portfolio)
        print('test_flatten_portfolio passed.')

if __name__ == '__main__':
    unittest.main()
