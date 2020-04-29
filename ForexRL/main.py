from environment.env import Env
from cust_enum import MODE_OPERATION, AGENT
from central_info import Mode_info as MI, Data_info as DI, Network_info as NI
from backtest.backtest import Backtest
import numpy as np


class App:
    def __init__(self):
        self.env = Env()

    def choose_agent(self):
        if NI.agent == AGENT.PG:
            from agent.agent_pg import Agent_pg as Agent

        return Agent

    def set_up(self):
        self.env.prep_data()
        if MI.mode_operation == MODE_OPERATION.PREP_FEATURE or MI.mode_operation == MODE_OPERATION.PREP_ARR:
            exit()

        Agent = self.choose_agent()
        self.agent = Agent(
            self.env.prep_data_obj.dataset['hist_norm'].shape[1])
        # print(self.env.prep_data_obj.dataset['hist_norm'].shape)
        # print(self.env.prep_data_obj.dataset[f'future_{DI.main_col}'].shape)
        #
        # self.backtest.backtest()
        # print(self.env.data)

    def learn_pg(self):
        score_history = []
        for e in range(NI.rl_episode):
            done = False
            score = 0
            observation = self.env.reset()
            while not done:
                action = self.agent.choose_action(observation)
                observation_, reward, done = self.env.step(action)
                self.agent.store_transition(observation, action, reward)
                observation = observation_
                score += reward
            score_history.append(score)

            print(f'train: {e}')
            self.agent.learn()

            print(
                f'episode {e} score {score:.1f} average_score {np.mean(score_history[-100:])}')
        filename = 'fname.png'

    def backtest(self):
        self.env.backtest.backtest()


app = App()
app.set_up()
app.learn_pg()
app.backtest()
