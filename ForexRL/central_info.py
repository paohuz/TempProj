from facilities import Helper, Slice_set
from cust_enum import MODE_OPERATION, SLICE_SET_TYPE, DATASET_TYPE, STRATEGY, AGENT, ACTION
# from backtest.strategy import Strategy_ma_crossover


class Mode_info:
    mode_operation = MODE_OPERATION.PREP_DATASET


class Path_info:

    version = 0

    data_path = Helper.File_manipulation.data_path(f'./data/')
    data_csv_path = Helper.File_manipulation.data_path(f'{data_path}csv/')
    data_arr_path = Helper.File_manipulation.data_path(f'{data_path}arr/')

    model_path = Helper.File_manipulation.data_path(f'./model/')
    backtest_path = Helper.File_manipulation.data_path(f'./report/backtest/')


class Network_info:
    agent = AGENT.PG

    rl_file = f'{Path_info.model_path}data.csv'

    rl_episode = 3
    action_space = [ACTION.NOTHING, ACTION.LONG, ACTION.SHORT]
    action_space_len = len(action_space)

    class Pg_info:
        discount_factor = 0.99
        learning_rate = 5*1e-4


class Data_info:
    raw_file = Helper.File_manipulation.data_file(
        f'{Path_info.data_csv_path}EURUSD2000_30min.csv')

    raw_date_format = '%d-%m-%y %H:%M'
    feature_date_format = '%Y-%m-%d %H:%M:%S'
    arr_date_format = '%Y-%m-%d %H:%M:%S'
    raw_index_col = 0
    feature_index_col = 0
    arr_index_col = 0

    feature_set = 'all'
    arr_set = 'test_arr'
    slice_set_dict = {
        'all': Slice_set(SLICE_SET_TYPE.ALL),
        'test_feature': Slice_set(SLICE_SET_TYPE.START_LEFT, start=4, len=100),
        'test_arr': Slice_set(SLICE_SET_TYPE.START_RIGHT, start=1000, len=1000),
    }

    dataset_type = DATASET_TYPE.D1

    feature_path = Helper.File_manipulation.data_path(
        f'{Path_info.data_csv_path}{feature_set}/')
    # arr_path = Helper.File_manipulation.data_path(
    #     f'{Path_info.data_csv_path}{arr_set}/')
    feature_file = f'{feature_path}data.csv'

    arr_path = Helper.File_manipulation.data_path(
        f'{Path_info.data_arr_path}{arr_set}/{dataset_type.value}/')
    arr_file = f'{arr_path}data.csv'
    trade_file = f'{arr_path}trade_info.csv'

    backtest_path = Helper.File_manipulation.data_path(
        f'{Path_info.backtest_path}{arr_set}/{dataset_type.value}/')
    backtest_file = f'{backtest_path}backtest.csv'

    rl_path = Helper.File_manipulation.data_path(
        f'{Path_info.model_path}{arr_set}/{dataset_type.value}/')
    rl_file = f'{rl_path}rl_{Network_info.agent.value}'

    float_cols = ['Open', 'High', 'Low', 'Close']
    feature_cols = ['Open', 'High', 'Low', 'Close']
    norm_main = ['Open', 'High', 'Low', 'Close']
    main_col = 'Close'

    feature_synth = False

    window_hist_dim = (2, 5)
    window_future_dim = (2)


class Trade_info:
    contract = 10000
    init_money = 10000

# class Strategy_info:
#     strategies = [Strategy_ma_crossover(40, 252)]


class Synthesis_feature:
    pnl = True
    ma = [40, 252]
    # ma = [40, 60]
    rsi = [14, 50]
    macd = [40, 252]
