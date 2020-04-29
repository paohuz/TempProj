from facilities import Helper
from cust_enum import MODE_OPERATION
from central_info import Path_info as PI, Data_info as DI, Mode_info as MI, Trade_info as TI, Synthesis_feature as SF
import talib
import numpy as np


class Prep_data:
    def load_data(self):
        raise NotImplementedError('load_data() must be defined in subclass')

    def prep_data(self):
        raise NotImplementedError('prep_data() must be defined in subclass')

    @staticmethod
    def get_float_cols(include_synth=False):
        features = DI.float_cols.copy()
        if include_synth:
            if SF.pnl:
                features.append('pnl')

            for ma in SF.ma:
                features.append(f'ma_{ma}')

            for rsi in SF.rsi:
                features.append(f'rsi_{rsi}')

            for macd in SF.macd:
                features.append(f'macd_{macd}')

        return features

    @staticmethod
    def get_features(include_synth=False):
        features = DI.feature_cols.copy()
        if include_synth:
            if SF.pnl:
                features.append('pnl')

            for ma in SF.ma:
                features.append(f'ma_{ma}')

            for rsi in SF.rsi:
                features.append(f'rsi_{rsi}')

            for macd in SF.macd:
                features.append(f'macd_{macd}')

        return features


class Prep_data_feature(Prep_data):
    def load_data(self):
        self.data = Helper.File_manipulation.load_data_csv(
            DI.raw_file, DI.raw_date_format, DI.raw_index_col)
        self.data = self.data[DI.slice_set_dict[DI.feature_set]
                              .start:DI.slice_set_dict[DI.feature_set].end]
        self.data[DI.float_cols] = self.data[DI.float_cols].astype(float)

    def prep_data(self):
        if SF.pnl:
            self.data['pnl'] = TI.contract*(self.data[DI.main_col] -
                                            self.data[DI.main_col].shift(1))/self.data[DI.main_col].shift(1)
        for val in SF.ma:
            self.data[f'ma_{val}'] = self.data[DI.main_col].rolling(
                window=val).mean()

        for val in SF.rsi:
            self.data[f'rsi_{val}'] = talib.RSI(
                self.data[DI.main_col].values, timeperiod=val)

        for val in SF.macd:
            macd, macdsignal, macdhist = talib.MACD(
                self.data[DI.main_col].values, signalperiod=val)
            self.data[f'macd_{val}'] = macd

        self.data.to_csv(DI.feature_file)


class Pre_data_arr(Prep_data):

    def validate_data_feature(self):
        if not Helper.File_manipulation.check_array_files([DI.feature_file]):
            prep_data_obj = Prep_data_feature()
            prep_data_obj.load_data()
            prep_data_obj.prep_data()

    def load_data(self):

        self.validate_data_feature()
        self.float_cols = self.get_float_cols(DI.feature_synth)
        self.features = self.get_features(DI.feature_synth)
        self.data = Helper.File_manipulation.load_data_csv(
            DI.feature_file, DI.feature_date_format, DI.feature_index_col)
        self.data = self.data[DI.slice_set_dict[DI.arr_set]
                              .start:DI.slice_set_dict[DI.arr_set].end]
        self.data[self.float_cols] = self.data[self.float_cols].astype(float)
        self.data_len = self.data.shape[0]
        self.data.to_csv(DI.arr_file)

    def prep_data(self):
        raise NotImplementedError('prep_data() must be defined in subclass')
        # for feature in self.features:
        #     arr_hist = []
        #     for i in range(DI.window_hist_dim, self.data_len-DI.window_future_dim+1):
        #         arr_hist.append(self.data[DI.main_col][i-DI.window_hist_dim:i])
        #     Helper.File_manipulation.save_array(
        #         f'{DI.arr_path}{feature}.npy', arr_hist)

        # arr_future = []
        # for i in range(DI.window_hist_dim, self.data_len-DI.window_future_dim+1):
        #     arr_future.append(self.data[DI.main_col][i:i+DI.window_hist_dim])
        # Helper.File_manipulation.save_array(f'{DI.arr_path}future_{DI.main_col}.npy', arr_hist)


