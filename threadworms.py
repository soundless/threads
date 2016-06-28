#!/usr/bin/env python

import sys
import random
import pygame
import threading

from pygame.locals import *

# setup contants
NUM_WORMS = 24
FPS = 30
CELL_SIZE = 20
CELLS_WIDE = 36
CELLS_HIGH = 24

GRID = []
for x in range(CELLS_WIDE):
    GRID.append([None] * CELLS_HIGH)

GRID_LOCK = threading.Lock()

# contants for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK
GRID_LINES_COLOR = DARKGRAY

WINDOW_WIDTH = CELL_SIZE * CELLS_WIDE
WINDOW_HEIGHT = CELL_SIZE * CELLS_HIGH

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0
BUTT = -1

# global variable that the worm threads check to see if they should exit.
WORMS_RUNNING = True

class Worm(threading.Thread):
    def __init__(self, name='Worm', maxsize=None, color=None, speed=None):
        threading.Thread.__init__(self)
        self.name = name

        # set the maxsize to the parameter, or to a random maxsize
        if maxsize is None:
            self.maxsize = random.randint(4, 10)
            # Have a small chance of a super long worm
            if random.randint(0, 4) == 3:
                self.maxsize += random.randint(10, 16)
        else:
            self.maxsize = maxsize

        # set the color to the parameter, or set to a random color
        if color is None:
            self.color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        else:
            self.color = color

        # set the speed to the parameter, or set to a random number
        if speed is None:
            self.speed = random.randint(30, 1000)
        else:
            self.speed = speed

        GRID_LOCK.acquire()

        startx = starty = 0
        while True:
            startx = random.randint(0, CELLS_WIDE - 1)
            starty = random.randint(0, CELLS_HIGH - 1)
            if GRID[startx][starty] is None:
                break

        GRID[startx][starty] = self.color

        GRID_LOCK.release()

        self.body =  [{'x': startx, 'y': starty}]
        self.direction = self.selectNewDirection()
        
    
    def run(self):

        while True:
            if not WORMS_RUNNING:
                return

            if random.randint(0, 100) < 50:
                self.direction = self.selectNewDirection()

            # thread code goes here
            GRID_LOCK.acquire()

            nextx, nexty = self.getNextPosition()
            if nextx in (-1, CELLS_WIDE) or nexty in (-1, CELLS_HIGH) or GRID[nextx][nexty]:
                self.direction = self.getNewDirection()

                if not self.direction:
                    self.body.reverse()
                    self.direction = self.getNewDirection()

                if self.direction:
                    nextx, nexty = self.getNextPosition()

            if self.direction:
                #print nextx, nexty
                GRID[nextx][nexty] = self.color
                self.body.insert(0, {'x':nextx, 'y':nexty})

                if len(self.body) > self.maxsize:
                    GRID[self.body[BUTT]['x']][self.body[BUTT]['y']] = None
                    del self.body[BUTT]
            else:
                self.direction = self.selectNewDirection()

            # some code that read or modifies GRID
            GRID_LOCK.release()

            pygame.time.wait(self.speed)

    def selectNewDirection(self):
        return random.choice((UP, DOWN, LEFT, RIGHT))

    def getNextPosition(self):
        x = self.body[HEAD]['x']
        y = self.body[HEAD]['y']

        if self.direction == UP:
            nextx = x
            nexty = y - 1
        elif self.direction == DOWN:
            nextx = x
            nexty = y + 1
        elif self.direction == LEFT:
            nextx = x - 1
            nexty = y
        elif self.direction == RIGHT:
            nextx = x + 1
            nexty = y
        else:
            assert False, 'Bad value for self.direction: %s' % self.direction

        return nextx, nexty


    def getNewDirection(self):
        x = self.body[HEAD]['x']
        y = self.body[HEAD]['y']

        newDirection = []
        if y-1 not in (-1, CELLS_HIGH) and GRID[x][y-1] is None:
            newDirection.append(UP)
        if y+1 not in (-1, CELLS_HIGH) and GRID[x][y+1] is None:
            newDirection.append(DOWN)
        if x-1 not in (-1, CELLS_WIDE) and GRID[x-1][y] is None:
            newDirection.append(LEFT)
        if x+1 not in (-1, CELLS_WIDE) and GRID[x+1][y] is None:
            newDirection.append(RIGHT)

        if newDirection == []:
            return None

        return random.choice(newDirection)


def main():
    global FPSC_LOCK, DISPLAY_SURF


    # Draw some walls on the grid
    squares = """
.................................
.................................
.................................
.....H..H..EEE..L....L.....OO....
.....H..H..E....L....L....O..O...
.....HHHH..EE...L....L....O..O...
.....H..H..E....L....L....O..O...
.....H..H..EEE..LLL..LLL...OO....
.................................
.....W.....W...OO...RRR..MM.MM...
.....W.....W..O..O..R.R..M.M.M...
.....W..W..W..O..O..RR...M.M.M...
.....W..W..W..O..O..R.R..M...M...
......WW.WW....OO...R.R..M...M...
.................................
.................................
"""
    setGridSquares(squares)

    # Pygame window set up
    pygame.init()
    FPSC_LOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Thread Worms')

    # Create the worm objects
    worms = []
    for i in range(NUM_WORMS):
        worms.append(Worm())
        worms[-1].start()

    while True:
        handleEvents()
        drawGrid()
        pygame.display.update()
        FPSC_LOCK.tick(FPS)

def handleEvents():
    global WORMS_RUNNING

    for event in pygame.event.get():
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            WORMS_RUNNING = False
            pygame.quit()
            sys.exit()

def drawGrid():
    DISPLAY_SURF.fill(BGCOLOR)
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(DISPLAY_SURF, GRID_LINES_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(DISPLAY_SURF, GRID_LINES_COLOR, (0, y), (WINDOW_WIDTH, y))

    GRID_LOCK.acquire()
    for x in range(0, CELLS_WIDE):
        for y in range(0, CELLS_HIGH):
            if GRID[x][y] is None:
                continue

            color = GRID[x][y]

            # Draw the body segment on the screen
            darkerColor = (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0))
            pygame.draw.rect(DISPLAY_SURF, darkerColor, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(DISPLAY_SURF, color, (x * CELL_SIZE + 2, y * CELL_SIZE + 2, CELL_SIZE - 4 , CELL_SIZE - 4))

    GRID_LOCK.release()

def setGridSquares(squares, color=(255, 255, 255)):
    squares = squares.split("\n")
    if squares[0] == '':
        del squares[0]
    if squares[-1] == '':
        del squares[-1]

    GRID_LOCK.acquire()

    for y in range(min(len(squares), CELLS_HIGH)):
        for x in range(min(len(squares[y]), CELLS_WIDE)):
            if squares[y][x] == ' ':
                GRID[x][y] = None
            elif squares[y][x] == '.':
                pass
            else:
                GRID[x][y] = color

    GRID_LOCK.release()


if __name__ == '__main__':
    main()