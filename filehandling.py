# file handling for headsup

import os


#read the contents of folder and return it as a list
#open and change directory
#


class files(object):
    
    def __init__(self):
        self.home = os.path.expanduser("~")
        self.cd(self.home)
        self.listdir()
        self.current = self.home
        
    def goup(self,path):
        self.current = os.path.dirname(os.path.dirname(path))

    def cd(self,path):
        os.chdir(path)
        
    def listdir(self):
        # something I found. It parses a list of the items present in a directory and only adds the subdirectories to the list.
        
        #need to figure out how this x for x in item thing works.
        
        self.dirlist = [x for x in os.listdir('.') if os.path.isdir(x)]
        
        return self.dirlist
        
        
    def open(self, item):
        #element should be passed a filename and use its current directory 
        
        pass
        
