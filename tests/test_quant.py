import unittest
from datetime import datetime, timedelta

from main import Quant

class TestQuant(unittest.TestCase):

    def test_dividend_yield(self):
        quant = Quant()
        self.assertEqual(quant.get_dividend_yield("TEA", 238.2), 0)
        self.assertEqual(quant.get_dividend_yield("TEA", 455.46), 0)
        with self.assertRaises(ValueError):
            self.assertEqual(quant.get_dividend_yield("TEA", 0), 0)

        # same dividend but different stock type will result in a different result for the same market price
        assert quant.get_stock("POP").last_dividend == quant.get_stock("GIN").last_dividend
        # Common stock
        self.assertEqual(quant.get_dividend_yield("POP", 100.0), 0.08)
        # Preferred stock
        self.assertEqual(quant.get_dividend_yield("GIN", 100.0), 0.02)

    def test_PE(self):
        quant = Quant()
        self.assertEqual(quant.get_PE("POP", 40), 5)


    def test_VWSP(self):
        quant = Quant()
        quant.record_trade("TEA", datetime(2018, 7, 11, 17, 11, 56, 543), 1000, "B", 50.0)
        quant.record_trade("TEA", datetime(2018, 7, 11, 17, 12, 58, 42), 2000, "B", 100.0)
        quant.record_trade("TEA", datetime(2018, 7, 11, 17, 18, 8, 2), 1000, "S", 50.0)
        # out of range data
        quant.record_trade("TEA", datetime(2018, 7, 11, 17, 38, 8, 2), 2000, "B", 100.0)

        expected = (2*1000*50+2000*100)/4000

        end_timestamp = datetime(2018, 7, 11, 17, 20, 20, 21)
        # 15 minutes before
        start_timestamp = end_timestamp - timedelta(minutes=15)
        self.assertEqual(quant.get_VWSP("TEA", start_timestamp, end_timestamp), expected)

        # te

    def test_GBCE_index(self):
        quant = Quant()
        quant.record_trade("TEA", datetime(2018, 7, 11, 17, 11, 26, 543), 1000, "B", 40.0)
        quant.record_trade("TEA", datetime(2018, 7, 11, 17, 12, 38, 42), 2000, "B", 90.0)
        quant.record_trade("TEA", datetime(2018, 7, 11, 17, 18, 8, 2), 1000, "S", 70.0)

        quant.record_trade("POP", datetime(2018, 7, 11, 17, 12, 16, 543), 1000, "B", 60.0)
        quant.record_trade("POP", datetime(2018, 7, 11, 17, 13, 38, 42), 2000, "B", 110.0)
        quant.record_trade("POP", datetime(2018, 7, 11, 17, 15, 8, 2), 1000, "B", 50.0)
        quant.record_trade("POP", datetime(2018, 7, 11, 17, 15, 9, 2), 1000, "S", 60.0)

        quant.record_trade("JOE", datetime(2018, 7, 11, 17, 10, 6, 543), 1000, "B", 70.0)
        quant.record_trade("JOE", datetime(2018, 7, 11, 17, 11, 5, 42), 2000, "B", 120.0)
        quant.record_trade("JOE", datetime(2018, 7, 11, 17, 11, 8, 2), 1000, "S", 50.0)
        quant.record_trade("JOE", datetime(2018, 7, 11, 17, 11, 9, 2), 1000, "B", 50.0)
        quant.record_trade("JOE", datetime(2018, 7, 11, 17, 11, 18, 2), 1000, "S", 55.0)

        result = quant.get_GBCE_index(datetime(2018, 7, 11, 18), timedelta(hours=1))
        # check that geometric mean is smaller than the arithmetic one, computed by hand
        self.assertLessEqual(result, 68.55555555555556)



if __name__ == '__main__':
    unittest.main()
