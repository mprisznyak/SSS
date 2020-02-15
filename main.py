"""
Super Simple Stocks example

by Miklós Prisznyák

Installation

1. Create and activate a virtual Python environment (at least v3.6)
2. Run

   pip install traits

"""
import argparse
from datetime import datetime, timedelta
import operator
import functools

# Use Enthought traits for type safety
from traits.api import HasStrictTraits,  Instance

from trade import create_GBCE, TradeData


def geometric_mean(seq):
    """
    Compute geometric mean for values in a sequence
    :param seq: sequence of numerical values
    :return: float
    """
    return pow(functools.reduce(operator.mul, seq, 1), 1/len(seq))


class Quant(HasStrictTraits):
    """
    a controller class to perform the required tasks
    """

    trade_data = Instance(TradeData)

    def _trade_data_default(self):
        return TradeData(exchange=create_GBCE())

    def get_stock(self, ticker):
        try:
            stock = self.trade_data.exchange[ticker]
        except KeyError:
            raise ValueError(f"No stock data for {ticker} ")
        return stock

    def get_dividend_yield(self, ticker, market_price):
        stock = self.get_stock(ticker)
        try:
            if stock.stock_type == "Common":
                dy = stock.last_dividend / market_price
            else:
                dy = stock.fixed_dividend*stock.par_value / market_price
        except ZeroDivisionError:
            raise ValueError(f"Error in computing dividend yield for {ticker} at price={market_price}")
        return dy

    def get_PE(self, ticker, market_price):
        stock = self.get_stock(ticker)
        try:
            result = market_price / stock.last_dividend
        except ZeroDivisionError:
            result = "NA"
        return result

    def record_trade(self, ticker, timestamp, quantity, indicator, price):
        # record transaction by delegating the job
        self.trade_data.add_trade(ticker, timestamp, quantity, indicator, price)

    def get_VWSP(self, ticker, from_timestamp, to_timestamp):
        # compute volume weighted stock price
        try:
            # dict of Trade keyed on timestamp
            trades = self.trade_data.get_trades_for(ticker)
            result = 0
            volume = 0
            for trade in trades:
                # filter on timestamp
                if from_timestamp <= trade.timestamp <= to_timestamp:
                    result += trade.price*trade.quantity
                    volume += trade.quantity
            result /= volume
        except (AttributeError, ZeroDivisionError):
            result = "NA"
        return result


    def get_GBCE_index(self, timestamp, time_interval):
        """
           compute arithmetic average for a ticket in this time period and then do geometric mean for all tickers
        """
        from_timestamp = timestamp - time_interval
        try:
            prices = []
            for ticker, _ in self.trade_data.exchange.get_stocks():
                trades = self.trade_data.get_trades_for(ticker)
                price = 0
                n = 0
                for trade in trades:
                    if from_timestamp <= trade.timestamp <= timestamp:
                        price += trade.price
                        n += 1
                if n:
                    price /= n # average in time period
                    prices.append(price)
            result = geometric_mean(prices)
        except ZeroDivisionError:
            result = "N/A"
        return result


def main():
    """
    Entry point

    handles CLI functions using the controller object quant
    """
    quant = Quant()

    def price_report(args):
        """
        Handler for subcommand price_report

        :param args:
        :return:
        """
        dividend_yield = quant.get_dividend_yield(args.ticker, args.price)
        pe = quant.get_PE(args.ticker, args.price)

        ts = datetime.now()
        # 15 minutes before now
        start_timestamp = ts - timedelta(minutes=15)
        vwsp = quant.get_VWSP(args.ticker, start_timestamp, ts)
        # compute share GBCE index
        allshare_index = quant.get_GBCE_index(ts, timedelta(hours=1))
        print(f"""  
        Price report  
        ============
        
        Ticker                       {args.ticker:>20} 
        Dividend yield               {dividend_yield:>20}
        P/E                          {pe:>20}
        Volume Weighted Stock Price  {vwsp:>20}
           in past 15 minutes
        GBCE Index                   {allshare_index:>20}
            in past hour
         
        
        """)

    def record_trade(args):
        """
        Handler for subcommand record_trade

        :param args:
        :return:
        """
        try:
            ts = datetime.strptime(args.timestamp, "%d-%m-%Y:%H:%M:%S:%f")
        except ValueError:
            print(f"Illegal timestamp format: {args.timestamp}")
            raise  # don't continue!
        try:
            quant.record_trade(args.ticker, ts, args.quantity, args.indicator, args.price)
            print(f"Trade recorded for {args.ticker}")
        except Exception:
            print(f"Error in recording trade for {args.ticker}")


    # command line interface
    parser = argparse.ArgumentParser(description='Super Simple Stocks')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    # sub commands: price_report and record_trade
    subparsers = parser.add_subparsers(title='available commands',
                                       help='arguments ')
    # parser for command "price_report"
    parser_pr = subparsers.add_parser('price_report', help='<ticker> <market price>')
    parser_pr.add_argument('ticker', help='stock ticker')
    parser_pr.add_argument('price', type=float, help='market price')
    parser_pr.set_defaults(func=price_report)

    # parser for command "record_trade"
    parser_rt = subparsers.add_parser('record_trade', help="<ticker> <timestamp> <quantity> <indicator> <price>")
    parser_rt.add_argument('ticker', help='stock ticker')
    parser_rt.add_argument('timestamp', help='DD-MM-YYYY:HH:mm:sec:ms')
    parser_rt.add_argument('quantity', type=int, help='quantity of stocks in transaction')
    parser_rt.add_argument('indicator', choices=["B", "S"], help='(B)uy or (S)ell')
    parser_rt.add_argument('price', type=float, help='<trade price>')
    parser_rt.set_defaults(func=record_trade)

    args = parser.parse_args()
    # call handler function
    args.func(args)


if __name__ == "__main__":
    main()
