
# , Strategy_info as SI
from central_info import Data_info as DI, Synthesis_feature as SF, Trade_info as TI
from cust_enum import ACTION, STRATEGY
import matplotlib.pyplot as plt
import numpy as np

from backtest.strategy import Buy_hold, Sell_hold, Strategy_ma_crossover, Strategy_rsi_threshold, Strategy_rl_pg


class Backtest:
    def __init__(self, data):
        self.data = data
        self.strategies = [
            Buy_hold(),
            Sell_hold(),
            Strategy_ma_crossover(40, 252),
            # Strategy_rsi_threshold(14, 25, 70, 50, 15)
        ]

        self.rl_strategy = Strategy_rl_pg(build_signal_auto=False)

    def build_trading_signal_rl(self):
        self.rl_strategy.build_trading_signal(self.data)

    def backtest(self):
        self.strategies.append(self.rl_strategy)
        for strategy in self.strategies:
            strategy.run_backtest(self.data)

        self.plot_equity()
        self.plot_action()
        self.plot_bar_summary()
        self.data.to_csv(DI.backtest_file)

    def plot_bar_summary(self):

        labels = []
        sharpe_ratio = []
        mmd = []
        for strategy in self.strategies:
            labels.append(strategy.name_strategy)
            sharpe_ratio.append(strategy.sharpe_ratio)
            mmd.append(strategy.mmd)

        x = np.arange(len(labels))
        width = 0.35  # the width of the bars
        fig, ax = plt.subplots(2, 1)
        rects1 = ax[0].plot(x, sharpe_ratio, width, label='sharpe ratio')
        rects2 = ax[1].plot(x, mmd, width, label='mmd')

        # ax.set_ylabel('Scores')
        ax[0].set_title('sharpe_ratio')
        ax[0].set_xticks(x)
        ax[0].set_xticklabels(labels)
        ax[0].legend()
        ax[1].set_title('mmd')
        ax[1].set_xticks(x)
        ax[1].set_xticklabels(labels)
        ax[1].legend()
        fig.tight_layout()
        plt.show()

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
