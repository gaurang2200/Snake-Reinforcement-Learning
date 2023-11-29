"""
Created on Sun Oct 29 23:29:01 2023
@author: gupta
"""

import numpy as np
from enum import Enum
import random

class Direction(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4


class Machine:
    def __init__(self, snake, width, height):
        self.episodes = 1
        self.iterations = 1
        self.num_iterations = 1000
        self.snake = snake
        self.width = width
        self.height = height
        self.gameOver = False
        # 25 - grid info and 4 - food info
        self.coverage = 3
        self.total = (self.coverage * self.coverage) + 4
        self.q_table = np.zeros((2**self.total, 4))
        self.random_num = 1
        self.state = 0
        
        self.rewards = []
        self.episode_reward = 0
        self.learning_rate = 0.1
        self.discount_rate = 0.90
        
        self.exploration_rate = 0.9
        self.max_exploration_rate = 1
        self.min_exploration_rate = 0.05
        self.exploration_decay_rate = 0.01
        
    
    def playGame(self):
        self.gameOver = False
        self.iterations = 1
        self.episode_reward = 0
        self.random_num = random.random()
        if self.random_num > self.exploration_rate:
            print(str(self.episodes) + "\tExploiting the game...")
            #print(str(self.q_table))
        else:
            print(str(self.episodes) + "\tExploring the game...")
            self.exploration_rate = self.min_exploration_rate + (self.max_exploration_rate - self.min_exploration_rate) * np.exp(-self.exploration_decay_rate * self.episodes)
        self.episodes += 1
        self.state = self.getState()
        np.savetxt("Q_table.txt", self.q_table)
    
    def moveDirection(self):
        if self.random_num > self.exploration_rate:
            self.exploitation()
        else:
            self.exploration()
    
    
    def getStep(self):
        return self.getState(), self.getReward()
    
    
    def getState(self):
        state = 0
        l = self.snake.x[0]
        r = self.snake.y[0]
        diff = int(self.coverage / 2)
        #print(str(l) + '\t' + str(r) + '\t' + str(self.snake.food_x) + '\t' + str(self.snake.food_y))
        
        for i in range(l-diff, l-diff+self.coverage):
            for j in range(r-diff, r-diff+self.coverage):
                bit = ((i-(l-diff)) * self.coverage) + (j-(r-diff))
                if i >= 0 and i < self.width and j >= 0 and j < self.height:
                    if self.snake.isBody(i, j):
                        state |= (1 << (self.total - bit - 1))
                else:
                    state |= (1 << (self.total - bit - 1))
        
                #print(str(self.total) + '\t' + str(bit) + '\t' + str(state & (1 << (self.total - bit - 1))))
                
        # Last 4 bits are for food directions
        # ...0-Left, 0-Up, 0-Right, 0-Down
        if l > self.snake.food_x:
            state |= (1 << 3)
        elif l < self.snake.food_x:
            state |= (1 << 1)
            
        if r > self.snake.food_y:
            state |= (1 << 2)
        elif r < self.snake.food_y:
            state |= (1 << 0)
        # 6print("Current State: " + str(bin(state)))
        return state
        
    
    def getAction(self, isExploration):
        directions = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]
        action = None
        self.iterations += 1
        if isExploration:
            action = random.choice(directions)
        else:
            action = Direction(np.argmax(self.q_table[self.state,:])+1)
        
        self.snake.moveSnake(action)
        action = action.value - 1
        new_state, reward = self.getStep()
        # Bellman Equation
        # q_new = (1-learning_rate)*q_old + learning_rate*(R_t+1 + discount_rate*max_q(s', a'))
        self.q_table[self.state,action] = ((1-self.learning_rate)*self.q_table[self.state,action]) + (self.learning_rate*(reward+(self.discount_rate*np.max(self.q_table[new_state,:]))))
        self.state = new_state
        self.episode_reward += reward
    
    
    def getReward(self):
        reward = 0
        if self.iterations >= self.num_iterations or self.snake.checkGameOver():
            reward = -10
            self.gameOver = True
        if self.iterations % 10 == 0:
            reward = -1
        if self.snake.x[0] == self.snake.food_x and self.snake.y[0] == self.snake.food_y:
            reward = 1
            self.snake.eatFood()
        return reward
    
    
    def exploitation(self):
        self.getAction(False)
        return
    
    
    def exploration(self):
        self.getAction(True)
        return

'''
# Markov Decision Processes (MDPs)
Environment
Agent -> Decision Maker
States -> All possible states of the Environment
Actions -> All the actions that can be taken in the environment
Reward -> All the rewards the agent can receive by taking an action in the environment
Goal -> Maximise the cummulative reward till the end


Exploration vs Exploitation
Epsilon Greedy Strategy - 



'''


