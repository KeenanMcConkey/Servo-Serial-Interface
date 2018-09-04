#!/usr/bin/env python

# Global variables
servoAngle = 0.0

# Create serial connection with Servo using PySerial
import serial
import io

ser = serial.Serial('/dev/cu.SLAB_USBtoUART')
print(" * Port: {}".format(ser.port))
print(" * Baudrate: {}".format(ser.baudrate))
serIO = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
serIO.write("fd")

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
    if (servoAngle == nextAngle):
        return
    toWrite = "mr {} \n".format(nextAngle * (51200.0 / 360.0))

    serIO.write(toWrite)
    serIO.flush()

    servoAngle = nextAngle

def updateServoIncremental(dir, cts, incAngle, stopAngle):
    serIO.write("MR 51200\n")
    ser.flush()
