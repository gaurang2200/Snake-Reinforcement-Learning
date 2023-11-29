"""
Created on Sat Oct 28 21:10:02 2023
@author: Gaurang Gupta
"""

import pygame as pg
import numpy as np
from Snake_Machine import Machine, Direction
from random import randint
pg.init()

# Game Controls
width = 20
height = 20
speed = 30
MANUAL = False

# Colors
black_color = (0, 0, 0)
white_color = (255, 255, 255)
red_color = (255, 0, 0)
grey_color = (20, 20, 20)

# Main Window
cell_size = 20
episodes = 1000
win = pg.display.set_mode((width*cell_size, height*cell_size))
pg.display.set_caption("Snake Game")
    

class Snake:
    def __init__(self):
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 1
        self.grid = np.zeros((width+5, height+5))
        self.x = np.array([int(width/2)])
        self.y = np.array([int(height/2)])
        self.length = 1
        self.food_x = 0
        self.food_y = 0
        self.makeFood()
    
    def drawSnake(self):
        self.grid = np.zeros((width+5, height+5))
        for (i, j) in zip(self.x, self.y):
            pg.draw.rect(win, white_color, (cell_size*i, cell_size*j, cell_size, cell_size), 0, 5)
            self.grid[i, j] = -10
    
    def moveSnake(self, direction):
        if direction == Direction.LEFT and self.speed_x == 0:
            self.speed_x = -abs(self.speed)
            self.speed_y = 0
        elif direction == Direction.RIGHT and self.speed_x == 0:
            self.speed_x = abs(self.speed)
            self.speed_y = 0
        elif direction == Direction.UP and self.speed_y == 0:
            self.speed_y = -abs(self.speed)
            self.speed_x = 0
        elif direction == Direction.DOWN and self.speed_y == 0:
            self.speed_y = abs(self.speed)
            self.speed_x = 0
        
        if self.length > 1:
            for i in range(self.length-1, 0, -1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
        
        self.x[0] += self.speed_x
        self.y[0] += self.speed_y

    
    def eatFood(self):
        self.x = np.append(self.x, self.food_x)
        self.y = np.append(self.y, self.food_y)
        self.length += 1
        self.makeFood()
    
    def isBody(self, x, y):
        for (i, j) in zip(self.x, self.y):
            if x == i and y == j:
                return True
        return False
    
    def makeFood(self):
        while True:
            x = randint(0, width - 1)
            y = randint(0, height - 1)
            found = False
            for (i, j) in zip(self.x, self.y):
                if x == i and y == j:
                    found = True
            if not found:
                self.food_x, self.food_y = x, y
                return
              
    def drawFood(self):
        self.grid[self.food_x, self.food_y] = 1
        pg.draw.rect(win, red_color, (self.food_x*cell_size, self.food_y*cell_size, cell_size, cell_size))
    
    def checkGameOver(self):
        if self.x[0] < 0 or self.y[0] < 0 or self.x[0] >= width or self.y[0] >= height:
            return True
        
        for i in range(1, self.length):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                print("Self colliding")
                return True
        if self.length == width * height:
            return True
        return False



def initializeGame():
    global width, height, snake, ai
    snake = Snake()
    ai = Machine(snake, width, height)
    ai.q_table = np.loadtxt("./assets/Q_table_3000.txt")
    resetGame()


def resetGame():
    global snake, ai, run, direction
    run = True
    direction = 0
    ai.playGame()
    snake.__init__()
    #ai.getState()
    #print(ai.q_table)


def startGame():
    global run, direction
    for episode in range(episodes):
        while run:
            pg.time.delay(110 - speed)
            win.fill(grey_color)
            snake.drawSnake()
            snake.drawFood()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            
            keys = pg.key.get_pressed()
            
            if keys[pg.K_q]:
                run = False
            
            if MANUAL:
                if (keys[pg.K_LEFT] or keys[pg.K_a]):
                    direction = Direction.LEFT
                elif (keys[pg.K_RIGHT] or keys[pg.K_d]):
                    direction = Direction.RIGHT
                elif (keys[pg.K_UP] or keys[pg.K_w]):
                    direction = Direction.UP
                elif (keys[pg.K_DOWN] or keys[pg.K_s]):
                    direction = Direction.DOWN
                snake.moveSnake(direction)
                if snake.checkGameOver():
                    resetGame()
                if snake.x[0] == snake.food_x and snake.y[0] == snake.food_y:
                    snake.eatFood()
            else :
                if ai.gameOver:
                    resetGame()
                ai.moveDirection()
            
            #drawGrid()
            pg.display.update()
    

def drawGrid():
    # Horizontal Lines
    for i in range(0, height*cell_size, cell_size):
        pg.draw.line(win, white_color, (0, i), (width*cell_size, i))
    
    # Vertical Lines
    for i in range(0, width*cell_size, cell_size):
        pg.draw.line(win, white_color, (i, 0), (i, height*cell_size))
    



initializeGame()
startGame()

pg.quit()