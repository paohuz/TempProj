from central_info import Data_info as DI, Trade_info as TI
from cust_enum import ACTION, INDICATOR, STRATEGY

import numpy as np
import matplotlib.pyplot as plt


class Strategy:
    def __init__(self, build_signal_auto=True):

        # SECTION cal_variables
        self.indicators = []
        self.position = f'{self.name_strategy}_pos'
        self.pnl = f'{self.name_strategy}_pnl'
        self.equity = f'{self.name_strategy}_equity'
        self.ret = f'{self.name_strategy}_ret'
        self.drawdown = f'{self.name_strategy}_drawdown'
        self.drawdown_daily = f'{self.name_strategy}_drawdown_daily'
        self.drawdown_daily_max = f'{self.name_strategy}_drawdown_daily_max'
        # !SECTION cal_variables

        self.build_signal_auto = build_signal_auto

    def init_data(self, data):
        # SECTION init_data
        self.data = data
        self.data[self.position] = 0
        self.data[self.equity] = 0
        self.data[self.equity][0] = TI.init_money
        # !SECTION init_data

    def build_trading_signal(self):
        raise NotImplementedError(
            'build_trading_signal() must be defined in subclass')

    # SECTION build_common_components
    def cal_equity(self):
        self.data[self.pnl] = self.data[self.position].shift(
            1)*self.data['pnl']
        self.data[self.equity][1:] = self.data[self.pnl][1:]
        self.data[self.equity] = self.data[self.equity].cumsum()
    # !SECTION build_common_components

    # SECTION calculate_evaluation_numbers
    def cal_sharpe_ratio(self):
        self.data[self.ret] = self.data[self.equity].pct_change()
        self.sharpe_ratio = np.sqrt(
            252) * (self.data[self.ret].mean() / self.data[self.ret].std())
        print(f'sharpe: {self.sharpe_ratio}')

    def call_mmd(self):
        """calculate mmd follow https://www.reddit.com/r/learnpython/comments/bxyze5/getting_max_drawdown_with_python/
        changing from total return to equity
        """
        self.data[self.drawdown] = self.data[self.equity] - \
            self.data[self.equity].cummax()
        self.mmd = self.data[self.drawdown].min()
        print(f'maxdd: {self.mmd}')

    def call_mmd_daily(self):
        """https://www.datacamp.com/community/tutorials/finance-python-trading
        changing from adj close to equity
        """
        window = 48
        rolling_max = self.data[self.equity].rolling(
            window, min_periods=1).max()
        self.data[self.drawdown_daily] = self.data[self.equity] / \
            rolling_max - 1.0

        # Calculate the minimum (negative) daily drawdown
        self.data[self.drawdown_daily_max] = self.data[self.drawdown_daily].rolling(
            window, min_periods=1).min()

    # !SECTION calculate_evaluation_numbers

    # SECTION visualizations
    def plot(self):
        ax_cnt = 5
        fig, ax = plt.subplots(ax_cnt, 1)
        for feature in DI.feature_cols:
            ax[0].plot(self.data[feature].values, label=feature)
        ax[1].plot(self.data[self.position].values, label='position')
        for indicator in self.indicators:
            ax[2].plot(self.data[indicator].values, label=indicator)
        ax[3].plot(self.data[self.equity].values, label='equity')
        ax[4].plot(self.data[self.drawdown_daily].values, label='dd daily')
        ax[4].plot(self.data[self.drawdown_daily_max].values,
                   label='mdd daily')

        for i in range(ax_cnt):
            ax[i].legend()

        fig.suptitle(self.name_strategy)
        # plt.legend(pad=0.1)
        plt.show()
    # !SECTION visualizations

    def run_backtest(self, data):
        if self.build_signal_auto:
            self.build_trading_signal(data)
        self.cal_equity()
        self.cal_sharpe_ratio()
        self.call_mmd()
        self.call_mmd_daily()
        self.plot()


class Buy_hold(Strategy):
    def __init__(self, build_signal_auto=True):

        # SECTION Strategy_name
        # name_short_long
        self.name_strategy = f'{STRATEGY.BH.value}'
        # !SECTION Strategy_name

        super().__init__(build_signal_auto)

        # SECTION indicators
        # !SECTION indicators

        # SECTION conditional_variables
        # !SECTION conditional_variables

    def build_trading_signal(self, data):
        # SECTION init_data
        self.init_data(data)
        # !SECTION init_data

        self.data[self.position] = ACTION.LONG.value


class Sell_hold(Strategy):
    def __init__(self, build_signal_auto=True):

        # SECTION Strategy_name
        # name_short_long
        self.name_strategy = f'{STRATEGY.SH.value}'
        # !SECTION Strategy_name

        super().__init__(build_signal_auto)

        # SECTION indicators
        # !SECTION indicators

        # SECTION conditional_variables
        # !SECTION conditional_variables

    def build_trading_signal(self, data):
        # SECTION init_data
        self.init_data(data)
        # !SECTION init_data

        self.data[self.position] = ACTION.SHORT.value


