# file handling for headsup

import os


#read the contents of folder and return it as a list
#open and change directory



class files(object):
    
    def __init__(self):
        self.home = os.path.expanduser("~")
        #self.CD(self.home)
        #self.List()
        #self.current = self.home
        
    def GoUp(self,path):
        self.current = os.path.dirname(os.path.dirname(path))

    def CD(self,path):
        os.chdir(path)
    
    
    def getTrigger(self,target):

        # open trigger text file with the name provided
        
        target = str("./triggers/"+target+".txt")

        
        item = open(target, "r")
        
        # read the text file into a string
        ret = item.read(100)
        # seperate the string up based on commas
        ret = ret.split(",")
        # set a counter for each item in the string
        index = len(ret)
        
        # the next function removes the new line character from the result to avoid confusion.
        for i in range(index):
            string = ret[i]
            if string.find("\n"):
                ret[i] = string.replace("\n", "")
                
                
        
        return ret

    def gettext(self,target):
        target = str("./notes/"+target)
        item = os.open(target, os.O_RDWR|os.O_CREAT)
        ret = os.read(item,10000)
        return ret
    
    
    def getimage(self,target):
        target = str("./images/"+target)
        item = os.open(target, os.O_RDWR|os.O_CREAT)
        ret = os.read(item,10000)
        return ret
    
    

    
    #~ def ListDir(self):
        #~ # something I found. It parses a list of the items present in a directory and only adds the subdirectories to the list. Returns that list.
        
        #~ # need to figure out how this x for x in object thing works.
        
        #~ self.dirlist = [x for x in os.listdir('.') if os.path.isdir(x)]

        #~ return self.dirlist
    
    def ListTriggers(self):
        textlist = []
        for file in os.listdir("./triggers"):
            if file.endswith(".txt"):
                if file.find(".txt"):
                    name = file.replace(".txt", "")
                    textlist.append(name)
        textlist.sort()
        return textlist
        
    def ListText(self):
        # this function polls a directory for all files ending in ".txt"
        
        # we create a list to store the file names in
        textlist = []
        
        # for each item in the specified directory we grab each one that ends in ".txt"
        for file in os.listdir("./notes"):
            if file.endswith(".txt"):
                textlist.append(file)
        
        #sort the list so its more useful
        textlist.sort()
        # we return this list to the asker
        return textlist
        
    def Open(self, item):
        #element should be passed a filename and use its current directory 
        
        pass
        
