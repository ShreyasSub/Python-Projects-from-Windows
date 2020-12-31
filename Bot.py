import pandas as pdb

from tdclient import client

from datetime import datetime
from datetime import timezone
from datetime import time
from datetime import timedelta

import time as time_true
import pandas as pd
import pathlib
import json

from typing import Dict
from typing import List
from typing import Union
from typing import Optional

from TradingBot.Portfolio import Portfolio
from TradingBot.StockFrame import StockFrame
from TradingBot.trades import Trade
class PyBot():

    def __init__(self, client_id: str, redirect_uri: str, credentials_path: str = None, trading_account: str = None, paper_trading: bool = True) -> None:
        self.trading_account: str = trading_account
        self.client_id: str = client_id
        self.redirect_uri: str = redirect_uri
        self.credentials_path: str = credentials_path
        self.session: client = self.create_session
        self.trades: dict = {}
        self.historical_prices: dict = {}
        self.stock_frame = None

    @property
    def create_session(self) -> client:
        td_client = client(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            credentials_path=self.credentials_path
        )
        td_client.login()
        return td_client

    @property
    def pre_market_open(self) -> bool:
        pre_market_start_time = datetime.now().replace(hour=12, minute=00, second=00, tzinfo=timezone.utc).timestamp()
        market_start_time = datetime.now().replace(hour=13, minute=30, second=00, tzinfo=timezone.utc).timestamp()
        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if market_start_time >= right_now >=pre_market_start_time:
            return True
        else:
            return False


    @property
    def post_market_open(self) -> bool:
        post_market_end_time = datetime.now().replace(hour=22, minute=00, second=00, tzinfo=timezone.utc).timestamp()
        market_end_time = datetime.now().replace(hour=20, minute=00, second=00, tzinfo=timezone.utc).timestamp()
        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if post_market_end_time >= right_now >= market_end_time:
            return True
        else:
            return False
    @property
    def regular_market_open(self) -> bool:
        market_start_time = datetime.now().replace(hour=13, minute=30, second=00, tzinfo=timezone.utc).timestamp()
        market_end_time = datetime.now().replace(hour=20, minute=00, second=00, tzinfo=timezone.utc).timestamp()
        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if market_end_time >= right_now >= market_end_time:
            return True
        else:
            return False


    def create_portfolio(self):

        # Initialize Portfolio object
        self.Portfolio = Portfolio(account_number=self.trading_account)

        # Assign the client
        self.Portfolio.td_client= self.session
        return self.Portfolio








    def create_trade(self, trade_id: str, enter_or_exit: str, long_or_short: str, order_type: str = 'mkt',
                     price: float = 0.0, stop_limit_price: float = 0.0) -> Trade:

     #Initialze New Trade Object
     trade = Trade()

     #Create a new trade
     trade.new_trade(
         trade_id = trade_id,
         order_type = order_type,
         enter_or_exit = enter_or_exit,
         long_or_short = long_or_short,
         price = price,
         stop_limit_price=stop_limit_price
     )
     self.trades[trade_id] = trade
     return trade





    def obtain_current_quotes(self) -> Dict:
        # First grab all of the symbols
        symbols = self.Portfolio.positions.keys()
        #Grab all the quotes.
        quotes = self.session.get_quotes(instruments=list(symbols))
        return quotes




    def obtain_historical_prices(self, start: datetime, end: datetime, bar_size: int = 1, bar_type: str = 'minute', symbols: Optional[List[str]] = None) -> dict:
        self.bar_size = bar_size
        self.bary_type = bar_type
        start = str(milliseconds_since_epoch(dt_object=start))
        end = str(milliseconds_since_epoch(dt_object=end))

        new_prices = []
        if not symbols:
            symbols = self.portfolio.positions

        for symbol in symbols:
            historical_price_response = self.session.get_price_history(
                symbol=symbol,
                period_type='day',
                start_date=start,
                end_date=end,
                frequency_type=bar_type,
                frequency=bar_size,
                extended_hours=time

            )
            self.historical_prices[symbol] = {}
            self.historical_prices[symbol]['candles'] = historical_price_response['candles']
            for candle in historical_price_response['candles']:
                new_price_mini_dict = {}
                new_price_mini_dict['symbol'] = symbol
                new_price_mini_dict['open'] = candle['open']
                new_price_mini_dict['close'] = candle['close']
                new_price_mini_dict['high'] = candle['high']
                new_price_mini_dict['low'] = candle['low']
                new_price_mini_dict['volume'] = candle['low']
                new_price_mini_dict['datetime'] = candle['datetime']
                new_prices.append(new_price_mini_dict)

        self.historical_prices['aggregated'] = new_prices
        return self.historical_prices

