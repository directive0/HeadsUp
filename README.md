![Logo](https://raw.githubusercontent.com/directive0/HeadsUp/master/assets/logo.png?raw=true "Logo")

# HeadsUp!

A simple pygame interface for a heads up display (HUD) intended to work with [VuFine headsets](https://www.vufine.com/) and [Raspberry Pi](https://www.raspberrypi.org/). It is the joint effort of two people who have never met. 

- Code by [C.Barrett](http://www.directive0.com)

- Design by [S.Caem](mailto:thedigitons@gmail.com)

The basic design intent of this program is to allow users to be able to access text and image reference, to view sensors related to the environment, and to trigger and receive IFTTT webhook events all from a simple wearable computing rig. It aims to offer some functionality approaching the level of products like Google Glass or HoloLens but without any augmented reality. 

A secondary desire of the project is that it be modular and allow users with a moderate knowledge of Python to create their own tile layouts if they desire, but this aspect is not fully realized yet.



### What works at present:

- Basic layout and interface.
- Basic handling for notes.
- Basic handling for images
- User created IFTTT events can be added and triggered.
- CPU and RAM status monitoring
- WIFI SSID name reporting (not 100% yet)


### What is left to be done:
- Fix numerous tiny bugs
- Recieve IFTTT alerts and display on main page.
- Final bug testing and cleanup
- Deciding whether to make user-generated tiles a big feature. It will require considerable refactoring (and I'm lazy -d0)
- Comment as much code as possible for anyone wishing to make substantial improvements.

## Required Hardware:


### CPU
- HeadsUp was designed for the Raspberry Pi 3 running Raspbian but will function on almost any computer running Python3.

### Display
- HeadsUp was designed to use the VuFine headset as its main display but it will run fine on any monitor that can meet a 1280x720 resolution.
- For more detailed information regarding using a vufine headset see the "Installation" heading below.

### Interface
- No specific keyboard interface has been defined yet but the software is being designed to support 5 basic controller buttons. I am leaning towards a Wii Nunchuck as my interface device but any 5 button interface could be supported in the future. For now the software polls pygame for simple keyboard presses.

## Required Software

HeadsUp is designed to run on Python 3, or if desired it should work on Python2+ (not tested). 

### Python Dependencies
- pygame
- psutil
- requests

- os (included with python)
- time (included with python)

If these modules are not already present on your machine they should be easy to install with apt-get, pip like so:

`sudo apt-get install -y python3 python3-dev python3-pygame python3-pip`

And then...

`sudo pip3 install psutil requests`

## Installation

- if using a vufine display and raspberry pi running raspbian make sure to disable overscan in your /boot/config.txt file or else Pygame will give you warnings about no appropriate video mode.

- use raspi-config to change your resolution to 1280x720 60hz

- Ensure your machine has the appropriate version of Python and its dependencies as listed above. 

- Clone the git repo to your machine 

`git clone https://www.headsup.com/directive0/HeadsUp`

- Open a terminal and navigate to the HeadsUp folder

`cd HeadsUp`

- Issue the command and the program will start

`python3 main.py`

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
