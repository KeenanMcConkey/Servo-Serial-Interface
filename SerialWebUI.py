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
    print('Invalid OS!')

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
serIO.write('fd\n') ## Reset servo to factory defaults
serIO.flush()

# Create a web interface to take data from using Flask
from flask import Flask, render_template, request, url_for
app = Flask(__name__)

## Index page
@app.route('/')
def index():
    return render_template('mdrive.html')

## Incremental form submission
@app.route('/handleIncremental', methods=['POST'])
def handleIncremental():
    cts = request.form['cts']
    if (cts == 't'):
        cts = True
    else:
        cts = False

    incAngle = float(request.form['incAngle'])
    stopAngle = request.form['stopAngle']

    if (stopAngle != ""):
        stopAngle = float(stopAngle)

    updateServoIncremental(cts, incAngle, stopAngle)
    return render_template('mdrive.html')

## Specific form submission
@app.route('/handleSpecific', methods=['POST'])
def handleSpecific():
    nextAngle = float(request.form['angle'])

    updateServoSpecific(nextAngle)
    return render_template('mdrive.html')

## Update M Drive servo with specific angle
def updateServoSpecific(nextAngle):
    global servoAngle
    angleDiff = nextAngle - servoAngle;

    if (angleDiff == 0.0):
        return

    writeServoAngle(angleDiff)
    servoAngle = nextAngle

## Updated M Drive with incremental angle once or continuously
def updateServoIncremental(cts, incAngle, stopAngle):
    global servoAngle

    if (cts): # Algorithm for continous incremental movement
        while(checkServoLimits(incAngle)):
            writeServoAngle(incAngle)
            servoAngle = servoAngle + incAngle

            if (servoAngle == stopAngle):
                return
            if (servoAngle + incAngle > stopAngle):
                print('ServoError: Angle movement exceeds stop angle')
                return

    else: # Algorithm for single incremental movement
        if (checkServoLimits(incAngle)):
            writeServoAngle(incAngle)
            servoAngle = servoAngle + incAngle

## Check if an angle increment is within limtis
def checkServoLimits(incAngle):
    global servoAngle
    testAngle = servoAngle + incAngle

    if (testAngle > 0.0 and testAngle < 600.0):
        return True
    else:
        print('ServoError: Angle movement exceeds servo limits')
        return False

## Write an angle to the servo via premade serial connection
def writeServoAngle(angle):
    ## Move relative
    toWrite = 'mr {}\r\n'.format(int(angle * 51200.0 / 360.0))
    ## Servo only accepts UTF-8 encoding
    toWrite.encode(encoding='UTF-8')

    serIO.write(toWrite)
    serIO.flush()
