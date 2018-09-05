# Servo-Serial-Interface

### Interface for Serial Control of M Drive Servo Motor

---

### Libraries

#### PySerial

https://github.com/pyserial/pyserial

#### Flask

https://github.com/pallets/flask

---

### Setup

#### Mac:
Install **Silicon Labs USB to UART Driver**

Port `/dev/cu.SLAB_USBtoUART`

```
FLASK_APP=SerialWebUI.py
flask run
```

#### Windows:
Port `COM9`

```
set FLASK_APP=SerialWebUI.py
flask run
```

---

### To-Do
Add **homing** feature to start servo at angle 0

Add **angle feedback** to web interface

Add **servo feedback** for continuous movement

---

### Issues

Continuous movement not working due to missing feedback

---

*Created by Keenan McConkey*
