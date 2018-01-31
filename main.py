#!/usr/bin/env python

"""

    HeadsUp

    Code by C.Barrett
    Designed by S.Caem

    This file controls the overall flow of the program.

"""


# First we import all the modules necessary for this project.
import pygame
import pygame.gfxdraw
import os
import time
from tiles import *
# This module will be useful when I reinstate system vitals.

# Initiate Pygame and the Font engine.
pygame.display.init()
pygame.font.init()


# set the screen resolution. Since the program is resolution independant it can be given a variety of view sizes.

#screenSize = (640,480)
screenSize = (1280,720)

logo = pygame.image.load('assets/logo.png')
pygame.display.set_icon(logo)

# We activate some pygame parameters. Colour depth, and hide mouse.
modes = pygame.display.list_modes(16)
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.mouse.set_visible(0)


# instantiate a pygame display with the name "surface". 

#surface = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
surface = pygame.display.set_mode(screenSize)
pygame.display.set_caption('HeadsUp')

# Set the state value.
status = "go!"

# define the screensize as a tuple (two number set)
ScreenX,ScreenY = screenSize

# create a list to hold our tile objects
tilelist = []

# This number determines the number of tiles
notiles = 6


# the following variables help store and control animation behaviour.

# page stores the actual in focus tile
page = 0

# selector stores the desired in focus tile.
selector = 0

# speed determines the pixel jumps each step.
speed = 20


#need to find a way to move tiles using integers
messageback = "none"


# This class handles our page indicator circles.
class Indicator(object):        
    def __init__(self,surface,screenSize,notiles):
        
        # collect the screensize
        self.screenX,self.screenY = screenSize
        
        # collect the number of tiles
        self.notiles = notiles

        # collect the surface, physical layout paramaters (gap between circles, total spans)
        self.surface = surface

        self.space = 10
        self.spanY = 10
        self.spanX = ((self.spanY + self.space) * self.notiles) - self.space
        self.margin = 40

        # collect the physical parameters for the circles.
        self.rad = self.spanY / 2
        self.centerposy = (self.screenY - self.margin)
        self.centerposx = (self.screenX / 2)


    # This function draws the indicator circles.
    
    def draw(self,page):
        
        # creates a list to define the colours of each circle, so as to tell the user which page we are on
        indicolours = []
        
        # for loop to define and draw each circle
            
        for i in range(self.notiles):
            
            # if the current circle is the same number as the page we are on light it up, indicating that we are now on that tile.
            if i == page:
                indicolours.append(white)
            else:
                indicolours.append(indicatorc)
                
            # the adjust factor controls spacing of each circle. It is the product of the diameter of the circle plus the size of the space between them, times the circle we're at.
            adjust = ((self.spanY + self.space) * i)
            
            # the center point of each circle along the X is the product of half the screen size minus half the size of the widget plus the radius of the circle.
            circlex = (1280 / 2) - (self.spanX / 2) + adjust + self.rad
            
            circlex = int(circlex)
            circley = int(self.centerposy)
            
            
            pygame.gfxdraw.aacircle(self.surface,circlex,circley,int(self.rad),indicolours[i])
            pygame.gfxdraw.filled_circle(self.surface,circlex,circley,int(self.rad),indicolours[i])



# The following class is to handle interval timers.
class timer(object):

    # Constructor code logs the time it was instantiated.    
    def __init__(self):
        self.timeInit = time.time()
        self.logtime()

    # The following funtion returns the first logged value.        
    def timestart(self):
        return self.timeInit

    # the following function updates the time log with the current time.
    def logtime(self):
        self.lastTime = time.time()

    # the following function returns the interval that has elapsed since the last log.        
    def timelapsed(self):
        self.timeLapse = time.time() - self.lastTime
        #print(self.timeLapse)
        return self.timeLapse


# for loop to create our tiles and put them in our list of tiles
for i in range(notiles):
    tile = Tile(i,surface,screenSize,background,i)
    tilelist.append(tile)


# we make an indicator object, these are the "dots" that tell the user what tile they're on
# we pass it our surface object, our screensize, and the number of tiles in our scene.
indicator1 = Indicator(surface,screenSize,notiles)

# the following objects are interval timers that regulate the drawing of various interface elements.
interval = timer()
graphtime = timer()


# The following is the mainloop.
while(status != "quit"):

    
    # In the scene the Tiles physical positions are maintained by the selectorAdj variable.
    # an integer (selector) determines the tile that should be shown from 0-max amount of tiles.
    # this integer is then (selectorAdj) multiplied by 100 to allow the tiles to be shifted in pixels each tick.
    # the actual position of the tiles is held by the page variable.
    selectorAdj = selector * 100

    # We wait for a timer to elapse
    if (interval.timelapsed() >= .001):

        # reset the interval timer
        interval.logtime()

        # the following if statement checks if the page is higher or lower than the selectorAdj variable. 
        
        # If it's higher, we increment page
        if page < selectorAdj:
            page = page + speed
            
        # if it's lowers, we decrement.
        if page > selectorAdj:
            page = page - speed


    #------------------Begin screen drawing portion------------------

    # fill the background with black
    surface.fill(black)

    # for loop to draw each of the tiles in our tile list. We pass it the page so they can draw themselves to the right location.
    for i in range(notiles):
        tilelist[i].draw(page)

    #draw our indicator circles.
    indicator1.draw(selector)

    # define the midpoint of the screen.
    mid = 1280/2

    # puke all those pixels to screen.
    pygame.display.flip()

    # keyinto lets us know which tile is presently selected, so that key evens can be sent to the right tile.
    keyinto = int(float(page) / 100)


    # input control handling. Get a list of most recent events.
    for event in pygame.event.get():
        # if quit was triggered make ready to quit.
        if event.type == pygame.QUIT:
            status = "quit"
        # otherwise if it was a keypress
        elif event.type == pygame.KEYDOWN:
            
            # if it was left decrement the selector
            if event.key == pygame.K_LEFT:
                if tilelist[keyinto].isview():
                    tilelist[keyinto].leftkey()
                else:
                    selector -= 1
                    if selector < 0:
                        selector = 0
                        
            # if it was right increment the selector
            if event.key == pygame.K_RIGHT:
                if tilelist[keyinto].isview():
                    tilelist[keyinto].rightkey()
                else:
                    selector += 1
                    if selector > (notiles - 1):
                        selector = (notiles - 1)
                        
            if event.key == pygame.K_DOWN:
                tilelist[keyinto].downkey()
            if event.key == pygame.K_UP:
                tilelist[keyinto].upkey()
            if event.key == pygame.K_RETURN:
                messageback = tilelist[keyinto].enterkey(status)
            if event.key == pygame.K_q:
                pygame.quit()
                quit()

    if messageback == "quit":
        print("messageback received")
        pygame.quit()
        quit()

    pygame.time.wait(30)

