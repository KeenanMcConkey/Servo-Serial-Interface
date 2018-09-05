# Servo-Serial-Interface

## Interface for Serial Control of M Drive Servo Motor

### Libraries

#### PySerial
https://github.com/pyserial/pyserial

#### Flask
https://github.com/pallets/flask

### Setup

#### Mac:
Install **Silicon Labs USB to UART Driver**  
Port `/dev/cu.SLAB_USBtoUART`

```
export FLASK_APP=SerialWebUI.py
flask run
```

#### Windows:
Port `COM9`

```
set FLASK_APP=SerialWebUI.py
flask run
```

Server is at localhost `127.0.0.1:5000`

### To-Do
1. ~~Add delay to incremental movements.~~  
2. ~~Show current angle on web interface~~
3. Change number of steps in motor for more precise movements.  
4. Add homing feature to start servo at angle 0.  
5. Make separate threads for web interface and serial.

### Issues
1. Angle is reset every time server is restarted.  
2. Sometimes current angle is displayed with too many decimal points.  
3. Web interface is useless when serial is connected.

---

*Created by Keenan McConkey*
