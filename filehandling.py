# file handling for headsup

import os


#read the contents of folder and return it as a list
#open and change directory
#


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
    
    def getitem(self,target):
        target = str("./notes/"+target)
        item = os.open(target, os.O_RDWR|os.O_CREAT)
        ret = os.read(item,10000)
        return ret

    
    def ListDir(self):
        # something I found. It parses a list of the items present in a directory and only adds the subdirectories to the list. Returns that list.
        
        # need to figure out how this x for x in object thing works.
        
        self.dirlist = [x for x in os.listdir('.') if os.path.isdir(x)]

                
        return self.dirlist
        
    def ListText(self):
        textlist = []
        for file in os.listdir("./notes"):
            if file.endswith(".txt"):
                textlist.append(file)
        return textlist
        
    def Open(self, item):
        #element should be passed a filename and use its current directory 
        
        pass
        
