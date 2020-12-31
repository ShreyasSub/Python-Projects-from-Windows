import time as true_time
import pprint
import pathlib
import operator
import pandas as pd

from datetime import datetime
from datetime import timedelta
from configparser import ConfigParser

from TradingBot import run_Bot
from TradingBot.Indicator import Indicators

#Grab the config file values.
config = ConfigParser
config.read('config/config.ini')
CLIENT_ID = config.get('main', 'CLIENT_ID')
REDIRECT_URI = config.get('main', 'REDIRECT_URI')
CREDENTIALS_PATH = config.get('main', 'CREDENTIALS_PATH')
ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER ')
#Initialize the bot
trading_bot = run_Bot(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH,
    trading_account=ACCOUNT_NUMBER,
    paper_trading=True
)

#Create a new portfolio
trading_bot_portfolio = trading_bot.create_portfolio()

#Add multiple positions to our portfolio.
multi_position = [
    {
      'asset_type':'equity',
      'quantity':2,
      'purchase_price':4.00,
      'symbol':'TSLA',
      'purchase_date':'2020-01-31'
    },
    {
      'asset_type':'equity',
      'quantity':2,
      'purchase_price':4.00,
      'symbol':'SQ',
      'purchase_date':'2020-01-31'
    }
]
#Add positions to portfolio.
new_positions = trading_bot_portfolio.add_positions(positions=multi_position)
pprint.pprint(new_positions)
#Add a single position to  Portfolio
trading_bot_portfolio.add_position(
    symbol='MSFT',
    quantity=10,
    purchase_price=10.00,
    asset_type='equity',
    purchase_date='2020-04-01'

)
pprint.pprint(trading_bot_portfolio.positions)
#Check to see if the regular market is open
if trading_bot.regular_marker_open:
    print('Regular Market Open')
else:
    print('Regular Market Not Open')

#Check to see if the Post Market is open.
if trading_bot.post_market_open:
    print('Post Market Open')
else:
    print('Post Market Not Open')

#Obtain the current quotes in the portfoio
current_quotes = trading_bot.obtain_current_qoutes()

#Define our date range
end_date = datetime.today()
start_date = end_date - timedelta(days=30)
#Obtain the historical prices
historical_prices = trading_bot.obtain_historical_prices(
    start=start_date,
    end=end_date,
    bar_size=1,
    bar_type='minute'
)
#Convert Data into Stock Frame
stock_frame = trading_bot.creat_stock_fram(data=historical_prices['aggregated'])
# Print head of stock frame.
pprint.pprint(stock_frame.frame.head(n=20))
#Create a new trade object
new_trade = trading_bot.create_trade(
    trade_id='long msft',
    enter_or_exit= 'enter',
    long_or_short= 'long',
    price= 200.00
)

#Make it Good Till Cancek
new_trade.good_till_cancel(cancel_time=datetime.now() + timedelta(minutes=90))
#Change Session
new_trade.modify_session(session='am')
#Add an Order Leg
new_trade.instrument(
    symbol = 'MSFT',
    quantity = 2,
    asset_type='EQUITY'
)
#Add a Stop Loss Order with the Main Order
new_trade.add_stop_loss(
    stop_size=10,
    percentage=.10,
)
#Print out order
pprint.pprint(new_trade.order)

#Create a new indicator client
indicator_client = Indicators(price_data_frame=stock_frame)

#Add the RSI indicator
indicator_client.rsi(period=14)

#Add a 200 day simple moving average
indicator_client.sma(period=200)

#Add a 50 day exponential moving avreage
indicator_client.ema(period=50)

#Add a signal to check for
indicator_client.set_indicator_signals(
    indicator='rsi',
    buy=40.0,
    sell=20.0,
    condition_buy=operator.ge,
    condition_sell=operator.le
)
#Define a trade dictionary
trades_dict = {
    'MSFT' : {
        'trade_func': trading_bot.trades['long_msft'],
        'trade_id':trading_bot.trades['long_msft'].trade_id

    }
}
while True:
    #Obtain the latest bar
    latest_bars = trading_bot.obatin_latest_bar()
    #Add those bars to StockFrame
    stock_frame.add_rows(data=latest_bars)
    #Refresh the indicators
    indicator_client.refresh()
    print("="*50)
    print("Current StockFrame")
    print("-" * 50)
    print(stock_frame.symbol_groups.tail())
    print("-" * 50)
    print("")


    #Check for signals.
    signals = indicator_client.check_signals()

    #Exectute trades.
    trading_bot.execute_signals(signals=signals, trades_to_execute=trades_dict)

    #Obtain the last bar, keep in mind this is after adding the new rows.
    last_bar_timestamp = trading_bot.creat_stock_frame.frame.tail(1).index.get_level_values(1)

    #Wait till the next bar
    trading_bot.wait_till_next_bar(last_bar_timestamp=last_bar_timestamp)




















