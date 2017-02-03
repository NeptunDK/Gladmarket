#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest
from stock import Stock
from helpers import Order, Share, convert_to_share
import logging

class Player:
    def __init__(self, name, starting_credits, description = None):
        self.name = name
        self.description = description
        self.credit = starting_credits
        self.portfolio = []  # Share = namedtuple('Share', ['stockname', 'vol', 'buyprice'])
        self.networth = None # todo
        self.salary = 5000

    def add_salary(self):
        # todo is it safe to have this here?
        self.credit += self.salary

    def add_share_to_portfolio(self, stock, order):
        # todo need check to see if player actually bought the stock?
        share = convert_to_share(stock, order)
        if share not in self.portfolio:
            self.portfolio.append(share)
        else:
            share_in_portfolio = self.list_similar_share(share)[0]
            newshare = Share(share.stockname, share.vol + share_in_portfolio.vol, share.buyprice)
            self.portfolio[self.portfolio.index(share_in_portfolio)] = newshare

    def remove_shares_from_portfolio(self, share):
        # todo should it be (self, stock, share) and use the convert to share like add_share_to_portfolio?
        if share in self.portfolio:
            self.portfolio.remove(share)
            logging.warning(f"{share} removed from portfolio.")
        else:
            similar_share = self.list_similar_share(share)[0]
            print('similar_share', similar_share)
            newshare = Share(share.stockname, similar_share.vol - share.vol, share.buyprice)
            self.portfolio[self.portfolio.index(similar_share)] = newshare
            logging.warning(f"{similar_share} updated to {newshare} in portfolio.")

    def list_similar_share(self, share):
        return [match for match in self.portfolio
                if (match.stockname == share.stockname) and (match.buyprice == share.buyprice)]

    def sort_portfolio(self):
        # todo choose sorting key, stockname, volume, price, value
        pass

    def combine_portfolio_shares(self):
        # todo combine
        pass

    # list shares

    # sell stocks

    # purchase/selling history here or somewhere else?

    # out of buisness / game over / start over

    # networth

    # login

    # save/load users



class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.testplayer = Player('Player1', 10000, 'Is only a test.')
        self.teststock = Stock("teststock", 1000)
        self.buyorder = Order(100, 1, 'Player1', 'buy')
        self.sellorder = Order(100, 1, 'Player1', 'sell')
        self.testshare = convert_to_share(self.teststock, self.buyorder)

    def test_player(self):
        self.assertEqual(self.testplayer.name, 'Player1')
        self.assertEqual(self.testplayer.description, 'Is only a test.')
        self.assertEqual(self.testplayer.credit, 10000)
        self.assertListEqual(self.testplayer.portfolio, [])
        print('test_player passed.')

    def test_add_sallery(self):
        self.testplayer.add_salary()
        self.assertEqual(self.testplayer.credit, 15000)
        self.testplayer.credit += 4000
        self.assertEqual(self.testplayer.credit, 19000)
        print('test_add_sallery passed.')

    def test_add_shares_to_portfolio(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_share_to_portfolio(self.teststock, self.buyorder)
        self.assertIn(self.testshare, self.testplayer.portfolio)
        self.testplayer.add_share_to_portfolio(self.teststock, self.buyorder)
        testcombinedshares = Share('teststock', 2, 100)
        self.assertIn(testcombinedshares, self.testplayer.portfolio)
        print('test_add_shares_to_portfolio passed.')

    def test_list_similar_share(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.portfolio.append(self.testshare)
        self.assertIn(self.testshare, self.testplayer.portfolio)
        self.assertEqual([self.testshare], self.testplayer.list_similar_share(self.testshare))
        print('test_list_similar_share passed.')

    def test_remove_shares_from_portfolio(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_share_to_portfolio(self.teststock, self.buyorder)
        self.assertIn(self.testshare, self.testplayer.portfolio)
        self.testplayer.remove_shares_from_portfolio(self.testshare)
        self.assertNotIn(self.testshare, self.testplayer.portfolio)
        testcombinedshares = Share('teststock', 2, 100)
        self.testplayer.portfolio.append(testcombinedshares)
        self.assertIn(testcombinedshares, self.testplayer.portfolio)
        self.testplayer.remove_shares_from_portfolio(self.testshare)
        self.assertIn(self.testshare, self.testplayer.portfolio)
        print('test_remove_shares_from_portfolio passed.')

if __name__ == '__main__':
    unittest.main()
