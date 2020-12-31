import numpy as np
import pandas as pd

from datetime import time
from datetime import datetime
from datetime import timezone

from typing import List
from typing import Dict
from typing import Union

from pandas.core.groupby import DataFrameGroupBy
from pandas.core.window import RollingGroupby

class StockFrame():
    def __init__(self, data: List[dict]) -> None:

        self._parse = None
        self._data = data
        self._frame: pd.DataFrame = self.create_frame()
        self._symbol_groups: DataFrameGroupBy = None
        self._symbol_rolling_groups: RollingGroupby = None

    @property
    def frame(self) -> pd.DataFrame:
        return self._frame

    @property
    def symbol_groups(self) -> DataFrameGroupBy:
        self._symbol_groups = self._frame.groupby(
         by='symbol',
         as_index=False,
         sort=True
    )
        return self._symbol_groups

    def symbol_rollin_groups(self, size: int) -> RollingGroupby:
        if not self._symbol_groups:
            self._symbol_groups



        self._symbol_rolling_groups = self._symbol_groups.rolling(size)
        return self._symbol_rolling_groups
    def create_frame(self) -> pd.DataFrame:
        # Make a data frame
        price_df = pd.DataFrame(data=self.data)
        price_df = self._parse-datetime.column(price_df=price_df)
        price_df = self._set_multi_index(price=price_df)
        return price_df
    def _pare_datetime_column(self, price_df: pd.DataFrame) -> pd.DataFrame:
        price_df['datetime'] = pd.to_datetime(price_df['datetime'], unit='ms', origin= 'unix')
        return price_df
    def _set_multi_index(self, price_df: pd.DataFrame):
        price_df =price_df.set_index(keys=['symbol', 'datetime', ])
        return price_df

    def add_rows(self, data: dict, row_id=None) -> None:
        column_names = ['open', 'close', 'high', 'low', 'volume']
        for quote in data:
            # parse that timestamp
            time_stamp = pd.to_datetime(
                data[quote]('quoteTimeInLong'),
                unit= 'ms',
                origin= 'unix'
            )
            #Define out Tuple
            row_id = (quote['symbol'], time_stamp)
            #Define our index
            row_values = [
                data[quote]['openPrice'],
                data[quote]['closePrice'],
                data[quote]['highPrice'],
                data[quote]['lowPrice'],
                data[quote]['askPrice'],
                data[quote]['askSize'] + data[quote]['bidSize'],
            ]
            #New Row
            new_row = pd.Series(data=row_values)
            #Add the row
            self._frame.loc[row_id, column_names] = new_row.values
            self.frame.sort_index(inplace=True)


    def do_indicators_exist(self, column_names: List[str]) -> bool:
        """Checks to see if the indicator columns specified exist
        Overview:
        --
        The user can add multiple indicator columns to their StockFrame object
        and in some cases we will need to modify those columns before making trades
        in those situations, this method, will help us check if those columns exist
        before proceeding on the code.

        Arguements:
        ---
        column names {List[str]} -- A list of column names that will be checked.
        Raises:
        ---
        KeyError: If a column is not found in StockFrame, a KeyError will be raised.

        Returns:
        ---
        bool -- 'True' if all columns exist.

        """
        if set (column_names).issubset(self._frame.columns):
            return True
        else:
            raise KeyError("The following indicator columns are missing from the StockFrame: {missing columns}".format(
                missing_columns=set(column_names).difference(self._frame.columns)

            ))


    def _check_signals(self, indicators: dict) -> Union[pd.Series, None]:
        """Returns the last row of StockFrame if conditions are met.
        Overview:
        ---
        Before a trade is executed, we must check to make sure if the conditions that warrant a 'buy'
        or 'sell' signal are met. This method will take last row for each signal in the StockFrame and
        compare the indicator column with the conditions specified by user.

        If the conditions are met the row will be returned back to user.
        Arguments:
        ---
        indicator {dict} -- A dictionary containing all the indicators to be checked along with their buy
        and sell criteria.

        Returns:
        ---
        {Union[pd.DataFrame, None]} -- If signals are generated then a pandas.DataFrame object
        will be returned. If no signals are found then nothing will be returned.

        """
        #Grab the last rows

        last_rows = self.symbol_groups.tail(1)
        conditions=[]

        #Check to see if all columns exist.
        if self.do_indicators_exist(column_names=indicators.keys()):
            for indicator in indicators:
                columns = last_rows[indicator]
                buy_condition_target = indicators[indicator]['buy'],
                sell_condition_target = indicators[indicator['sell'],
                buy_condition_operator = indicators[indicator]['buy_operator'],
                sell_condition_operator = indicators[indicator['sell_operator'],
                condition_1: pd.Series = buy_condition_operator(column, buy_condition_target),
                condition_2:pd.Series = sell_condition_operator(column, sell_condition_target),
                condition_1=condition_1.where(lambda x : x == True).dropna(),
                condition_2 = condition_2.where(lambda x: x == True).dropna(),
                conditions.append(('buys',condition_1)), ('sells',condition_2)

            return conditions






















