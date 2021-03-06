#!/usr/bin/env python

"""

    HeadsUp

    Code by C.Barrett
    Designed by S.Caem
    
    This file controls the layout of each Tile.

"""


import pygame
import pygame.gfxdraw
import os
import time
from datetime import datetime
from getvitals import *
from filehandling import *
from textrect import *
from ifttt import *
from calget import *
#from main import tileTitles

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

tileTitles = ("Home","System","IFTTT","Notes","Images","Sensors")


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
        
        test = int(self.xSpan)
        for i in range(test):
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
        test = int(self.xSpan)
        for i in range(test):
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
        self.scaler = 3


    def update(self, content, fontSize, nx, ny, fontType, color):
        self.x = nx
        self.y = ny
        self.content = content
        self.fontSize = fontSize
        self.myfont = pygame.font.Font(fontType, self.fontSize)
        self.color = color


    def left(self,w,h,x,y):
        size = self.getrect()
        xmid = x + 40
        ymid = y + h/2
        textposx = xmid
        textposy = ymid - (size[1]/2) + self.scaler
        self.update(self.content,self.fontSize,textposx,textposy,titleFont,self.color)


    def center(self,w,h,x,y):
        size = self.getrect()
        xmid = x + w/2
        ymid = y + h/2
        textposx = xmid - (size[0]/2)
        textposy = ymid - (size[1]/2) + self.scaler
        self.update(self.content,self.fontSize,textposx,textposy,titleFont,self.color)


    def pageup(self):
        pass

    def nopages(self):
        ret = self.text.nopages
        return ret

    def paragraph(self,page):

        my_rect = pygame.Rect((0, 0, 804, 366))

        self.text = TextBlock()

        # this next function returns a block of text rendered for the screen.
        rendered_text = self.text.render_textrect(self.content, self.myfont, my_rect, textc, buttonc, page,0)

        #self.nopage = self.text.nopages()

        return rendered_text


    def getpages(self):
        return self.nopage

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
        
    def getcenter(self):
        self.ret = self.rect.center
        return self.ret
        
    def update(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        
    
    def draw(self, surface):
        self.rect = pygame.Rect((self.x,self.y), self.size)
        pygame.draw.rect(surface, self.color, self.rect)


class viewingarea(object):
    def __init__(self, content, info):
        
        self.content = content
        
        self.info = info
        
        self.textarea = Label()
        
        # defines the surface we will be drawing to, passed from our tiles object
        self.surface = self.info["surface"]
        
        # draw our background box
        self.substrate = Box()
        self.substrate.update(200,120,(880, 440),buttonc)
        
        # Sets the currently selected button
        self.selector = 0
        self.selectmax = 2
        self.page = 0
        
    def rightkey(self):
        self.page += 1
        self.pageadjust()
        
    def leftkey(self):
        self.page -= 1
        self.pageadjust()
        
    def pageadjust(self):
        if self.page <= 0:
            self.page = 0
        if self.page >= (self.maxpages-1):
            self.page = (self.maxpages-1)
        
    def enterkey(self,tile):
        if self.selector == 0:
            tile.stopview()
        elif self.selector == 1:
            self.page -=1

        elif self.selector == 2:
            self.page +=1
            
    def selectalign(self):
        if self.selector > self.selectmax:
            self.selector = self.selectmax
        
        if self.selector < 0:
            self.selector = 0
    
    def drawbutton(self,x,content):
        #defines center of button
        y = 400
        
        butymid =  y + (40 / 2)  
        
        butxmid = x + 180 / 2
        
        # draws button backplane
        rect = pygame.Rect(x,580,180,40)
        pygame.draw.rect(self.surface, buttonc, rect)
        
        # instantiates a label object.
        butlabel = Label()
        butlabel.update(content,26,butxmid,y,titleFont,textc)
        size = butlabel.getrect()
        butlabel.center(180,40,x,580)
        butlabel.center(180,40,x,580)
        #textposx = butxmid - (size[0]/2)
        #textposy = butymid - (size[1]/2)qq
        
        #butlabel.update(content,26,textposx,textposy,titleFont,textc)
        butlabel.draw(self.surface)
        
    def outline(self,xLeft,xRight,yTop,yBottom,line):
        pygame.draw.lines(self.surface, textc, False, ((xLeft,yTop),(xRight,yTop),(xRight,yBottom),(xLeft,yBottom),(xLeft,yTop)), line)
    

    def draw(self):
        # draw the background box
        self.substrate.draw(self.surface)
        
        # check if this is a notes tile (3) or an image tile (4)
        if self.info["tiletype"] == 3:
            self.textarea.update(self.content,26,0,0,titleFont,textc)
            
            self.surface.blit(self.textarea.paragraph(self.page), (240,160))
            
            self.maxpages = int(self.textarea.nopages())
            print(self.maxpages)
            
        # if its an image viewing tile
        elif self.info["tiletype"] == 4:
            
            
            backrect = self.substrate.getcenter()
            
            self.content = pygame.transform.scale(self.content, (880,440))

            self.surface.blit(self.content,(200,120))
        
        labels = ["Exit","Previous","Next"]
        
  
        label = labels[0]
        xgo = 200
        self.drawbutton(xgo, label)
        if 0 == self.selector:
            self.outline(xgo,(xgo+180),580,(580+40),3)

    

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
        
        if self.selector ==  4:
            if self.type == 1:
                print("quit received")
                return "quit"
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
    
    def wifiname(self):
        wifiname = getwifi()
        return wifiname
        
    def drawblock(self,y,h):
        rect = pygame.Rect((self.info["innerx"],y), (self.info["actareaw"],h))
        pygame.draw.rect(self.surface, buttonc, rect)
        
    def drawbutton(self,y,content):
        # the x mid point of the button is the distance of the x coordinate of the button plus the span of the button divided by 2
        butxmid = self.info["innerx"] + (self.info["aaspanx"] / 2)  
        
        # the y mid point of the button is the distance of the y coordinate of the button plus the height of the button divided by 2
        butymid = y + (40 / 2)  
        
        # draw the rectangle to screen
        self.drawblock(y,40)
        
        # instantiate a text object
        butlabel = Label()
        # update the content of the text object.
        butlabel.update(content,26,butxmid,y,titleFont,textc)
        
        #center the text on the button
        butlabel.center(self.info["actareaw"],40,self.info["innerx"],y)

        # draw the text.
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
            timely = self.info["actareay"]
            timel.update(self.time,26,(self.info["innerx"]+155),(self.info["actareay"]+7),titleFont,textc)
 

            timel.center(self.info["aaspanx"],40,self.info["innerx"],timely)
            timel.draw(self.surface)
            
            # instantiate the label for the date line
            datel = Label()
            datey = self.info["actareay"]+38
            datel.update(self.date,26,(self.info["innerx"]+92),(self.info["actareay"]+40),titleFont,textc)
            size = datel.getrect()
            labelpos = self.info["innerx"]+(self.info["aaspanx"]/2)-(size[0]/2)

            datel.center(self.info["aaspanx"],40,self.info["innerx"],datey)
            datel.draw(self.surface)
            

            
            # instantiate the label for the time line
            wifi = Label()
            wifiname = self.wifiname()
            wifiy = self.info["actareay"] + 180
            wifi.update(wifiname,26,(self.info["innerx"]+155),(self.info["actareay"]+7),titleFont,textc)
            
            wifi.center(self.info["aaspanx"],40,self.info["innerx"],wifiy)
            wifi.draw(self.surface)
            
        # draw system screen actionable buttons and highlight    
        if self.type == 1:
            buttontexts = ["Shutdown","Reboot","Toggle Wifi", "Toggle Bluetooth", "Quit HeadsUP"]
            self.selectmax = 4
            for i in range(5):
                
                ypos = self.info["actareay"] + (60*i)
                self.drawbutton(ypos,buttontexts[i])
                if i == self.selector:
                    self.outline(self.info["innerx"],(self.info["innerx"] + self.info["aaspanx"]),ypos,(ypos+40),3)
        
        # draw IFTT buttons
        if self.type == 2:
            
            buttontexts = ["Engage", "Up","Down","Refresh List", "Delete"]
            self.selectmax = 4
            for i in range(5):
                
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

        # Define layout for Images tile
        if self.type == 4:
            buttontexts = ["View","Up","Down", "Refresh List", "Delete"]
            self.selectmax = len(buttontexts)
            for i in range(self.selectmax):
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
            self.timer = pygame.time.Clock()
        
        #interval timer variables:
        self.lasttime = 0
        self.interval = 50
        
    
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


        #["Engage", "Up","Down","Refresh List", "Delete"]
        # if this is an IFTTT tile.
        if self.type == 2:
            if selection == 2:
                self.selector += 1
            if selection == 1:
                self.selector -= 1
            if selection == 0:
                item = self.folist[self.selector]
                
                fs = files()
                triggerinfo = fs.getTrigger(item)
                key,trig = triggerinfo
                trigger = MakerTrigger(key,trig)
                try:
                    trigger.alert()
                except:
                    pass
                
        # if this is a notes tile.
        if self.type == 3:
            if selection == 2:
                self.selector += 1
            if selection == 1:
                self.selector -= 1
            if selection == 0:
                
                #
                item = self.folist[self.selector]
                
                fs = files()
                notetext = fs.gettext(item)
                
        # if viewing area selected collect image or text for viewing and instantiate a viewarea object with that data.
        
                target.viewit(notetext)
                
        # if this is an images tile.
        if self.type == 4:
            if selection == 2:
                self.selector += 1
            if selection == 1:
                self.selector -= 1
            if selection == 0:
                item = self.folist[self.selector]
                
                fs = files()
                image = fs.getimage(item)
                
        # if viewing area selected collect image or text for viewing and instantiate a viewarea object with that data.
        
                target.viewit(image)
                

                
                
                


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
        butxmid = self.info["dispbx"] + 5  
        butymid = y + (40 / 2)  
        self.drawblock(y,40)
        butlabel = Label()
        butlabel.update(content,26,butxmid,y,titleFont,textc)
        size = butlabel.getrect()
        butlabel.left(self.info["dispw"],40,self.info["dispbx"],y)

        #butlabel.update(content,26,textposx,textposy,titleFont,textc)
        butlabel.draw(self.surface)
        
    def draw(self,info):
        
        self.info = info
        
        # --------------------------------------------------------------------------------- Home Tile layout
        # Display the current Calendar data
        if self.type == 0:
            self.info = info
            
            # Draw the agenda label
            self.heading = "Agenda"
            agendaheading = Label()
            agendaheading.update(self.heading,30,self.info["dispbx"] + 10 , self.info["innery"] + 10,titleFont,textc)
            
            # Draw todays date.
            datelabel = Label()
            
            
            self.drawblock(self.info["innery"],self.info["disph"])
            agendaheading.draw(self.surface)
            
            events = CalendarPull()
            
            eventlist = events.GetTodaysEvents()
            
            listsize = len(eventlist)
            objs = [Label() for i in range(listsize)]
            i=0
            for obj in objs:
                content = eventlist[i]
                obj.update(content,20,self.info["dispbx"] + 10 ,(self.info["innery"]+60)+(30 * i),titleFont,textc)
                obj.draw(self.surface)
                i += 1
        # ------------------------------------------------------------------------------- System Tile Layout
        if self.type == 1:
            #self.graphassign(2)
#           graph1 = GraphLine(xLeft,yTop,xRight,yBottom,line)
            data = sensorget()
            for i in range(2):
                ypos = self.info["innery"] + (260 * i)
                self.drawblock(ypos,220)
                
                
            self.timenow = pygame.time.get_ticks()
            elapsed = self.timenow - self.lasttime
            if elapsed > self.interval:
                self.lasttime = self.timenow
                self.graph.update(self.surface,data['cpuperc'],0,100,textc)
                self.graph2.update(self.surface,data['ramperc'],0,100,textc)
    
    
        # iftt tile layout-------------------------------------------------------------------------------
        if self.type == 2:
            
            # Get the trigger text files
            triggers = files()
            
            self.folist = triggers.ListTriggers()
            count= len(self.folist)
            for i in range(count):
                # name each button the title of the text file
                caption = str(self.folist[i])
                
                # set the position of each button, each time through the loop the button is moved down 60 pixels
                ypos = self.info["innery"] + (60 * i)
                
                self.drawbutton(ypos,caption)
                
                    
                if i == self.selector:
                    self.outline(self.info["dispbx"],(self.info["dispbx"] + self.info["dispw"]),ypos,(ypos+40),3)
                    
        # notes tile layout-------------------------------------------------------------------------------
        if self.type == 3:

            notes = files()
            
            self.folist = notes.ListText()
            count= len(self.folist)
            for i in range(count):
                caption = str(self.folist[i])
                ypos = self.info["innery"] + (60 * i)
                self.drawbutton(ypos,caption)
                if i == self.selector:
                    self.outline(self.info["dispbx"],(self.info["dispbx"] + self.info["dispw"]),ypos,(ypos+40),3)

        # Image tile layout-------------------------------------------------------------------------------
        if self.type == 4:

            images = files()
            
            self.folist = images.ListImage()
            count= len(self.folist)
            for i in range(count):
                caption = str(self.folist[i])
                ypos = self.info["innery"] + (60 * i)
                self.drawbutton(ypos,caption)
                if i == self.selector:
                    self.outline(self.info["dispbx"],(self.info["dispbx"] + self.info["dispw"]),ypos,(ypos+40),3)

    
class Tile(object):
    def __init__(self,tiletype,surface,screenSize,colour,index):
        self.info = {"tiletype" : tiletype, "surface" : surface, "x" : 160, "y" : 80, "index" : index, "colour" :colour , "seam" : 80, "inner" : 40, "titlesize" : 100, "spanx" : 960, "spany" : 560, "innerx" : 200, "innery" : 120, "inspanx" : 880, "inspany" : 480, "lineposy" : 210, "aaspanx" : 420, "dispposx" : 660, "dispw" : 420, "disph" : 480, "actareay" : 320, "actareaw" : 420, "actareah" : 280}       
        self.info["tilejump"] = self.info["seam"] + self.info["spanx"]

        if self.info["index"] > 0:
            self.info["x"] = self.info["x"] + ((self.info["seam"] + self.info["spanx"]) * self.info["index"])

        self.info["pos"] = (self.info["x"],self.info["y"])
        self.info["inpos"] = (self.info["innerx"],self.info["innery"])
        self.info["size"] = (self.info["spanx"],self.info["spany"])
        self.info["innersize"] = (self.info["inspanx"],self.info["inspany"])
        self.updatelayout()
        
        
        #the following variable is used to determine whether the current tile is using a viewframe to display content and if so controls are different
        self.viewing = False

        
        
    def upkey(self):
#        print("keyupped!")
        self.actionarea.upkey()
        
    def downkey(self):
#        print("keydown received!")
        self.actionarea.downkey()
        
    def enterkey(self,status):
        
        #receives enter key and passes it to action area
        
        # if the tile is currently in a viewing event (looking at an image or a note)
        if self.viewing:
            #Direct enterkey events to the viewing area as opposed to the action/display area (so that enters effect the viewing area)
           self.viewframe.enterkey(self)
        else:
            # otherwise see what the current selected button is in the action area
            selection = self.actionarea.enterkey()
            
            # if the action area has a "quit" button selected (not sure if this is still what's happening, may be deprecated)
            if selection == "quit":
                # then return a quit directive to the main loop
                print("quit also received")
                status = "quit"
                return status
                
            # if no quit event is received then pass the display area the currently selected button in the action area, 
            #and a copy of this tile so the display area has access to the tile's methods
            self.disparea.enterkey(selection,self)
            


    
    def leftkey(self):
        # if a left key event is received 
        self.viewframe.leftkey()

    def rightkey(self):
        self.viewframe.rightkey()
    
    
    def isview(self):
        if self.viewing:
            return True
        else:
            return False
            
    def stopview(self):
        self.viewing = False

    def viewit(self, item):
        #print(item)
        # Set the tiles state show that it is currently in view mode. This makes sure inputs are handled properly.
        self.viewing = True
        
        # apply the returned item (be it text or surface) 
        self.item = item
        
        # create a viewing area object with the appropriate information
        self.viewframe = viewingarea(self.item,self.info)
    
    def drawlayout(self):
        # the following checks what type of tile this is and draws elements accordingly. If there is a viewframe event triggered it draws that, if not it draws the standard layout.

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

        index = self.info["tiletype"]

        self.title = tileTitles[index]

        self.disparea = displayarea(self.info)
        self.actionarea = actionarea(self.info)

    
    def position(self,page):
        # the following updates internal coordinates for each tile so that tiles can move horizontally when the user selects a new one. This basically allows for the main loop to feed updated position data to each tile so they can move appropriately
        
        # current  X position =  default X position - the tilejump X scaler * the page number 
        self.info["pos"] = (self.info["x"] - ((self.info["tilejump"]) * page)),self.info["y"]
        self.info["upx"] = (self.info["x"] - (self.info["tilejump"] * page))
        self.info["innerx"] = (self.info["x"] - (self.info["tilejump"] * page)) + self.info["inner"]
        self.info["dispbx"] = self.info["innerx"] + 459
        self.info["pageadjust"] = self.info["tilejump"] * page

    def draw(self,page1):
        
        # takes the integer scaler value and turns it into a page index.
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
            # draw both the display area and the action area
            self.drawlayout()
        
        else:
            # if not in focus just makes the tile dark grey.
            self.rect = pygame.Rect(self.info["pos"], self.info["size"])
            pygame.draw.rect(self.info["surface"], buttoncmute, self.rect)
