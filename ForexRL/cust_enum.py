from enum import Enum

# This represents as master type


class MODE_OPERATION(Enum):
    PREP_FEATURE = 'prepare_feature'
    PREP_ARR = 'prepare_arr'
    PREP_DATASET = 'prepare_dataset'
    TRAIN_PRED = 'train_prediction'
    TRAIN_RL = 'train_rl'
    TEST_RL = 'test_rl'


class SLICE_SET_TYPE(Enum):
    ALL = 0
    START_LEFT = 1
    START_RIGHT = -1


class DATASET_TYPE(Enum):
    D1 = '1d'
    D2 = '2d'
    D3 = '3d'


class ACTION(Enum):
    NOTHING = 0
    LONG = 1
    SHORT = -1


class AGENT(Enum):
    PG = 'pg'
    AC = 'ac'
    DQN = 'dqn'


class INDICATOR(Enum):
    MA = 'ma'
    RSI = 'rsi'


class STRATEGY(Enum):
    BH = 'bh'  # buy and hold
    SH = 'sh'  # sell and hold
    MA = 'ma'  # moving average crossover
    RSI = 'rsi'  # RSI threshold
    PG = 'pg'  # policy gradient
