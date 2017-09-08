import psutil
import time

def sensorget():
    
   statusram = psutil.virtual_memory()
   
   vitaldict = {} 
   vitaldict['cpuperc'] = str(psutil.cpu_percent(interval=.1))
   vitaldict['ramtotal'] = str(statusram[0])
   vitaldict['ramavail'] = str(statusram[1])
   vitaldict['ramperc'] = str(statusram[2])
   vitaldict['cpufreq'] = str(psutil.cpu_freq())

   return vitaldict

def voicecall():
    pass
    
