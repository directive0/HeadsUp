![Logo](https://raw.githubusercontent.com/directive0/HeadsUp/master/assets/logo.png?raw=true "Logo")

# HeadsUp!

Simple pygame interface for a heads up display (HUD). Intended to work with VuFine headsets and Raspberry Pi. It is the joint effort of two people who have never met.

Code by C.Barrett
Design by S.Caem

### What works at present:

- Basic layout and interface.
- Basic handling for notes.
- IFTTT events can be added and triggered.
- CPU and RAM status monitoring
- WIFI SSID name reporting (not 100% yet)


### What is left to be done:
- Recieve IFTTT alerts
- Open Images


## Required Dependencies

HeadsUp is designed to run on Python 3.

### Python Dependencies
- pygame
- psutil
- os
- time
- requests

If these modules are not already present on your machine they should be easy to install with Pip.

## Keys

HeadsUp is designed to work with 5 basic buttons: Up, Down, Left, Right, and Enter. There is one exception as the "Q" key will quit the program. Eventually I will break out these keys into a configure file so that you only need to edit the configure file if you want to make changes to them.


## How to configure IFTTT:

In order to use IFTTT triggers from the IFTTT tile you need to create a text file containing your Key and the Event Name seperate by a comma as below and make a folder named "triggers" for it to reside in. You can find your key by logging into IFTT and going to https://ifttt.com/maker_webhooks and then clicking the "documentation" button at the top right. 

Name the text file what you want the button to be labelled that activates it; "Turn on lights.txt" for example and make a folder in the HeadsUp directory called "triggers". Put the text file in the folder named "triggers"

Do not add any extra information to the text file or any extra lines or else it will not work. 

There is an example included in this git that you can edit with your own IFTTT key and alert name. You will need to create a WebHooks applet on the IFTTT website that receives the appropriate trigger. 


## Notes:

Add any text files you wish to view from HeadsUp! in the "notes" folder.

## Images:

Add any images you wish to display to the "images" folder
