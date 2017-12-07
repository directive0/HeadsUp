![Logo](https://raw.githubusercontent.com/directive0/picorder/master/assets/logo.png?raw=true "Logo")

# HeadsUp!

Simple pygame interface for a heads up display (HUD). Intended to work with VuFine headsets and Raspberry Pi. 

Code by C.Barrett
Design by S.Caem

### What works at present:

- Basic layout and interface
- Basic handling for notes.
- IFTTT events can be triggered
- CPU and RAM status monitoring
- WIFI SSID name reporting (not 100% yet)


### What is left to be done:
- Recieve IFTTT alerts
- Open Images


## Required Python Dependencies

- pygame
- psutil
- os
- time
- requests




## Keys

HeadsUp is designed to work with 5 basic buttons: Up, Down, Left, Right, and Enter. There is one exception as the "Q" key will quit the program.



## How to configure IFTTT:

In order to use IFTTT triggers from the IFTTT tile you need to create a text file containing your Key and the Event Name seperate by a comma as below.

1234556789101112,trigger

Name the text file what you want the button to be labelled that activates it; "Turn on lights.txt" for example.

Do not add any extra information to the text file or any extra lines or else it will not work.


## Notes:

Add any text files you wish to view from HeadsUp! in the "notes" folder.

## Images:

Add any images you wish to display to the "images" folder
