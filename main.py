#!/usr/bin/env python
# HeadsUp Mark 2 - uses parametric means to create Tiles that serve information to headsup displays
# Code by C.Barrett
# Designed by S.Caem

# First we import all the modules necessary for this project.
import pygame
import pygame.gfxdraw
import os
import time

# This module will be useful when I reinstate system vitals.
from getvitals import *

# Initiate Pygame and the Font engine.
pygame.init()
pygame.font.init()

# Here are some basic colours we can call on.
background = (38,38,38)
textc = (128,128,128)
buttonc = (51,51,51)
displayc = (64,64,64)
indicatorc = (80,80,80)
indicatorhigh = (255,255,255)
red = (150,50,0)
green = (106,255,69)
blue = (99,157,255)
yellow = (255,221,5)
black = (0,0,0)
white = (255,255,255)

# Here is the location of our font.
titleFont = "assets/slimjoe.otf"

# set the screen resolution. Since the program is resolution independant it can be given a variety of view sizes.

#screenSize = (640,480)
screenSize = (1280,720)

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

# the following function maps a value from the target range onto the desination range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# the following class draws graphs with or without outlines and updates values everytime it is called.
class GraphLine(object):
    
    def __init__(self,xLeft,yTop,xRight,yBottom,line):
        self.line = line
        self.lineoffset = line/2
        self.yTop = yTop + self.lineoffset
        self.yBottom = yBottom - self.lineoffset
        self.xLeft = xLeft + self.lineoffset
        self.xRight = xRight - self.lineoffset

        
        self.ySpan = abs(self.yTop - self.yBottom)
        self.xSpan = abs(self.xLeft - self.xRight)
        self.yMid = (self.ySpan / 2) + self.yTop
        self.graphData = self.grablist()
    
    # the following function returns the list.
    def grablist(self):
        
        self.glist = []

        for i in range(self.xSpan):
            self.glist.append(self.yBottom)
            
        return self.glist
    
    # the following appends data to the list.
    def updatelist(self,data):
        #grabs a simple 15 wide tuple for our values
        #puts a new sensor value at the end 
        self.buffer.append(data)
        #pop the oldest value off
        self.buffer.pop(0)
    
    # the following pairs the list of values with coordinates on the X axis. The supplied variables are the starting X coordinates and spacing between each point.    
    def graphprep(self,list):
        linepoint = self.xLeft
        jump = 1      
        self.newlist = []
        for i in range(self.xSpan):
            self.newlist.append((linepoint,list[i]))
            linepoint = linepoint + jump
    
        return self.newlist
    
    def update(self,surface,data,dataLow,dataHigh,colour):
        # Because the graph screen is slow to update it needs to pop a reading onto screen as soon as it is initiated I draw a value once and wait for the interval to lapse for the next draw. Once the interval has lapsed pop another value on screen.
        #Sets a black screen ready for our UI elements      
        #surface.fill(black)

        #self.graphlabel = Label()
        #self.intervallabel = Label()
        #self.intervallabelshadow = Label()
        
        

        #self.slider1 = Image()
        
        
        #gets our data
        self.SenseData = data
        
        #converts data to float
        self.Data = float(self.SenseData)
        #scales the data to the limits of our screen
        self.DataGraph = translate(self.Data, dataLow, dataHigh, self.yBottom, self.yTop)
        #grabs a simple 61 wide tuple for our values
        self.DataBuffer = self.grablist()
        
        
        #puts a new sensor value at the end 
        self.graphData.append(self.DataGraph)
        #pop the oldest value off
        self.graphData.pop(0)
        
        #preps the list by adding the X coordinate to every sensor value
        DataCords = self.graphprep(self.graphData   )
        #DataSlide = translate(self.SenseData, dataLow, dataHigh, self.yBottom, self.yTop)
        #slider1.update(sliderb, 283, DataSlide)
        
        #draw the lines
        
        pygame.draw.lines(surface, colour, False, DataCords, (self.line - 1))
        
        pygame.draw.lines(surface, colour, False, ((self.xLeft,self.yTop),(self.xRight,self.yTop),(self.xRight,self.yBottom),(self.xLeft,self.yBottom),(self.xLeft,self.yTop)), self.line)

# this is a function that returns text at the proper dimensions to fit a rectangle.
def dynamic_font(text, name, size, color, width, aa=True, dec_by=1):
    font = pg.font.Font(name, size)
    if font.size(text)[0] > width:
        return dynamic_font(text, name, size-dec_by, color, width, aa, dec_by)
    return font.render(text, aa, color)
    
# This class controls our tiles. 
class Tile(object):
    def __init__(self,title,surface,screenSize,colour,index):

        self.title = title        
        self.surface = surface
        self.screenspanx,self.screenspany = screenSize 
        self.x = self.screenspanx * .10
        self.y = self.screenspany * .13
        self.seamadj = .05
        self.titlesizeadj = .15
        self.index = index
        self.colour = colour

        self.update()


    def update(self):

        self.seam = self.screenspanx * self.seamadj
        self.titlesize = int(self.screenspany * self.titlesizeadj)
        self.spanX  = self.screenspanx - (self.x*2)
        self.spanY = self.screenspany - (self.y*2)
        self.tilejump = self.seam + self.spanX

        if self.index > 0:
            self.x = self.x + ((self.seam + self.spanX) * self.index)

        self.innerX = self.x + (self.spanX * .05)
        self.innerY = self.y + (self.spanY * .05)
        self.inSpanX  = self.spanX - ((self.spanX * .05)*2)
        self.inSpanY = self.spanY - ((self.spanY * .05)*2)

        self.pos = (self.x,self.y)
        self.inpos = (self.innerX,self.innerY)
        self.size = (self.spanX,self.spanY)
        self.innersize = (self.inSpanX,self.inSpanY)

    def addelement(self):
        pass

    def draw(self,page):
        #if page > 0:
        self.pos = (self.x - (self.tilejump * page)),self.y
        self.innerX = (self.x - (self.tilejump * page)) + (self.spanX * self.seamadj)
        #else:
            #self.pos = self.x,self.y

        #draw the background of the tile
        rect = pygame.Rect(self.pos, self.size)
        pygame.draw.rect(self.surface, self.colour, rect)

        #draw the foreground elements of the tile.
        title = Label()
        title.update(self.title,self.titlesize,self.innerX,self.innerY,titleFont,textc)
        title.draw(self.surface)

