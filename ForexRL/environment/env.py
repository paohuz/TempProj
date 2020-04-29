from facilities import Helper
from cust_enum import MODE_OPERATION, DATASET_TYPE, ACTION
from central_info import Path_info as PI, Data_info as DI, Mode_info as MI, Trade_info as TI, Synthesis_feature as SF
from environment.prep_data import Prep_data_feature, Prep_data_arr_1D, Prep_data_arr_2D, Prep_data_arr_3D, Prep_dataset
from backtest.backtest import Backtest

import talib
import numpy as np


class Env:

    # def test(self):
    #     print(DI.raw_file)

    def prep_data(self):
        if MI.mode_operation == MODE_OPERATION.PREP_FEATURE:
            self.prep_data_obj = Prep_data_feature()
        elif MI.mode_operation == MODE_OPERATION.PREP_ARR:
            if DI.dataset_type == DATASET_TYPE.D1:
                self.prep_data_obj = Prep_data_arr_1D()
            if DI.dataset_type == DATASET_TYPE.D2:
                self.prep_data_obj = Prep_data_arr_2D()
            if DI.dataset_type == DATASET_TYPE.D3:
                self.prep_data_obj = Prep_data_arr_3D()
        elif MI.mode_operation == MODE_OPERATION.PREP_DATASET:
            self.prep_data_obj = Prep_dataset()
        elif MI.mode_operation == MODE_OPERATION.TRAIN_RL:
            pass

        self.prep_data_obj.load_data()
        self.prep_data_obj.prep_data()

        self.dataset_len = self.prep_data_obj.dataset['hist_norm'].shape[0]

        self.backtest = Backtest(self.prep_data_obj.data)
        self.backtest.build_trading_signal_rl()

    def reset(self):
        self.idx = 0
        self.done = False
        self.reward = 0
        self.last_action = ACTION.NOTHING

        return self.prep_data_obj.dataset['hist_norm'][self.idx]

    def cal_reward(self):
        pass

    def open_pos(self):
        self.entry_idx = self.idx
        self.reward = 1

    def close_pos(self):
        self.reward = self.last_action.value * \
            self.prep_data_obj.data['pnl'][self.entry_idx:self.idx].sum()

    def det_action(self, action):
        self.curr_action = ACTION(action)
        if self.last_action == ACTION.NOTHING:
            if self.curr_action is not ACTION.NOTHING:
                self.open_pos()
        elif self.last_action == ACTION.LONG:
            if self.curr_action is not ACTION.NOTHING:
                self.close_pos()
            elif self.curr_action is not ACTION.SHORT:
                self.close_pos()
                self.open_pos()
        elif self.last_action == ACTION.SHORT:
            if self.curr_action is not ACTION.NOTHING:
                self.close_pos()
            elif self.curr_action is not ACTION.LONG:
                self.close_pos()
                self.open_pos()

        self.last_action = self.curr_action

    def step(self, action):
        self.det_action(action)

        self.backtest.rl_strategy.update_trading_signal(
            self.idx, self.curr_action)

        next_state = None

        if not self.done:
            self.idx += 1
            next_state = self.prep_data_obj.dataset['hist_norm'][self.idx]

        if not self.done and self.idx >= self.dataset_len-1:
            self.done = True

        return next_state, self.reward, self.done
