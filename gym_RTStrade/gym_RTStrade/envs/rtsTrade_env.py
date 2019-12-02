import gym
import random
from gym import spaces
class rtsTrade_env(gym.Env):
    def __init__(self):
        
        self.nbars_obs = 40
        self.nbars_game = 40 #also check in def reset
        self.counter = 0
        self.action_space = spaces.Discrete(3)    
        self.observation_space = spaces.Box(low=0, high=4000000,shape=(40,4))
        self.net = 0
        self.prev_action = -1
        self.returns = []
        print('v1.11')

    def data_init(self,df_train,df_valid,df_test):
        
        self.df = df_train
        self.df_train = df_train
        self.df_valid = df_valid
        self.df_test = df_test
    
    def step(self, action):
        
        reward = self._take_action(action)  
        self.returns.append(reward)
        self.net += reward
        self.current_pos += 1  
        self.counter += 1
        done = False
        if self.counter >= self.nbars_game:
            done = True
            self.counter = 0
        
        if self.current_pos >= (len(self.df)):
            done = True
            self.counter = 0
        
        obs = self.df.iloc[self.current_pos-self.nbars_obs:self.current_pos] 
        return obs, reward, done, {}
    
    def _take_action(self,action):
        entry_price = self.df.iloc[self.current_pos]['Open']
        close_price = self.df.iloc[self.current_pos]['Close']
        prev_close = self.df.iloc[self.current_pos-1]['Close']
        if (self.prev_action!=action):
            if action == 0:
                reward = entry_price-close_price - 10
            if action == 1:
                reward = -1
            if action == 2:
                reward = close_price-entry_price - 10 
        else:
            if action == 0:
                reward = prev_close-close_price 
            if action == 1:
                reward = -1
            if action == 2:
                reward = close_price-prev_close         
        self.prev_action = action
        return reward
        
    def reset(self):
        self.df = self.df_train
        self.nbars_game=40      
        self.counter = 0
        self.net = 0
        self.prev_action = -1
        self.returns = []
        self.current_pos = random.randint(self.nbars_obs , len(self.df.loc[:, 'Open'].values) - self.nbars_game)  
        frame = self.df.iloc[self.current_pos-self.nbars_obs:self.current_pos]
        
        return frame
    
    def reset_to_trainScore(self):
        self.df = self.df_train
        self.current_pos = self.nbars_obs   
        self.counter = 0
        self.net = 0
        self.returns = []
        self.prev_action = -1
        frame = self.df.iloc[self.current_pos-self.nbars_obs:self.current_pos]        
        self.nbars_game=400000
       
        return frame
    
    def reset_to_validScore(self):
        self.df = self.df_valid
        self.current_pos = self.nbars_obs  
        self.counter = 0
        self.net = 0
        self.returns = []
        self.prev_action = -1
        frame = self.df.iloc[self.current_pos-self.nbars_obs:self.current_pos]        
        self.nbars_game=400000
        
        return frame
    
    def reset_to_testScore(self):
        self.df = self.df_test
        self.current_pos = self.nbars_obs  
        self.counter = 0
        self.net = 0
        self.returns = []
        self.prev_action = -1
        frame = self.df.iloc[self.current_pos-self.nbars_obs:self.current_pos]        
        self.nbars_game=400000
        
        return frame


    def render(self, mode='human', close=False):
        pass