class Prep_data_arr_1D(Pre_data_arr):
    def prep_data(self):

        window_hist = DI.window_hist_dim[-1]

        self.data[window_hist-1:self.data_len -
                  DI.window_future_dim].to_csv(DI.trade_file)
        self.data = self.data[self.features]
        arr_hist = []
        arr_hist_norm = []
        for i in range(window_hist, self.data_len-DI.window_future_dim+1):
            feature_hist = []
            feature_hist_norm = []
            base = self.data[DI.main_col][i-window_hist]
            for feature in DI.norm_main:
                feature_hist.extend(
                    self.data[feature][i-window_hist:i].values)
                feature_hist_norm.extend(
                    (self.data[feature][i-window_hist:i].values-base)/base)

            for feature in list(set(self.features) - set(DI.norm_main)):
                feature_hist.extend(
                    self.data[feature][i-window_hist:i].values)
                base = self.data[feature][0]
                feature_hist_norm.extend(
                    (self.data[feature][i-window_hist:i].values-base)/base)

            arr_hist.append(feature_hist)
            arr_hist_norm.append(feature_hist_norm)

        arr_hist = np.array(arr_hist)
        arr_hist_norm = np.array(arr_hist_norm)

        Helper.File_manipulation.save_array(f'{DI.arr_path}hist.npy', arr_hist)
        Helper.File_manipulation.save_array(
            f'{DI.arr_path}hist_norm.npy', arr_hist_norm)

        with open(f'{DI.arr_path}features.txt', "w") as file:
            for feature in DI.norm_main:
                file.write(f'{feature}\n')
            for feature in list(set(self.features) - set(DI.norm_main)):
                file.write(f'{feature}\n')

        # for feature in self.features:
        #     arr_hist = []
        #     for i in range(DI.window_hist_dim, self.data_len-DI.window_future_dim+1):
        #         arr_hist.append(self.data[DI.main_col][i-DI.window_hist_dim:i])
        #     Helper.File_manipulation.save_array(f'{DI.arr_path}{feature}.npy', arr_hist)

        arr_future = []
        arr_future_norm = []
        for i in range(window_hist, self.data_len-DI.window_future_dim+1):
            base = self.data[DI.main_col][i]
            arr_future.append(self.data[DI.main_col]
                              [i:i+DI.window_future_dim].values)
            arr_future_norm.append(
                (self.data[DI.main_col][i:i+DI.window_future_dim].values-base)/base)

        arr_future = np.array(arr_future)
        arr_future_norm = np.array(arr_future_norm)
        Helper.File_manipulation.save_array(
            f'{DI.arr_path}future_{DI.main_col}.npy', arr_future)
        Helper.File_manipulation.save_array(
            f'{DI.arr_path}future_{DI.main_col}_norm.npy', arr_future_norm)


class Prep_data_arr_2D(Pre_data_arr):
    def prep_data(self):
        window_hist = DI.window_hist_dim[-1]
        self.data[window_hist-1:self.data_len -
                  DI.window_future_dim].to_csv(DI.trade_file)
        self.data = self.data[self.features]
        arr_hist = []
        arr_hist_norm = []
        for i in range(window_hist, self.data_len-DI.window_future_dim+1):
            feature_hist = []
            feature_hist_norm = []
            base = self.data[DI.main_col][i-window_hist]
            # feature_hist.append([feature_hist, self.data[DI.norm_main][i-DI.window_hist_dim:i].values])
            # feature_hist_norm.append([feature_hist_norm, (self.data[DI.norm_main][i-DI.window_hist_dim:i].values-base)/base])
            for feature in DI.norm_main:
                feature_hist.append(
                    self.data[feature][i-window_hist:i].values)
                feature_hist_norm.append(
                    (self.data[feature][i-window_hist:i].values-base)/base)

            for feature in list(set(self.features) - set(DI.norm_main)):
                feature_hist.append(
                    self.data[feature][i-window_hist:i].values)
                base = self.data[feature][0]
                feature_hist_norm.append(
                    (self.data[feature][i-window_hist:i].values-base)/base)

            feature_hist = np.swapaxes(feature_hist, 0, 1)
            feature_hist_norm = np.swapaxes(feature_hist_norm, 0, 1)
            arr_hist.append(feature_hist)
            arr_hist_norm.append(feature_hist_norm)

        arr_hist = np.array(arr_hist)
        arr_hist_norm = np.array(arr_hist_norm)

        Helper.File_manipulation.save_array(f'{DI.arr_path}hist.npy', arr_hist)
        Helper.File_manipulation.save_array(
            f'{DI.arr_path}hist_norm.npy', arr_hist_norm)

        with open(f'{DI.arr_path}features.txt', "w") as file:
            for feature in DI.norm_main:
                file.write(f'{feature}\n')
            for feature in list(set(self.features) - set(DI.norm_main)):
                file.write(f'{feature}\n')

        # for feature in self.features:
        #     arr_hist = []
        #     for i in range(DI.window_hist_dim, self.data_len-DI.window_future_dim+1):
        #         arr_hist.append(self.data[DI.main_col][i-DI.window_hist_dim:i])
        #     Helper.File_manipulation.save_array(f'{DI.arr_path}{feature}.npy', arr_hist)

        arr_future = []
        arr_future_norm = []
        for i in range(window_hist, self.data_len-DI.window_future_dim+1):
            base = self.data[DI.main_col][i]
            arr_future.append(self.data[DI.main_col]
                              [i:i+DI.window_future_dim].values)
            arr_future_norm.append(
                (self.data[DI.main_col][i:i+DI.window_future_dim].values-base)/base)

        arr_future = np.array(arr_future)
        arr_future_norm = np.array(arr_future_norm)
        Helper.File_manipulation.save_array(
            f'{DI.arr_path}future_{DI.main_col}.npy', arr_future)
        Helper.File_manipulation.save_array(
            f'{DI.arr_path}future_{DI.main_col}_norm.npy', arr_future_norm)


