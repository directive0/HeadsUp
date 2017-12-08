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
    

from subprocess import check_output

def getwifi():
    try:
        scanoutput = check_output(["iwgetid"])
        print(scanoutput)
        ssid = "WiFi not found"
    
        for line in scanoutput.split():
            line = line.decode("utf-8")
            print(line)
            if line[:5]  == "ESSID":
                #will need to fix this for names with spaces.
                ssid = line.split('"')[1]
                ssidname = str(ssid.encode())
                string = "SSID: " + ssidname
                
    except:
        string = "Unable to Retrieve WIFI Name"

    return str(string)
    
