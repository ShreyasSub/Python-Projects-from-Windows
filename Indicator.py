import operator
import numpy as np
import pandas as pd

from typing import Any
from typing import List
from typing import Dict
from typing import Union
from typing import Optional
from typing import Tuple

from TradingBot.StockFrame import StockFrame


class Indicators():

    def __init__(self, price_data_frame: StockFrame) -> None:
        self.StockFrame: StockFrame = price_data_frame
        self._price_groups = self.StockFrame.symbol_groups
        self._current_Indicators = {}
        self.indicator_signals = {}
        self._frame = self._StockFrame.frame

    def set_indicator_signals(self, indicator: str, buy: float, sell: float, condition_buy: Any,
                              condition_sell: Any) -> None:
        # If there is no signal for that indicator set a template
        if indicator not in self.indicator_signals:
            self._indicator_signals[indicator] = {}

        # Modify signal
        self.indicator_signals[indicator]['buy'] = buy
        self.indicator_signals[indicator]['sell'] = sell
        self.indicator_signals[indicator]['buy_operator'] = condition_buy
        self.indicator_signals[indicator]['sell_operator'] = condition_sell
    def obtain_indicator_signals(self, indicator: str) -> Dict:
        if indicator and indicator in self._indicator_signals:
            return self.indicator_signals[indicator]
        else:
            return self._indicator_signals

    @operator
    def price_data_frame(self) -> pd.DataFrame:
        return self._frame

    @price_data_frame.setter
    def price_data_frame(self, price_data_frame: pd.DataFrame) -> None:
        self._frame = price_data_frame

    def change_in_price(self) -> pd.DataFrame:
        locals_data = locals()
        del locals_data['self']

        column_name = 'change_in_price'
        self._current_Indicators[column_name] = {}
        self._current_Indicators[column_name]['args'] = locals_data
        self._current_Indicators[column_name]['func'] = self.change_in_price
        self._frame[column_name] = self._price_groups['close'].transform(
            lambda x: x.diff()

        )

    def rsi(self, period: int, method: str = 'wilders' ) -> pd.DataFrame:
        locals_data = locals()
        del locals_data['self']
        column_name = 'rsi'
        self._current_Indicators[column_name] = {}
        self._current_Indicators[column_name]['args'] = locals_data
        self._current_Indicators[column_name]['func'] = self.rsi

        if 'change_in_price' not in self._frame.columns:
            self.change_in_price()

            #Define the up days
            self._frame['up_day'] = self._price_groups['change-in_price'].transform(
                lambda x: np.where(x >=0, x,0)
            )
            self._frame['ewma_up'] = self._price_groups['up_day'].transform(
                lambda x: x.ewm(span=period).mean()
            )

            relative_strength = self._frame['ewma_up'] / self._frame['ewma_down']
            relative_strength_index = 100 - (100 / (1.0 + relative_strength))
            #Add the RSI indicator to the data frame.
            self._frame['rsi'] = np.where(relative_strength_index == 0, 1, 100 - (100 / (1.0 + relative_strength)))
            #clean up before sending hack
            self._frame.drop(
                labels = ['ewma_up', 'ewma_down', 'down_day', 'up_day', 'change_in_prior'],
                axis=1,
                inplace=True
             )
            return self._frame
        def sma(self, period: int) -> pd.DataFrame:
            locals_data = locals()
            del locals_data['self']
            column_name = 'sma'
            self._current_Indicators[column_name] = {}
            self._current_Indicators[column_name]['args'] = locals_data
            self._current_Indicators[column_name]['func'] = self.sma
            #Add the SMA
            self._frame[column_name] = self._price_groups['close'].transform(
                lambda x: x.rolling(window= period).mean()
            )
            return self._frame
        def ema(self, period: int, alpha: float = 0.0) -> pd.DataFrame:
            locals_data = locals()
            del locals_data['self']
            column_name = 'ema'
            self._current_Indicators[column_name] = {}
            self._current_Indicators[column_name]['args'] = locals_data
            self._current_Indicators[column_name]['func'] = self.ema
            # Add the SMA
            self._frame[column_name] = self._price_groups['close'].transform(
                lambda x: x.rolling(window=period).mean()
            )
            return self._frame
        def refresh(self):
            # First Update Groups
            self._price_groups = self._stock_frame_symbol_groups
            #Loop through all stored indicators
            for indicator in self._current_indicators:
                indicator_arguments = self._current_indicators[indicator]['args']
                indicator_function = self._current_indicators[indicator]['func']
                #Update the column
                indicator_function(**indicator_arguments)

        def check_signals(self) -> Union[pd.DataFrame, None]:
            signals_df = self.StockFrame._check_signals(insicators=self._indicator_signals)
            return signals_df












