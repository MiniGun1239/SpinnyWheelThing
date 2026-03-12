# Spinny Wheel Thing
A very feature-crept Steering wheel running on rpi pico

## Intro
This is my attempt at making a sim wheel with (sadly) no FFB.

## Setup
### Step 1
(Skip to **Step** 3 if firmware is ready with circuit python version 9.x or above)

1. On your Raspberry Pi Pico (or Pico 2), There is a button ```BOOTSEL```.  
2. Hold it and plug in the pi without releasing it.

You should be able to see a drive connected named ```PRI-PRI2```.  
This is the Pi mounted as a **Mass Storage Device**

### Step 2
In this repo, there should be a ```boot/``` directory.  
Inside it there is a ```.uf2``` file.  

Move the ```adafruit-circuitpython-raspberry_pi_pico-en_US-10.1.4.uf2``` file into the ```RPI-RP2```'s root directory.  

Disconnect the Pi.

### Step 3
Reconnect the Pi, do NOT hold ```BOOTSEL``` this time, if you did, go back to step 2

From this repo, move ```boot.py``` and ```code```.py to the 

### Step 4
_TBA_