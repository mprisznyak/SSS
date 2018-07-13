import unittest

from datetime import datetime

from trade import Trade, TradeData, IllegalTrade, Exchange

class TestTrade(unittest.TestCase):

    def setUp(self):
        se = Exchange()
        se.add_stock("TEA")
        se.add_stock("POP")
        self.test_trade_data = TradeData(exchange=se)

    def test_create_trade(self):
        t = Trade(timestamp=datetime(2018, 7, 11, 17, 11, 56, 543),
                  quantity=101)
        self.assertEqual(t.timestamp.hour, 17)
        self.assertEqual(t.timestamp.minute, 11)
        self.assertEqual(t.timestamp.second, 56)
        self.assertEqual(t.timestamp.microsecond, 543)
        self.assertEqual(t.quantity, 101)

    def test_trades(self):
        self.assertEqual(self.test_trade_data.get_trades_for("TEA"), [])
        self.assertIsNone(self.test_trade_data.get_trades_for("Foo"))

    def test_record_trade(self):
        trade_data = self.test_trade_data
        with self.assertRaises(IllegalTrade):
            trade_data.add_trade("Foo", datetime.now(), 1999, "B", 343.2)

        with self.assertRaises(IllegalTrade):
            trade_data.add_trade("TEA", datetime.now(), 1999, "C", 343.2)

        trade_data.add_trade("TEA", datetime.now(), 1999, "B", 343.2)
        trade_data.add_trade("TEA", datetime.now(), 2010, "S", 341.5)
        self.assertEqual(len(trade_data.get_trades_for("TEA")), 2)


if __name__ == '__main__':
    unittest.main()
