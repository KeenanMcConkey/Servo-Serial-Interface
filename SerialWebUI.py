# SerialWebUI handles hosting of HTML web interface and HTTP query parsing
# while also connecting to the M Drive servo when necessary

# Global variables
servoAngle = 0

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
    updateServoIncremental(dir, cts, incAngle, stopAngle)
    return render_template('mdrive.html')

## Specific form submission
@app.route('/handleSpecific', methods=['POST'])
def handleSpecific():
    nextAngle = request.form['angle']
    updateServoSpecific(nextAngle)
    return render_template('mdrive.html')

## Automatically run in debug mode
if __name__ == '__main__':
    app.run(debug = True)

# Connect to M Drive servo using PySerial
import serial
import io

## Update M Drive servo with specific anglew
def updateServoSpecific(nextAngle):
    ## Create serial connection with servo
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM8'
    ser.open()

    serIO = io.textIOWrapper(io.buffredRWPair(ser, ser))
    serIO.write("mr ")
    serIO.write(nextAngle * (51200 / 360))
    serIO.write("\n")
    serIO.flush()
    ser.close()

def updateServoIncremental(dir, cts, incAngle, stopAngle):
    ## Create serial connection with servo
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM8'
    ser.open()
    ser.close()
