# HeadsUp Tiles
# Code by C.Barrett
# Design by S.Caem

# To do 
# Integrate file system 
# integrate Notes
# integrat 

import pygame
import pygame.gfxdraw
import os
import time
from datetime import datetime
from getvitals import *
from filehandling import *
from textrect import *

# Here are some basic colours we can call on.
background = (38,38,38)
textc = (128,128,128)
buttonc = (51,51,51)
buttoncmute = (26,26,26)
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
titleFont = "assets/font.ttf"

# the following function maps a value from the target range onto the desination range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def gettextsize():
    # give it a string
    # give it a size
    # return the width required for that text.
    pass
    
    
    
# the following class draws graphs with or without outlines and updates values everytime it is called.
class GraphLine(object):
    
    def __init__(self,xLeft,yTop,xRight,yBottom,line,title):
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
        self.title = title
        self.label = Label()
        self.readout = Label()
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
        DataCords = self.graphprep(self.graphData)
        #DataSlide = translate(self.SenseData, dataLow, dataHigh, self.info["y"]Bottom, self.info["y"]Top)
        #slider1.update(sliderb, 283, DataSlide)
        
        #draw the lines
        labelposy,labelposx = (self.yTop+20),(self.xLeft+25)
        readoutposx = self.xRight - 100
        content = str(data) + "%"
        pygame.draw.lines(surface, colour, False, DataCords, self.line)
        self.label.update(self.title, 26, labelposx, labelposy, titleFont, textc)
        self.readout.update(content, 26, readoutposx, labelposy, titleFont, textc)
        textsize = self.readout.getrect()
        textpos = self.xRight - textsize[0] - 13
        self.readout.update(content, 26, textpos, labelposy, titleFont, textc)
        self.label.draw(surface)
        self.readout.draw(surface)
        #pygame.draw.lines(surface, colour, False, ((self.xLeft,self.yTop),(self.xRight,self.yTop),(self.xRight,self.yBottom),(self.xLeft,self.yBottom),(self.xLeft,self.yTop)), self.line)


