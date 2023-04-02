import clr
import time
import pyuac
import serial
import time
import pystray
import threading
import sys
import os
clr.AddReference("OpenHardwareMonitorLib")
from OpenHardwareMonitor.Hardware import Computer, HardwareType, SensorType
from PIL import Image



def on_quit():
    icon.stop()
    sys.exit()


if hasattr(sys, '_MEIPASS'):
    # Running in a PyInstaller bundle
    image_path = os.path.join(sys._MEIPASS, 'icon.png')
else:
    # Running as a standalone script
    image_path = 'icon.png'


computer = Computer()
sensors = []
sensorIdentifers = ["/amdcpu/0/temperature/0", "/amdcpu/0/load/0", "/nvidiagpu/0/temperature/0", "/nvidiagpu/0/load/0", "/ram/load/0"]

def setupComputer():
    computer.CPUEnabled = True
    computer.GPUEnabled = True
    computer.RAMEnabled = True
    computer.HDDEnabled = True
    computer.Open()
    updateComputer()


def updateComputer():
    for a in computer.Hardware:
        a.Update()     

def findSensor(identifier):
    allSensors = []
    for hardware in computer.Hardware:
         for sensor in hardware.Sensors:
              allSensors.append(sensor)
    for sensor in allSensors:
        if sensor.Identifier.ToString() == identifier:
            return sensor
    return None

def sendToSerial():
    values = []
    for sensorIdentifier in sensorIdentifers:
            unfomatedValue = findSensor(sensorIdentifier).Value
            formatted = "{:.2f}".format(unfomatedValue)
            values.append(formatted)
    serialString = ','.join(values)
    print(serialString)
    ser.write(serialString.encode('utf-8'))
    ser.flush()
    time.sleep(2)
    ser.flush()
    
def main():
     while True:
            updateComputer()
            sendToSerial()

try:
    if not pyuac.isUserAdmin():
            print("Re-launching as admin!")
            
            pyuac.runAsAdmin()
    else:    
        setupComputer()
        ser = serial.Serial('COM3', 9600)
        backgroundThread = threading.Thread(target=main)
        backgroundThread.daemon = True
        backgroundThread.start()
        if hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle
            image_path = os.path.join(sys._MEIPASS, 'icon.png')
        else:
            # Running as a standalone script
            image_path = 'icon.png'
        image = Image.open(image_path)
        menu = pystray.Menu(pystray.MenuItem('Quit', on_quit))
        icon = pystray.Icon('pcss', image, 'pcss', menu)
        icon.run()
        
    
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
    input("Press enter to exit")