class Strategy_ma_crossover(Strategy):
    def __init__(self, ma_short, ma_long, build_signal_auto=True):

        # SECTION Strategy_name
        # name_short_long
        self.name_strategy = f'{STRATEGY.MA.value}_{ma_short}_{ma_long}'
        # !SECTION Strategy_name

        super().__init__(build_signal_auto)

        # SECTION indicators
        self.name_indicator = INDICATOR.MA.value
        # !SECTION indicators

        # SECTION conditional_variables
        self.signal_short = f'{self.name_indicator}_{ma_short}'
        self.signal_long = f'{self.name_indicator}_{ma_long}'
        self.indicators.append(self.signal_short)
        self.indicators.append(self.signal_long)
        # !SECTION conditional_variables

    def build_trading_signal(self, data):
        # SECTION init_data
        self.init_data(data)
        # !SECTION init_data

        # SECTION strategy
        self.data.loc[self.data[self.signal_short] >
                      self.data[self.signal_long], [self.position]] = ACTION.LONG.value
        self.data.loc[self.data[self.signal_short] <
                      self.data[self.signal_long], [self.position]] = ACTION.SHORT.value
        # !SECTION strategy


class Strategy_rsi_threshold(Strategy):
    def __init__(self, period, oversold, overbought, tp, sl, build_signal_auto=True):

        # SECTION Strategy_name
        # name_short_long
        self.name_strategy = f'{STRATEGY.RSI.value}_{oversold}_{overbought}'
        # !SECTION Strategy_name

        super().__init__(build_signal_auto)

        # SECTION indicators
        self.name_indicator = INDICATOR.RSI.value
        # !SECTION indicators

        # SECTION conditional_variables
        self.oversold = oversold
        self.overbought = overbought
        self.tp = tp
        self.sl = sl
        self.signal_period = f'{self.name_indicator}_{period}'
        self.indicators.append(self.signal_period)
        # !SECTION conditional_variables

    def build_trading_signal(self, data):
        # SECTION init_data
        self.init_data(data)
        # !SECTION init_data

        # SECTION strategy
        prev_act = ACTION.NOTHING

        for i in range(self.data.shape[0]):
            if prev_act is ACTION.NOTHING:
                if self.data[self.signal_period][i] >= self.overbought:
                    self.data[self.position][i] = ACTION.SHORT.value
                    entry_idx = i+1
                    prev_act = ACTION.SHORT
                elif self.data[self.signal_period][i] <= self.oversold:
                    self.data[self.position][i] = ACTION.LONG.value
                    entry_idx = i+1
                    prev_act = ACTION.LONG
                else:
                    self.data[self.position][i] = ACTION.NOTHING.value
            elif prev_act is ACTION.SHORT:
                if self.data['pnl'][entry_idx:i+1].sum() <= -self.tp:
                    self.data[self.position][i] = ACTION.NOTHING.value
                    prev_act = ACTION.NOTHING
                elif self.data['pnl'][entry_idx:i+1].sum() >= self.sl:
                    self.data[self.position][i] = ACTION.NOTHING.value
                    prev_act = ACTION.NOTHING
                elif self.data[self.signal_period][i] <= self.oversold:
                    self.data[self.position][i] = ACTION.LONG.value
                    entry_idx = i+1
                    prev_act = ACTION.LONG
                else:
                    self.data[self.position][i] = ACTION.SHORT.value
            elif prev_act is ACTION.LONG:
                if self.data['pnl'][entry_idx:i+1].sum() >= self.tp:
                    self.data[self.position][i] = ACTION.NOTHING.value
                    prev_act = ACTION.NOTHING
                elif self.data['pnl'][entry_idx:i+1].sum() <= -self.sl:
                    self.data[self.position][i] = ACTION.NOTHING.value
                    prev_act = ACTION.NOTHING
                elif self.data[self.signal_period][i] >= self.overbought:
                    self.data[self.position][i] = ACTION.SHORT.value
                    entry_idx = i+1
                    prev_act = ACTION.SHORT
                else:
                    self.data[self.position][i] = ACTION.LONG.value
        # !SECTION strategy


class Strategy_rl_pg(Strategy):
    def __init__(self, build_signal_auto=True):

        # SECTION Strategy_name
        # name_short_long
        self.name_strategy = f'{STRATEGY.PG.value}'
        # !SECTION Strategy_name

        super().__init__(build_signal_auto)

        # SECTION indicators
        # self.name_indicator = INDICATOR.PG.value
        # !SECTION indicators

        # SECTION conditional_variables
        # self.signal_short = f'{self.name_indicator}_{ma_short}'
        # self.signal_long = f'{self.name_indicator}_{ma_long}'
        # self.indicators.append(self.signal_short)
        # self.indicators.append(self.signal_long)
        # !SECTION conditional_variables

    def build_trading_signal(self, data):
        # SECTION init_data
        self.init_data(data)
        # !SECTION init_data

        # SECTION strategy
        # !SECTION strategy

    def update_trading_signal(self, idx, action):
        self.data[self.position][idx] = action.value
