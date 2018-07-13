import unittest

from traits.api import TraitError
from exchange import Stock, Exchange

class TestStocks(unittest.TestCase):

    def test_can_create_stock(self):
        stock = Stock(ticker="TEA", par_value=100.0)
        self.assertEqual(stock.ticker, "TEA")
        self.assertEqual(stock.stock_type, "Common")
        self.assertEqual(stock.last_dividend, 0)
        self.assertIsNone(stock.fixed_dividend)
        self.assertEqual(stock.par_value, 100)

    def test_add_stock(self):
        se = Exchange()
        se.add_stock("TEA")
        self.assertEqual(se["TEA"].ticker, "TEA")
        self.assertEqual(se["TEA"].par_value, 0.0)

    def test_stock_data(self):
        se = Exchange()
        se.add_stock("GIN", stock_type="Preferred", last_dividend=8, fixed_dividend=0.02, par_value=99)
        self.assertEqual(se["GIN"].stock_type, "Preferred")
        with self.assertRaises(TraitError):
            se["GIN"].stock_type = "Foo"

        stock = se["GIN"]
        stock.par_value = 100 # override
        # check data via dict API
        self.assertEqual(se["GIN"].last_dividend, 8)
        self.assertEqual(se["GIN"].fixed_dividend, 0.02)
        self.assertEqual(se["GIN"].par_value, 100)

    def test_exhange(self):
        se = Exchange()
        se.add_stock("TEA")
        se.add_stock("POP")
        se.add_stock("ALE", par_value=60)
        se.add_stock("GIN", "Preferred", 8, 0.02, 100)
        self.assertEqual(len(se),4)
        for ticker, stock in se.get_stocks():
            self.assertIsInstance(stock, Stock)
            self.assertEqual(ticker, stock.ticker)

        self.assertEqual(se["GIN"].stock_type, "Preferred")
        self.assertEqual(se["GIN"].fixed_dividend, 0.02)
        self.assertEqual(se["GIN"].par_value, 100)

        self.assertEqual(se["ALE"].par_value, 60)
        self.assertEqual(se["ALE"].last_dividend, 0)

if __name__ == '__main__':
    unittest.main()
