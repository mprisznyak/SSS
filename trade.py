"""
 Trade data

"""
from datetime import datetime, timedelta

from traits.api import HasStrictTraits, Int, Dict, Enum, Float, BaseInstance, Instance
from traits.api import TraitError

from exchange import  Exchange

# custom trait
TimeStamp = BaseInstance(datetime)


def create_GBCE():
    """ load stock data """
    se = Exchange()
    se.add_stock("TEA", last_dividend=0, par_value=100)
    se.add_stock("POP", last_dividend=8, par_value=100)
    se.add_stock("ALE", last_dividend=23, par_value=60)
    se.add_stock("GIN", stock_type="Preferred", last_dividend=8, fixed_dividend=0.02, par_value=100)
    se.add_stock("JOE", last_dividend=13, par_value=250)
    return se


class Trade(HasStrictTraits):
    """
    storage class for trade date
    """
    timestamp = TimeStamp
    quantity = Int
    indicator = Enum("B", "S")
    price = Float


class IllegalTrade(Exception):
    pass


class TradeData(HasStrictTraits):
    """
    storage class for trade data
    """
    data = Dict
    exchange = Instance(Exchange)

    def _exchange_default(self):
        return Exchange()

    def _data_default(self):
        # initialize trades storage
        return {ticker: [] for ticker, _ in self.exchange.get_stocks()}

    def add_trade(self, ticker, timestamp, quantity, indicator, price):
        try:
            # check if ticker is valid
            _ = self.exchange[ticker]
            trade = Trade(timestamp=timestamp, quantity=quantity, indicator=indicator, price=price)
            self.data[ticker].append(trade)
        except (KeyError, TraitError):
            raise IllegalTrade from None

    def get_trades_for(self, ticker):
        return self.data.get(ticker)

