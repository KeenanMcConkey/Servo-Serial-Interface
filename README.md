# Servo-Serial-Interface

#### Interface for Serial Control of M Drive Servo Motor

---
### Libraries

#### PySerial

https://github.com/pyserial/pyserial

#### Flask

https://github.com/pallets/flask

---
### Setup

```
FLASK_APP=SerialWebUI.py
flask run
```

#### Mac:
Port `/dev/cu.SLAB_USBtoUART`

Uses **Silicon Labs USB to UART Driver**
#### Linux:
Port `/dev/ttysUSB0`

#### Windows:
Port `COM9`

### To-Do
Add **homing** feature to start motor at 0

Add current angle **feedback** to web interface

---
*Created by Keenan McConkey*
