
# , Strategy_info as SI
from central_info import Data_info as DI, Synthesis_feature as SF, Trade_info as TI
from cust_enum import ACTION, STRATEGY
import matplotlib.pyplot as plt
import numpy as np

from backtest.strategy import Buy_hold, Strategy_ma_crossover, Strategy_rsi_threshold


class Backtest:
    def __init__(self, data):
        self.data = data
        self.strategies = [
            Buy_hold(),
            Strategy_ma_crossover(40, 252),
            Strategy_rsi_threshold(14, 25, 70, 50, 15)
        ]

    def backtest(self):
        for strategy in self.strategies:
            strategy.run_backtest(self.data)

        self.plot_equity()
        self.plot_action()
        self.data.to_csv('backtest.csv')

    def plot_equity(self):
        ax_cnt = 1+len(self.strategies)
        fig, ax = plt.subplots(ax_cnt, 1)
        for feature in DI.feature_cols:
            ax[0].plot(self.data[feature].values, label=feature)
            ax[0].legend()

        for idx, strategy in enumerate(self.strategies):
            ax_id = idx + 1
            ax[ax_id].plot(self.data[strategy.equity].values,
                           label=strategy.name_strategy)
            ax[ax_id].legend()

        fig.suptitle('equity')
        plt.show()

    def plot_action(self):
        ax_cnt = 1+len(self.strategies)
        fig, ax = plt.subplots(ax_cnt, 1)
        for feature in DI.feature_cols:
            ax[0].plot(self.data[feature].values, label=feature)
            ax[0].legend()

        for idx, strategy in enumerate(self.strategies):
            ax_id = idx + 1
            ax[ax_id].plot(self.data[strategy.position].values,
                           label=strategy.name_strategy)
            ax[ax_id].legend()

        fig.suptitle('action')
        plt.show()

    def plot(self):
        ax_cnt = 1
        if SF.pnl:
            ax_cnt += 1
        if len(SF.ma) > 0:
            ax_cnt += 3
        if len(SF.rsi) > 0:
            ax_cnt += 3
        if len(SF.macd) > 0:
            ax_cnt += 1

        fig, ax = plt.subplots(ax_cnt, 1)
        ax_id = 0
        for feature in DI.feature_cols:
            ax[ax_id].plot(self.data[feature].values, label=feature)
            ax[ax_id].legend()
        ax_id += 1
        if SF.pnl:
            ax[ax_id].plot(self.data['pnl'].values, label='pnl')
            ax[ax_id].legend()
        ax_id += 1
        for feature in SF.ma:
            ax[ax_id].plot(self.data[f'ma_{feature}'].values, label=feature)
            ax[ax_id].legend()
        ax_id += 1
        if len(SF.ma) > 0:
            ax[ax_id].plot(self.data[f'ma_pos'].values, label='ma_pos')
            ax[ax_id].legend()
            ax_id += 1
            ax[ax_id].plot(self.data[f'ma_equity'].values, label='ma_equity')
            ax[ax_id].legend()
            ax_id += 1
        # for feature in SF.rsi:
        #     ax[ax_id].plot(self.data[f'rsi_{feature}'].values, label=feature)
        #     ax[ax_id].legend()
        # ax_id += 1
        # if len(SF.rsi) > 0:
        #     ax[ax_id].plot(self.data[f'rsi_pos'].values, label='rsi_pos')
        #     ax[ax_id].legend()
        #     ax_id += 1
        #     ax[ax_id].plot(self.data[f'rsi_equity'].values, label='rsi_equity')
        #     ax[ax_id].legend()
        #     ax_id += 1
        ax[ax_id].plot(self.data[f'bh_pos'].values, label='bh_pos')
        ax[ax_id].legend()
        ax_id += 1
        ax[ax_id].plot(self.data[f'bh_equity'].values, label='bh_equity')
        ax[ax_id].legend()
        ax_id += 1

        for feature in SF.macd:
            ax[ax_id].plot(self.data[f'macd_{feature}'].values, label=feature)
            ax[ax_id].legend()
        ax_id += 1

        plt.show()

    def test(self):
        self.ma_trade()
        # self.rsi_trade()
        self.buy_hold()
        self.cal_equity(['bh', 'ma'])
        # print(self.data)
        self.plot()
        # self.data.to_csv('backtest.csv')
        self.mmd()

    def mmd(self):
        ticker = self.data['bh_equity']
        # self.data[trade_return] = self.data[trade_equity].pct_change()
        # self.data["total_return"] = self.data["daily_returns"].cumsum()
        # self.data["drawdown"] = self.data["total_return"] - \
        # self.data["total_return"].cummax()
        self.data["drawdown"] = self.data['bh_equity'] / \
            ticker.cummax() - 1.0  # ticker - ticker.cummax()
        maxdd = self.data["drawdown"].min()
        print(f'maxdd: {maxdd}')
        # window = 252
        window = 48  # self.data.shape[0]

        # Calculate the max drawdown in the past window days for each day
        rolling_max = self.data['bh_equity'].rolling(
            window, min_periods=1).max()
        daily_drawdown = self.data['bh_equity']/rolling_max - 1.0

        # Calculate the minimum (negative) daily drawdown
        max_daily_drawdown = daily_drawdown.rolling(
            window, min_periods=1).min()

        # Plot the results
        plt.plot(daily_drawdown.values)
        plt.plot(max_daily_drawdown.values)
        # daily_drawdown.plot()
        # max_daily_drawdown.plot()

        # Show the plot
        plt.show()

    def buy_hold(self):
        indicator = 'bh'
        trade_pos = f'{indicator}_pos'
        self.data[trade_pos] = ACTION.LONG.value

    def ma_trade(self):
        indicator = 'ma'
        trade_pos = f'{indicator}_pos'
        trade_pnl = f'{indicator}_pnl'
        trade_equity = f'{indicator}_equity'
        self.data[trade_pos] = 0
        signal_short = f'{indicator}_40'
        signal_long = f'{indicator}_252'
        self.data.loc[self.data[signal_short] >
                      self.data[signal_long], [trade_pos]] = ACTION.LONG.value
        self.data.loc[self.data[signal_short] <
                      self.data[signal_long], [trade_pos]] = ACTION.SHORT.value
        # self.data[trade_pnl] = self.data[trade_pos].shift(1)*self.data['pnl']
        # self.data[trade_equity] = 0
        # self.data[trade_equity][0] = TI.init_money
        # self.data[trade_equity][1:] = self.data[trade_pnl][1:]
        # self.data[trade_equity] = self.data[trade_equity].cumsum()

    def rsi_trade(self):
        indicator = 'rsi'
        trade_pos = f'{indicator}_pos'
        trade_pnl = f'{indicator}_pnl'
        trade_equity = f'{indicator}_equity'
        self.data[trade_pos] = 0
        signal_short = f'{indicator}_14'
        signal_long = f'{indicator}_50'
        signal = f'{indicator}_14'
        oversold = 25
        overbought = 70

        # self.data[trade_equity] = 0
        # self.data[trade_equity][0] = TI.init_money

        prev_act = ACTION.NOTHING

        for i in range(self.data.shape[0]):
            if prev_act is ACTION.NOTHING:
                if self.data[signal][i] >= overbought:
                    self.data['rsi_pos'][i] = ACTION.SHORT.value
                    entry_idx = i+1
                    prev_act = ACTION.SHORT
                elif self.data[signal][i] <= oversold:
                    self.data['rsi_pos'][i] = ACTION.LONG.value
                    entry_idx = i+1
                    prev_act = ACTION.LONG
                else:
                    self.data['rsi_pos'][i] = ACTION.NOTHING.value
            elif prev_act is ACTION.SHORT:
                if self.data['pnl'][entry_idx:i+1].sum() <= -50:
                    self.data['rsi_pos'][i] = ACTION.NOTHING.value
                    prev_act = ACTION.NOTHING
                elif self.data['pnl'][entry_idx:i+1].sum() >= 15:
                    self.data['rsi_pos'][i] = ACTION.NOTHING.value
                    prev_act = ACTION.NOTHING
                elif self.data[signal][i] <= oversold:
                    self.data['rsi_pos'][i] = ACTION.LONG.value
                    entry_idx = i+1
                    prev_act = ACTION.LONG
                else:
                    self.data['rsi_pos'][i] = ACTION.SHORT.value
            elif prev_act is ACTION.LONG:
                if self.data['pnl'][entry_idx:i+1].sum() >= 50:
                    self.data['rsi_pos'][i] = ACTION.NOTHING.value
                    prev_act = ACTION.NOTHING
                elif self.data['pnl'][entry_idx:i+1].sum() <= -15:
                    self.data['rsi_pos'][i] = ACTION.NOTHING.value
                    prev_act = ACTION.NOTHING
                elif self.data[signal][i] >= overbought:
                    self.data['rsi_pos'][i] = ACTION.SHORT.value
                    entry_idx = i+1
                    prev_act = ACTION.SHORT
                else:
                    self.data['rsi_pos'][i] = ACTION.LONG.value

        # self.data.loc[self.data[signal_short] > 60, [trade_pos]] = 1
        # self.data.loc[self.data[signal_short] < 60, [trade_pos]] = -1
        self.data[trade_pnl] = self.data[trade_pos].shift(1)*self.data['pnl']
        self.data[trade_equity] = 0
        self.data[trade_equity][0] = TI.init_money
        self.data[trade_equity][1:] = self.data[trade_pnl][1:]
        self.data[trade_equity] = self.data[trade_equity].cumsum()

    def cal_equity(self, strategies):
        for strategy in strategies:
            trade_pnl = f'{strategy}_pnl'
            trade_pos = f'{strategy}_pos'
            trade_equity = f'{strategy}_equity'
            trade_return = f'{strategy}_return'
            self.data[trade_pnl] = self.data[trade_pos].shift(
                1)*self.data['pnl']
            self.data[trade_equity] = 0
            self.data[trade_equity][0] = TI.init_money
            self.data[trade_equity][1:] = self.data[trade_pnl][1:]
            self.data[trade_equity] = self.data[trade_equity].cumsum()
            self.data[trade_return] = self.data[trade_equity].pct_change()
            sharpe_ratio = np.sqrt(
                252) * (self.data[trade_return].mean() / self.data[trade_return].std())
            print(f'{strategy}: {sharpe_ratio}')
