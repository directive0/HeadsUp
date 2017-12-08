#!/usr/bin/env python

"""

HeadsUp Mark 7 -  Tiles that serve information to a headsup display, send and recieve arbitrary IFTTT

    Code by C.Barrett
    Designed by S.Caem

Exciting developments:

    -Finally got IFTTT working


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



page = 0
selector = 0
speed = 20
director = 0


#need to find a way to move tiles using integers
messageback = "none"

# this is a function that returns text at the proper dimensions to fit a rectangle.
def dynamic_font(text, name, size, color, width, aa=True, dec_by=1):
    font = pg.font.Font(name, size)
    if font.size(text)[0] > width:
        return dynamic_font(text, name, size-dec_by, color, width, aa, dec_by)
    return font.render(text, aa, color)

# This class draws our page indicator circles.
class Indicator(object):        
    def __init__(self,surface,screenSize,notiles):
        
        # needs to take number of tiles into account, 
        #find the size of itself, 
        #position itself centered and draw all the indicators. 
        self.screenX,self.screenY = screenSize
        self.notiles = notiles
        self.surface = surface
        self.space = 10
        self.spanY = 10
        self.margin = 40
        self.spanX = ((self.spanY + self.space) * self.notiles) - self.space

        self.rad = self.spanY / 2
        self.centerposy = (self.screenY - self.margin)
        self.centerposx = (self.screenX / 2)
        
        # the width of the indicator widget = ((diameter of circle + gap) * notiles)-gap 
        # this gives us the total width of the widget
        self.widgetx = ()
        
    def update(self, page):
        if page > 0:
            pass
    
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

def center(text,font,size):
    pass
    
# The following class describes our scene and handles the general operation of our program.
class Scene(object):
    def __init__(self,tiles,size):
        self.notiles = tiles
        self.screenSize = size
        
    def update(self,page):
        pass
        
        
# The following class is to handle interval timers.
class timer(object):

    # Constructor code logs the time it was instantiated.    
    def __init__(self):
        self.timeInit = time.time()
        self.logtime()

    # The following funtion returns the last logged value.        
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
         
         
def vitalshow():
    info = sensorget()
    title = Label()
    title.update("LOCAL",60,84,170,titleFont,red)
    title.draw(surface)
    
    cpulabel = Label()
    cpulabel.update("CPU % = " + info['cpuperc'],50,84,300,titleFont,red)
    cpulabel.draw(surface)
    
    ramlabel = Label()
    ramlabel.update("RAM % = " + info['ramperc'],50,84,370,titleFont,red)
    ramlabel.draw(surface)


# for loop to create our tiles and put them in our list of tiles
for i in range(notiles):
    tile = Tile(i,surface,screenSize,background,i)
    tilelist.append(tile)

        
# we make an indicator object.    
indicator1 = Indicator(surface,screenSize,notiles)

# the following objects control interval timing for the graphs and something else... I think? hmmmmm.
interval = timer()
graphtime = timer()

while(status != "quit"):

    
    # page = selector
    # following mess of code moves the tiles into the correct position.
    selectorAdj = selector * 100
    
    if (interval.timelapsed() >= .001):

        
        interval.logtime()
        
        if page < selectorAdj:
            page = page + speed
        
        if page > selectorAdj:
            page = page - speed
        
    #print("selector adjust is:")    
    #print(selectorAdj)
    #print("page is:")
    #print(page)
    #print(page)

    
   # if page < 0:
   #     page  = 0


    # print "page = " + str(page)
    # print "selector = " +  str(selector)
    
    # we begin the screen drawing of the loop
    
    # fill the background black
    surface.fill(black)
    
    # for loop to draw each of the objects in our object list.
    for i in range(notiles):
        tilelist[i].draw(page)
    
    #draw our indicator circles.
    indicator1.draw(selector)
    
    # define the midpoint of the screen.
    mid = 1280/2
    
    
    # puke all those pixels to screen.
    pygame.display.flip()
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

