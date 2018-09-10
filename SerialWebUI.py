#!/usr/bin/env python

# Global variables
servoAngle = 0.0

# Check current platform and assign ports based on this
import platform
os = platform.system()

if (os == 'Darwin'):
    port = '/dev/cu.SLAB_USBtoUART'
elif (os == 'Windows'):
    port = 'COM9'
elif (os == 'Linux'):
    port = '/dev/ttysUSB0'
else:
    port = ''
    print('OSError: Invalid OS!')

# Create serial connection with Servo using PySerial
import serial
import io

try:
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = 9600
    ser.open()
except SerialException:
    print('SerialError: Could not connect to serial port')

print(' * Port: {}'.format(ser.port))
print(' * Baudrate: {}'.format(ser.baudrate))

# Create IO wrapper that encodes text to bytes
serIO = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

## Write to precreated IO object and flush
def ioWrite(toWrite):
    toWrite.encode(encoding='ascii') ## Servo only accepts UTF-8
    serIO.write(toWrite)
    serIO.flush()

# Setup M Drive servo motor
ioWrite('fd\r\n') ## Reset servo to factory defaults
ioWrite('ma 0\r\n') ## Homing routine
ioWrite('h\r\n') # Wait until task completes
ioWrite('s1=1,0,0\r\n') # Make input 1 homing input

# Create a web interface to take data from using Flask
from flask import Flask, render_template, request, url_for
app = Flask(__name__)

## Index page
@app.route('/')
def index():
    global servoAngle

    return render_template('mdrive.html', currAngle=servoAngle)

## Incremental form submission
@app.route('/handleIncremental', methods=['POST'])
def handleIncremental():
    global servoAngle

    cts = request.form['cts']
    if (cts == 't'):
        cts = True
    else:
        cts = False

    incAngle = float(request.form['incAngle'])
    delay = float(request.form['delay'])
    stopAngle = request.form['stopAngle']

    if (stopAngle != ""):
        stopAngle = float(stopAngle)

    updateServoIncremental(cts, incAngle, stopAngle, delay)
    return render_template('mdrive.html', currAngle=round(servoAngle,2))

## Specific form submission
@app.route('/handleSpecific', methods=['POST'])
def handleSpecific():
    global servoAngle

    nextAngle = float(request.form['angle'])

    updateServoSpecific(nextAngle)
    return render_template('mdrive.html', currAngle=servoAngle)

## Update M Drive servo with specific angle
def updateServoSpecific(nextAngle):
    global servoAngle
    angleDiff = nextAngle - servoAngle;

    if (angleDiff == 0.0):
        return

    writeServoAngle(angleDiff)
    servoAngle = nextAngle

## Updated M Drive with incremental angle once or continuously with delay
import time

def updateServoIncremental(cts, incAngle, stopAngle, delay):
    global servoAngle

    if (cts): # Algorithm for continous incremental movement
        while(checkServoLimits(incAngle)):
            writeServoAngle(incAngle)
            servoAngle = servoAngle + incAngle

            if (incAngle == 0): # Avoid infinite loop
                return
            if (servoAngle == stopAngle):
                return
            if (incAngle > 0 and servoAngle+incAngle > stopAngle):
                print('ServoError: Angle movement exceeds stop angle')
                return
            if (incAngle < 0 and servoAngle+incAngle < stopAngle):
                print('ServoError: Angle movement exceeds stop angle')
                return

            time.sleep(delay)

    else: # Algorithm for single incremental movement
        if (checkServoLimits(incAngle)):
            writeServoAngle(incAngle)
            servoAngle = servoAngle + incAngle

## Check if an angle increment is within limtis
def checkServoLimits(incAngle):
    global servoAngle
    testAngle = servoAngle + incAngle

    if (testAngle >= -90.0 and testAngle <= 90.0):
        return True
    else:
        print('ServoError: Angle movement exceeds servo limits')
        return False

## Write an angle to the servo via premade serial connection
def writeServoAngle(angle):
    ## Move relative
    toWrite = 'mr {}\r\n'.format(int(angle * 51200.0 / 360.0))
    ioWrite(toWrite)
