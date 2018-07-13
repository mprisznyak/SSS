"""
Stock exchange

"""

from traits.api import HasStrictTraits, Str, Dict, Enum, Float, Either


class Stock(HasStrictTraits):
    """
    ticker fundamentals
    """
    ticker = Str
    stock_type = Enum("Common", "Preferred")
    last_dividend = Float
    fixed_dividend = Either(None, Float)
    par_value = Float


class Exchange(HasStrictTraits):
    """
    in-memory database for stocks
    """
    stocks = Dict(Str, Stock)

    def add_stock(self, ticker, stock_type=None, last_dividend=None, fixed_dividend=None, par_value=None):
        stock = Stock(ticker=ticker)
        if stock_type:
            stock.stock_type = stock_type
        if last_dividend:
            stock.last_dividend = last_dividend
        if fixed_dividend:
            stock.fixed_dividend = fixed_dividend
        if par_value:
            stock.par_value = par_value

        self.stocks[ticker] = stock

    def __getitem__(self, symbol):
        # indexable by stock symbol
        return self.stocks.get(symbol)

    def __len__(self):
        return len(self.stocks)

    def get_stocks(self):
        # iterate over all tickers
        for ticker in self.stocks.keys():
            yield ticker, self.stocks[ticker]