class Prep_data_arr_3D(Pre_data_arr):
    def prep_data(self):

        window_time = DI.window_hist_dim[0]
        window_hist = DI.window_hist_dim[1]

        self.data[window_hist+window_time-2:self.data_len -
                  DI.window_future_dim].to_csv(DI.trade_file)
        self.data = self.data[self.features]

        arr_hist = []
        arr_hist_norm = []

        for i in range(window_hist, self.data_len-DI.window_future_dim+1-window_time+1):
            feature_hist_time = []
            feature_hist_time_norm = []
            for j in range(window_time):
                feature_hist = []
                feature_hist_norm = []
                base = self.data[DI.main_col][i-window_hist+j]
                # feature_hist.append([feature_hist, self.data[DI.norm_main][i-DI.window_hist_dim:i].values])
                # feature_hist_norm.append([feature_hist_norm, (self.data[DI.norm_main][i-DI.window_hist_dim:i].values-base)/base])
                for feature in DI.norm_main:
                    feature_hist.append(
                        self.data[feature][i-window_hist+j:i+j].values)
                    feature_hist_norm.append(
                        (self.data[feature][i-window_hist+j:i+j].values-base)/base)

                for feature in list(set(self.features) - set(DI.norm_main)):
                    feature_hist.append(
                        self.data[feature][i-window_hist+j:i+j].values)
                    base = self.data[feature][0]
                    feature_hist_norm.append(
                        (self.data[feature][i-window_hist+j:i+j].values-base)/base)

                feature_hist = np.swapaxes(feature_hist, 0, 1)
                feature_hist_norm = np.swapaxes(feature_hist_norm, 0, 1)

                feature_hist_time.append(feature_hist)
                feature_hist_time_norm.append(feature_hist_norm)
            arr_hist.append(feature_hist_time)
            arr_hist_norm.append(feature_hist_time_norm)

        arr_hist = np.array(arr_hist)
        arr_hist_norm = np.array(arr_hist_norm)

        Helper.File_manipulation.save_array(f'{DI.arr_path}hist.npy', arr_hist)
        Helper.File_manipulation.save_array(
            f'{DI.arr_path}hist_norm.npy', arr_hist_norm)

        with open(f'{DI.arr_path}features.txt', "w") as file:
            for feature in DI.norm_main:
                file.write(f'{feature}\n')
            for feature in list(set(self.features) - set(DI.norm_main)):
                file.write(f'{feature}\n')

        # for feature in self.features:
        #     arr_hist = []
        #     for i in range(DI.window_hist_dim, self.data_len-DI.window_future_dim+1):
        #         arr_hist.append(self.data[DI.main_col][i-DI.window_hist_dim:i])
        #     Helper.File_manipulation.save_array(f'{DI.arr_path}{feature}.npy', arr_hist)

        arr_future = []
        arr_future_norm = []
        for i in range(window_hist+window_time-1, self.data_len-DI.window_future_dim+1):
            base = self.data[DI.main_col][i]
            arr_future.append(self.data[DI.main_col]
                              [i:i+DI.window_future_dim].values)
            arr_future_norm.append(
                (self.data[DI.main_col][i:i+DI.window_future_dim].values-base)/base)

        arr_future = np.array(arr_future)
        arr_future_norm = np.array(arr_future_norm)
        Helper.File_manipulation.save_array(
            f'{DI.arr_path}future_{DI.main_col}.npy', arr_future)
        Helper.File_manipulation.save_array(
            f'{DI.arr_path}future_{DI.main_col}_norm.npy', arr_future_norm)


class Prep_dataset(Prep_data):
    def load_data(self):
        self.float_cols = self.get_float_cols(True)
        self.features = self.get_features(True)
        self.data = Helper.File_manipulation.load_data_csv(
            DI.trade_file, DI.arr_date_format, DI.arr_index_col)
        self.data[self.float_cols] = self.data[self.float_cols].astype(float)
        self.data = self.data[self.features]
        self.data_len = self.data.shape[0]

        self.dataset = {}
        # for feature in self.features:
        #     self.dataset[feature] = Helper.File_manipulation.load_array(
        #         f'{DI.arr_path}{feature}.npy')

        self.dataset['hist'] = Helper.File_manipulation.load_array(
            f'{DI.arr_path}hist.npy')
        self.dataset['hist_norm'] = Helper.File_manipulation.load_array(
            f'{DI.arr_path}hist_norm.npy')

        self.dataset[f'future_{DI.main_col}'] = Helper.File_manipulation.load_array(
            f'{DI.arr_path}future_{DI.main_col}.npy')
        self.dataset[f'future_{DI.main_col}_norm'] = Helper.File_manipulation.load_array(
            f'{DI.arr_path}future_{DI.main_col}_norm.npy')

    def prep_data(self):
        print('hist')
        print(self.dataset['hist'].shape)
        print('hist_norm')
        print(self.dataset['hist_norm'].shape)
        print(f'future_{DI.main_col}')
        print(self.dataset[f'future_{DI.main_col}'].shape)
        print(f'future_{DI.main_col}_norm')
        print(self.dataset[f'future_{DI.main_col}_norm'].shape)