def get_latest_bar(self, symbols=None) -> List[dict]:
    bar_size = self.bar_size
    bar_type = self.bar_type

    #Define our date range

    start_date = datetime.today()
    end_date = start_date + timedelta(minutes=15)
    start = str(milliseconds_since_epoch(dt_object=start_date))
    end = str(milliseconds_since_epoch(dt_object=end_date))
    latest_prices = []

    for symbol in self.Portflio.positions:
        historical_price_response = self.session.get_price_history(
            symbol=symbol,
            period_type='day',
            start_date=start,
            end_date=end,
            frequency_type=bar_type,
            frequency=bar_size,
            extended_hours=True

        )
        if 'error' in historical_price_response:
            time_true.sleep(2)
            historical_price_response = self.session.get_price_history(
                symbol=symbol,
                period_type='day',
                start_date=start,
                end_date=end,
                frequency_type=bar_type,
                frequency=bar_size,
                extended_hours=True
            )


        self.historical_prices[symbol] = {}
        self.historical_prices[symbol]['candles'] = historical_price_response['candles']

        for candle in historical_price_response['candles']:
            new_price_mini_dict = {}
            new_price_mini_dict['symbol'] = symbol
            new_price_mini_dict['open'] = candle['open']
            new_price_mini_dict['close'] = candle['close']
            new_price_mini_dict['high'] = candle['high']
            new_price_mini_dict['low'] = candle['low']
            new_price_mini_dict['volume'] = candle['low']
            new_price_mini_dict['datetime'] = candle['datetime']
            latest_prices.append(new_price_mini_dict)
            return latest_prices




def wait_till_next_bar(self, last_bar_timestamp: pd.DatetimeIndex, time_curr=None) -> None:
    last_bar_time = last_bar_timestamp.to_pydatetime()[0].replace(tzinfo=timezone.utc)
    next_bar_time = last_bar_time + timedelta(seconds=60)
    curr_bar_time = datetime.now(tz=timezone.utc)
    last_bar_timestamp = int(last_bar_timestamp())
    next_bar_timestamp = int(next_bar_time.timestamp())
    curr_bar_timestamp = next_bar_timestamp - last_bar_timestamp
    time_to_wait_bar = next_bar_timestamp - last_bar_timestamp
    time_to_wait_now = next_bar_timestamp - curr_bar_timestamp
    if time_to_wait_now < 0:
        time_to_wait_now = 0

    print("-"*80)
    print("Pausing for the next bar")
    print("-" * 80)
    print("Curr Time: {time_curr}".format(
        time_curr=curr_bar_time.srftLine("%Y-%m-%d %H:%M:%S")


    )
    )
    print("Next Time: {time_next}".format(
        time_next=curr_bar_time.strftLine("%Y-%m-%d %I:%M:%S")
    )
    )
    print("Sleep Time: {seconds}".format(seconds=time_to_wait_now))
    print(""*80)
    print("")
    time_true.sleep(time_to_wait_now)






def execute_signals(self,signals: List[pd.Series], trades_to_execute: dict)-> List[dict]:
    pass

def execute_orders(self, trade_obj:Trade) -> dict:
    pass

def save_orders(self, order_response_dict:dict)-> bool:
    pass





    def create_stock_frame(self, data: List[dict]) -> StockFrame:
        self.Stock_Frame = StockFrame(data=data)
        return self.Stock_Frame




