# The following class is used to display text
class Label(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = white
        self.fontSize = 88
        self.myfont = pygame.font.Font(titleFont, self.fontSize)
        text = "hello"
        self.size = self.myfont.size(text)

        
    def update(self, content, fontSize, nx, ny, fontType, color):
        self.x = nx
        self.y = ny
        self.content = content
        self.fontSize = fontSize
        self.myfont = pygame.font.Font(fontType, self.fontSize)
        self.color = color
        
    def center(self,w,h,x,y):
        size = self.getrect()
        xmid = x + w/2
        ymid = y + h/2
        textposx = xmid - (size[0]/2)
        textposy = ymid - (size[1]/2)
        self.update(self.content,self.fontSize,textposx,textposy,titleFont,self.color)
    
    def paragraph(self):
        
        my_rect = pygame.Rect((0, 0, 804, 366))
    
        rendered_text = render_textrect(self.content, self.myfont, my_rect, textc, buttonc, 0)
        return rendered_text
        
    def getrect(self):
        label = self.myfont.render(self.content, 1, self.color)
        textw = label.get_width()
        texth = label.get_height()
        
        return textw,texth
        
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
        surface.blit(self.Img, (self.info["x"],self.info["y"]))

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

class viewingarea(object):
    def __init__(self, content, info):
        self.content = content
        self.info = info
        self.textarea = Label()
        self.surface = self.info["surface"]
        self.substrate = Box()
        self.substrate.update(200,120,(880, 440),buttonc)
    
    def drawbutton(self,y,content):
        butxmid = self.info["dispbx"] + (self.info["dispw"] / 2)  
        butymid = y + (40 / 2)  
        self.drawblock(y,40)
        butlabel = Label()
        butlabel.update(content,26,butxmid,y,titleFont,textc)
        size = butlabel.getrect()
        butlabel.center(self.info["dispw"],40,self.info["dispbx"],y)
        #textposx = butxmid - (size[0]/2)
        #textposy = butymid - (size[1]/2)qq
        
        #butlabel.update(content,26,textposx,textposy,titleFont,textc)
        butlabel.draw(self.surface)
    
    def draw(self):
        self.substrate.draw(self.surface)
        self.textarea.update(self.content,26,0,0,titleFont,textc)
        self.surface.blit(self.textarea.paragraph(), (240,160))
        

class actionarea(object):
    def __init__(self,info):
        self.info = info
        self.textbox = Box()
        self.surface = self.info["surface"]
        self.type = self.info["tiletype"]
        self.selector = 0
        self.selectmax = 5
    
    def outline(self,xLeft,xRight,yTop,yBottom,line):
        pygame.draw.lines(self.surface, textc, False, ((xLeft,yTop),(xRight,yTop),(xRight,yBottom),(xLeft,yBottom),(xLeft,yTop)), line)
        
    def selectoralign(self):
        if self.selector > self.selectmax:
            self.selector = self.selectmax
        if self.selector < 0:
            self.selector = 0
            
    def downkey(self):
        self.selector += 1
        self.selectoralign()
        
    def upkey(self):
        self.selector -= 1
        self.selectoralign()
    
    def enterkey(self):
        return self.selector
        # when receives key down send action area message who will send display area a message?
        # maybe just send message to display area directly?

        
    def getdatetime(self):
        date = datetime.today()
        datestr = date.ctime()
        datelist = datestr.split()
        
        self.time = datelist[3]
        self.day = datelist[0]
        self.month = datelist[1]
        self.dayno = datelist[2]
        self.year = datelist[4]
        self.date = self.day + " - " + str(self.dayno) + "/" + str(self.month) + "/" + str(self.year)
        
    def drawblock(self,y,h):
        rect = pygame.Rect((self.info["innerx"],y), (self.info["actareaw"],h))
        pygame.draw.rect(self.surface, buttonc, rect)
        
    def drawbutton(self,y,content):
        butxmid = self.info["innerx"] + (self.info["aaspanx"] / 2)  
        butymid = y + (40 / 2)  
        self.drawblock(y,40)
        butlabel = Label()
        butlabel.update(content,26,butxmid,y,titleFont,textc)
        size = butlabel.getrect()
        textposx = butxmid - (size[0]/2)
        textposy = butymid - (size[1]/2)
        
        butlabel.update(content,26,textposx,textposy,titleFont,textc)
        butlabel.draw(self.surface)
        
    def draw(self,info):
        self.info = info

        if self.type == 0:
            # Home Tile Action area
            
            # get time and date
            self.getdatetime()
            #draw the back of the action area for time and date
            
            for i in range(2):

                ypos = self.info["actareay"] + (100*i)
                height = 80 + (100*i)
                self.drawblock(ypos,height)

            
            # instantiate the label for the time line
            timel = Label()
            timel.update(self.time,26,(self.info["innerx"]+155),(self.info["actareay"]+7),titleFont,textc)
            size = timel.getrect()
            labelpos = self.info["innerx"]+(self.info["aaspanx"]/2)-(size[0]/2)
            timel.update(self.time,26,labelpos,(self.info["actareay"]+7),titleFont,textc)
            timel.draw(self.surface)
            
            # instantiate the label for the date line
            datel = Label()
            datel.update(self.date,26,(self.info["innerx"]+92),(self.info["actareay"]+40),titleFont,textc)
            size = datel.getrect()
            labelpos = self.info["innerx"]+(self.info["aaspanx"]/2)-(size[0]/2)
            datel.update(self.date,26,labelpos,(self.info["actareay"]+40),titleFont,textc)
            datel.draw(self.surface)
            
        # draw system screen actionable buttons and highlight    
        if self.type == 1:
            buttontexts = ["Shutdown","Reboot","Toggle Wifi", "Toggle Bluetooth", "Quit HeadsUP"]
            self.selectmax = 4
            for i in range(5):
                
                ypos = self.info["actareay"] + (60*i)
                self.drawbutton(ypos,buttontexts[i])
                if i == self.selector:
                    self.outline(self.info["innerx"],(self.info["innerx"] + self.info["aaspanx"]),ypos,(ypos+40),3)
        
        if self.type == 2:
            buttontexts = ["Invoke Assistant", "Toggle Hotword"]
            self.selectmax = 1
            for i in range(2):
                
                ypos = self.info["actareay"] + (60*i)
                self.drawbutton(ypos,buttontexts[i])
                if i == self.selector:
                    self.outline(self.info["innerx"],(self.info["innerx"] + self.info["aaspanx"]),ypos,(ypos+40),3)
        
        # Define layout for Notes Tiles
        if self.type == 3:
            buttontexts = ["View","Up","Down", "Refresh List", "Delete"]
            self.selectmax = 4
            for i in range(5):
                ypos = self.info["actareay"] + (60*i)
                self.drawbutton(ypos,buttontexts[i])
                if i == self.selector:
                    self.outline(self.info["innerx"],(self.info["innerx"] + self.info["aaspanx"]),ypos,(ypos+40),3)


    
class displayarea(object):
    def __init__(self,info):
        self.selector = 0
        self.info = info
        self.surface = self.info["surface"]
        self.type = self.info["tiletype"]
        if self.type == 1:
            self.graph = GraphLine(660,120,1080,340,5, "CPU")
            self.graph2 = GraphLine(660,380,1080,600,5, "RAM")
         #   self.graph1 = GraphLine(xLeft,yTop,xRight,yBottom,line)
    
    def downkey(self):
        self.selector += 1
        self.selectoralign()
        
    def upkey(self):
        self.selector -= 1
        self.selectoralign()
        
    def enterkey(self,selection,target):
        # this function defines the behaviour of the display area when the enter key is pressed. 
        # It determines what type of tile it is and what the selected function is, because of the diversity
        # of tiles it will require a lot of different selections to be defined

        # if this is a notes tile.
        if self.type == 3:
            if selection == 2:
                self.selector += 1
            if selection == 1:
                self.selector -= 1
            if selection == 0:
                item = self.folist[self.selector]
                print(item)
                fs = files()
                notetext = fs.getitem(item)
                target.viewit(notetext)
                
        # if viewing area selected collect image or text for viewing and instantiate a viewarea object with that data.
        


    def selectoralign(self):
        if self.selector > 4:
            self.selector = 4
        if self.selector < 0:
            self.selector = 0
            
    def outline(self,xLeft,xRight,yTop,yBottom,line):
        pygame.draw.lines(self.surface, textc, False, ((xLeft,yTop),(xRight,yTop),(xRight,yBottom),(xLeft,yBottom),(xLeft,yTop)), line)       
        
    def drawblock(self,y,h):
        rect = pygame.Rect((self.info["dispbx"],y), (self.info["dispw"],h))
        pygame.draw.rect(self.surface, buttonc, rect)
    
    def drawbutton(self,y,content):
        butxmid = self.info["dispbx"] + (self.info["dispw"] / 2)  
        butymid = y + (40 / 2)  
        self.drawblock(y,40)
        butlabel = Label()
        butlabel.update(content,26,butxmid,y,titleFont,textc)
        size = butlabel.getrect()
        butlabel.center(self.info["dispw"],40,self.info["dispbx"],y)
        #textposx = butxmid - (size[0]/2)
        #textposy = butymid - (size[1]/2)qq
        
        #butlabel.update(content,26,textposx,textposy,titleFont,textc)
        butlabel.draw(self.surface)
        
    def draw(self,info):
        
        self.info = info
        
        # Home Tile layout
        if self.type == 0:
            self.info = info
            self.message = "No New Messages"
            self.drawblock(self.info["innery"],self.info["disph"])
        
        # System Tile Layout 
        if self.type == 1:
            #self.graphassign(2)
#           graph1 = GraphLine(xLeft,yTop,xRight,yBottom,line)
            data = sensorget()
            for i in range(2):
                ypos = self.info["innery"] + (260 * i)
                self.drawblock(ypos,220)
            self.graph.update(self.surface,data['cpuperc'],0,100,textc)
            self.graph2.update(self.surface,data['ramperc'],0,100,textc)
    
    
        # notes tile layout
        if self.type == 3:
            #self.graphassign(2)
#           graph1 = GraphLine(xLeft,yTop,xRight,yBottom,line)
            notes = files()
            
            self.folist = notes.ListText()
            count= len(self.folist)
            for i in range(count):
                caption = str(self.folist[i])
                ypos = self.info["innery"] + (60 * i)
                self.drawbutton(ypos,caption)
                if i == self.selector:
                    self.outline(self.info["dispbx"],(self.info["dispbx"] + self.info["dispw"]),ypos,(ypos+40),3)

        
    def update(self):
        pass
    
class Tile(object):
    def __init__(self,tiletype,surface,screenSize,colour,index):
        self.info = {"tiletype" : tiletype, "surface" : surface, "x" : 160, "y" : 80, "index" : index, "colour" :colour , "seam" : 80, "inner" : 40, "titlesize" : 100, "spanx" : 960, "spany" : 560, "innerx" : 200, "innery" : 120, "inspanx" : 880, "inspany" : 480, "lineposy" : 240, "aaspanx" : 420, "dispposx" : 660, "dispw" : 420, "disph" : 480, "actareay" : 320, "actareaw" : 420, "actareah" : 280}       
        self.info["tilejump"] = self.info["seam"] + self.info["spanx"]

        if self.info["index"] > 0:
            self.info["x"] = self.info["x"] + ((self.info["seam"] + self.info["spanx"]) * self.info["index"])

        self.info["pos"] = (self.info["x"],self.info["y"])
        self.info["inpos"] = (self.info["innerx"],self.info["innery"])
        self.info["size"] = (self.info["spanx"],self.info["spany"])
        self.info["innersize"] = (self.info["inspanx"],self.info["inspany"])
        self.updatelayout()
        self.viewing = False
        
    def upkey(self):
#        print("keyupped!")
        self.actionarea.upkey()
        
    def downkey(self):
#        print("keydown received!")
        self.actionarea.downkey()
        
    def enterkey(self):
        #receives enter key and passes it to action area
        if self.viewing:
            self.viewing = False
        else:
            selection = self.actionarea.enterkey()
            self.disparea.enterkey(selection,self)

    def viewit(self, item):
        print(item)
        self.viewing = True
        self.item = item
        self.viewframe = viewingarea(self.item,self.info)
    
    def drawlayout(self):
        # the following checks what type of tile this is and draws elements accordingly. If there is a viewframe event triggered it draws that, if not it draws the standard layout.
            #self.actarea = actionarea(0,self.info["surface"])
            if self.viewing:
                self.viewframe.draw()
                
            else:
                title = Label()
                title.update(self.title,self.info["titlesize"],self.info["innerx"],self.info["innery"],titleFont,textc)
                title.draw(self.info["surface"])
                pygame.draw.lines(self.info["surface"], textc, False, ((self.info["innerx"], self.info["lineposy"]),((self.info["innerx"] + self.info["aaspanx"]), self.info["lineposy"])), 6)
                self.disparea.draw(self.info)
                self.actionarea.draw(self.info)
    
                    
    def updatelayout(self):
        # the following checks what kind of tile this is and updates the layout accordingly
        if self.info["tiletype"] == 0:
            self.title = "Home"

        if self.info["tiletype"] == 1:
            self.title = "System"
        
        if self.info["tiletype"] == 2:
            self.title = "Assistant"
        
        if self.info["tiletype"] == 3:
            self.title = "Notes"
        
        if self.info["tiletype"] == 4:
            self.title = "RSS"
            
        self.disparea = displayarea(self.info)
        self.actionarea = actionarea(self.info)
            
    def update(self):
        pass
    
    def position(self,page):
        # the following updates internal coordinates for each tile so that tiles can move horizontally when the user selects a new one.
        self.info["pos"] = (self.info["x"] - ((self.info["tilejump"]) * page)),self.info["y"]
        self.info["upx"] = (self.info["x"] - (self.info["tilejump"] * page))
        self.info["innerx"] = (self.info["x"] - (self.info["tilejump"] * page)) + self.info["inner"]
        self.info["dispbx"] = self.info["innerx"] + 459
        self.info["pageadjust"] = self.info["tilejump"] * page


    def getinfo(self):
        return self.layout

    def draw(self,page1):

        page = (float(page1) / 100)

        # check position values
        self.position(page)
        
        #if in focus draw action and display areas
        if page == self.info["index"]:
        #actarea.draw(self.info["pos"])
        
            #draw the background of the tile
            self.rect = pygame.Rect(self.info["pos"], self.info["size"])
            pygame.draw.rect(self.info["surface"], self.info["colour"], self.rect)

            #draw the foreground elements of the tile.

        
            # draw display area to right
            # self.disparea.draw(self.info["dispbx"],self.info["innery"],(self.info["dispw"],self.info["disph"]))
            self.drawlayout()
        
            # draw horizontal line 

            # draw action area
        else:
            # if not in focus just makes the tile dark grey.
            self.rect = pygame.Rect(self.info["pos"], self.info["size"])
            pygame.draw.rect(self.info["surface"], buttoncmute, self.rect)