# This class draws our page indicator circles.
class Indicator(object):        
    def __init__(self,surface,screenSize):
        self.surface = surface
        self.xadj = .122  
        self.yadj = .025
        self.spaceadj = .007
        self.marginadj = .088
        self.screenX,self.screenY = screenSize
        self.margin = self.screenY * self.marginadj
        self.spanX = self.screenX * self.xadj
        self.spanY = self.screenY * self.yadj
        self.space = self.screenX * self.spaceadj
        self.rad = self.spanY / 2
        self.centerposy = (self.screenY - self.margin)
        self.centerposx = (self.screenX / 2)
        
    def update(self, page):
        if page > 0:
            pass
    
    def draw(self,page):
        
        indicolours = []
        
        for n in range(4):
            if n == page:
                indicolours.append(white)
            else:
                indicolours.append(indicatorc)
        
        testx = int(self.centerposx - (self.space/2) - (self.rad*2) - self.space - self.rad)
        testy = int(self.centerposy)
        
        pygame.gfxdraw.aacircle(self.surface,testx,testy,int(self.rad),indicolours[0])
        pygame.gfxdraw.filled_circle(self.surface,testx,testy,int(self.rad),indicolours[0])
        
        testx2 = int((self.centerposx - (self.space/2) - (self.rad*2) - self.space - self.rad) + (self.rad *2) + self.space)
        
        pygame.gfxdraw.aacircle(self.surface,testx2,testy,int(self.rad),indicolours[1])
        pygame.gfxdraw.filled_circle(self.surface,testx2,testy,int(self.rad),indicolours[1])
        
        
        testx3 = int(testx2 + (self.rad *2) + self.space)
        
        pygame.gfxdraw.aacircle(self.surface,testx3,testy,int(self.rad),indicolours[2])
        pygame.gfxdraw.filled_circle(self.surface,testx3,testy,int(self.rad),indicolours[2])
        
        testx4 = int(testx3 + (self.rad *2) + self.space)
        
        pygame.gfxdraw.aacircle(self.surface,testx4,testy,int(self.rad),indicolours[3])
        pygame.gfxdraw.filled_circle(self.surface,testx4,testy,int(self.rad),indicolours[3])

# The following class is used to display text
class Label(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = white
        self.fontSize = 33
        self.myfont = pygame.font.Font(titleFont, self.fontSize)
        
    def update(self, content, fontSize, nx, ny, fontType, color):
        self.x = nx
        self.y = ny
        self.content = content
        self.fontSize = fontSize
        self.myfont = pygame.font.Font(fontType, self.fontSize)
        self.color = color
        
    def draw(self, surface):
        label = self.myfont.render(self.content, 1, self.color)
        surface.blit(label, (self.x, self.y))

# the following class is used to display images
class Image(object):
    def __init__(self):
        self.x = 258
        self.y = 66
        self.Img = blueInsignia
        
    def update(self, image, nx, ny):
        self.x = nx
        self.y = ny
        self.Img = image

        
    def draw(self, surface):
        surface.blit(self.Img, (self.x,self.y))

# the following class is used to draw rectangles.
class Box(object):
    def __init__(self):
        self.x=0
        self.y=0
        self.vx=1
        self.vy=1
        self.size=(50,50)
        self.color=(0,0,255)
        
    def update(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
    
    def draw(self, surface):
        rect = pygame.Rect((self.x,self.y), self.size)
        pygame.draw.rect(surface, self.color, rect)

# The following class describes our scene and handles the general operation of our program.
class Scene(object):
    def __init__(self,tiles,size):
        self.notiles = tiles
        self.screenSize = size
        
    def update(self,page):
        pass

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

ScreenX,ScreenY = screenSize


tile1 = Tile("Home",surface,screenSize,background,0)
tile2 = Tile("System",surface,screenSize,background,1)
tile3 = Tile("Assistant",surface,screenSize,background,2)  
tile4 = Tile("Notes",surface,screenSize,background,3)   
indicator1 = Indicator(surface,screenSize)

page = 0
selector = 0
speed = .1


while(status != "quit"):

    
    #page = selector
    
    if page < selector:
        page += speed
        
    if page > selector:
        page -= speed
        
    
    print "page = " + str(page)
    
    print "selector = " +  str(selector)

    surface.fill(black)
    tile1.draw(page)
    tile2.draw(page)
    tile3.draw(page)
    tile4.draw(page)
    
    indicator1.draw(selector)
    pygame.display.flip()
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selector -= 1
            if event.key == pygame.K_RIGHT:
                selector += 1
    
    pygame.time.wait(15)
    
    # this next item checks to see if the q key was pressed 
    #key = pygame.key.get_pressed()
    
    #if key[pygame.K_RIGHT]:
        #selector += 1
    #if key[pygame.K_LEFT]:
        #selector -= 1
        
    #if key[pygame.K_q]:

        #status = "quit"
    #else:
        ## otherwise it updates the status by calling on the startUp function, which is passed our pygame display object, and the time since we booted our program.
        #status = "go!"
