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
    print('Error: Unknown OS')

# Create serial connection with Servo using PySerial
import serial
import io

ser = serial.Serial(port)
print(" * Port: {}".format(ser.port))
print(" * Baudrate: {}".format(ser.baudrate))
serIO = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
serIO.write("fd") ## Reset servo to factory def

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
    dir = request.form['dir']
    cts = request.form['cts']
    incAngle = request.form['incAngle']
    stopAngle = request.form['stopAngle']

    if (incAngle != ""):
        incAngle = float(incAngle)
    if (stopAngle != ""):
        stopAngle = float(stopAngle)

    updateServoIncremental(dir, cts, incAngle, stopAngle)
    return render_template('mdrive.html')

## Specific form submission
@app.route('/handleSpecific', methods=['POST'])
def handleSpecific():
    nextAngle = float(request.form['angle'])

    updateServoSpecific(nextAngle)
    return render_template('mdrive.html')

## Automatically run in debug mode
if __name__ == '__main__':
    app.run(debug = True)

## Update M Drive servo with specific angle
def updateServoSpecific(nextAngle):
    global servoAngle
    angleDiff = nextAngle - servoAngle;

    if (angleDiff == 0):
        return

    writeServoAngle(angleDiff)
    servoAngle = nextAngle

## Updated M Drive with incremental angle once or continuously
def updateServoIncremental(dir, cts, incAngle, stopAngle):
    if (dir == neg):
        incAngle = incAngle * -1

    if (cts == f):
        if (checkServoLimits(incAngle)):
            writeServoAngle(incAngle)
            servoAngle = servoAngle + incAngle
        else:
            print('Angle movement exceeds servo limits')
    else:
        while(checkServoLimits(incAngle)):
            writeServoAngle(incAngle)
            servoAngle = servoAngle + incAngle

            if (servoAngle == stopAngle):
                return
            if (servoAngle + incAngle > stopAngle):
                print('Angle movement exceeds stop angle')
                return
        print('Angle movement exceeds servo limits')

## Check if an angle increment is within limtis
def checkServoLimits(incAngle):
    testAngle = servoAngle + incAngle

    if (testAngle > 0.0 and testAngle < 600.0):
        return true
    else:
        return false

## Write an angle to the servo via premade serial connection
def writeServoAngle(angle):
    ## Move relative amount
    serIO.write("mr {}\n".format(angle * (51200.0 / 360.0)))
    serIO.flush()
