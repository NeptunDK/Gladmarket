#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest
from helpers import Order, Share
import logging
from operator import itemgetter, attrgetter


class Player:  # could also be called wallet, then a player/firm/company/bot could have a wallet
    def __init__(self, name, starting_credits, description=None):
        self.name = name
        self.description = description
        self.credit = starting_credits
        self.portfolio = []  # Share = namedtuple('Share', ['stockname', 'vol', 'buyprice'])
        self.networth = None
        self.salary = 5000

    def add_salary(self):
        # todo is it safe to have this here?
        self.credit += self.salary

    def add_share_to_portfolio(self, share):
        similar_share = self.list_similar_share(share)

        if not similar_share:
            self.portfolio.append(share)
        else:
            new_volume = similar_share[0].vol + share.vol
            updated_share = Share(share.stockname, new_volume, share.buyprice)
            self.portfolio.remove(similar_share[0])
            self.portfolio.append(updated_share)
            logging.warning(f"New order: {share} combined with old share: {similar_share[0]} into: {updated_share}.")
        # todo need check to see if player actually bought the stock?

    def remove_shares_from_portfolio(self, share):
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
        self.portfolio = sorted(self.portfolio, key=attrgetter('vol'), reverse=True)  # secondary key
        self.portfolio = sorted(self.portfolio, key=attrgetter('stockname',))  # primary key

    def combine_portfolio_shares(self):
        # todo combine don't care about buyprice
        pass

    def list_shares(self):
        # todo sort? list_shares(self, sortkey=None)
        # todo list number of shares list_shares(self, amount=None)
        return self.portfolio

    # sell stocks/shares
    # on the market instead?

    # purchase/selling history here or somewhere else?
    # self.transactions_log

    # out of buisness / game over / start over
    #

    def update_networth(self):
        # todo update to use CURRENT stockprice, instead of share.buyprice
        share_networth = sum(share.vol * share.buyprice for share in self.portfolio)
        self.networth = self.credit + share_networth

    # login

    # save/load user
    # todo is this the correct place?


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.testplayer = Player('Player1', 10000, 'Is only a test.')
        self.testshare = Share("Teststock", 1, 100)
        self.buyorder = Order(100, 1, 'Player1', 'buy')
        self.sellorder = Order(100, 1, 'Player1', 'sell')

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
        self.testplayer.add_share_to_portfolio(self.testshare)
        self.assertIn(self.testshare, self.testplayer.portfolio)
        self.testplayer.add_share_to_portfolio(self.testshare)
        testcombinedshares = Share('Teststock', 2, 100)
        self.assertIn(testcombinedshares, self.testplayer.portfolio)
        print('test_add_shares_to_portfolio passed.')

    def test_add_shares_to_portfolio2(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_share_to_portfolio(Share('DELL', 1, 1000))
        self.testplayer.add_share_to_portfolio(Share('DELL', 8, 1000))
        self.testplayer.add_share_to_portfolio(Share('DELL', 1, 5000))
        self.testplayer.add_share_to_portfolio(Share('DELL', 1, 1000))
        print('name')
        print(self.testplayer.portfolio)
        self.assertIn(Share(stockname='DELL', vol=10, buyprice=1000), self.testplayer.portfolio)
        self.assertIn(Share(stockname='DELL', vol=1, buyprice=5000), self.testplayer.portfolio)
        print('test_add_shares_to_portfolio2 passed.')

    def test_list_similar_share(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.portfolio.append(self.testshare)
        self.assertIn(self.testshare, self.testplayer.portfolio)
        self.assertEqual([self.testshare], self.testplayer.list_similar_share(self.testshare))
        print('test_list_similar_share passed.')

    def test_remove_shares_from_portfolio(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_share_to_portfolio(self.testshare)
        self.assertIn(self.testshare, self.testplayer.portfolio)
        self.testplayer.remove_shares_from_portfolio(self.testshare)
        self.assertNotIn(self.testshare, self.testplayer.portfolio)
        testcombinedshares = Share('Teststock', 2, 100)
        self.testplayer.add_share_to_portfolio(testcombinedshares)
        self.assertIn(testcombinedshares, self.testplayer.portfolio)
        self.testplayer.remove_shares_from_portfolio(self.testshare)
        self.assertIn(self.testshare, self.testplayer.portfolio)
        print('test_remove_shares_from_portfolio passed.')

    def test_list_shares(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_share_to_portfolio(self.testshare)
        self.assertIn(self.testshare, self.testplayer.portfolio)
        print(self.testplayer.list_shares()[0])
        print('test_list_shares passed.')

    def test_update_networth(self):
        # todo update to use CURRENT stockprice, instead of share.buyprice
        self.assertEqual(self.testplayer.networth, None)
        self.testplayer.update_networth()
        self.assertEqual(self.testplayer.networth, 10000)
        self.testplayer.add_share_to_portfolio(self.testshare)
        self.testplayer.update_networth()
        self.assertEqual(self.testplayer.networth, 10100)
        self.testsharetwo = Share("Sharetest", 2, 33)
        self.testplayer.add_share_to_portfolio(self.testsharetwo)
        self.testplayer.update_networth()
        self.assertEqual(self.testplayer.networth, 10166)
        print('test_update_networth passed.')

    def test_sort_portfolio(self):
        self.assertEqual([], self.testplayer.portfolio)
        self.testplayer.add_share_to_portfolio(Share('IMB', 3, 150))
        self.testplayer.add_share_to_portfolio(Share('IMB', 2, 75))
        self.testplayer.add_share_to_portfolio(Share('DELL', 1, 1000))
        self.testplayer.add_share_to_portfolio(Share('DELL', 8, 1000))
        self.testplayer.add_share_to_portfolio(Share('DELL', 1, 5000))
        self.testplayer.add_share_to_portfolio(Share('DELL', 1, 1000))
        self.assertIn(Share(stockname='IMB', vol=3, buyprice=150), self.testplayer.portfolio)
        self.assertIn(Share(stockname='IMB', vol=2, buyprice=75), self.testplayer.portfolio)
        self.assertIn(Share(stockname='DELL', vol=10, buyprice=1000), self.testplayer.portfolio)
        self.assertIn(Share(stockname='DELL', vol=1, buyprice=5000), self.testplayer.portfolio)
        self.testplayer.sort_portfolio()
        self.assertEqual([Share(stockname='DELL', vol=10, buyprice=1000),
                          Share(stockname='DELL', vol=1, buyprice=5000),
                          Share(stockname='IMB', vol=3, buyprice=150),
                          Share(stockname='IMB', vol=2, buyprice=75)], self.testplayer.portfolio)
        print('test_sort_portfolio passed.')

if __name__ == '__main__':
    unittest.main()
