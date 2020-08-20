import serial
import os
import time

port = serial.Serial("/dev/tty.SLAB_USBtoUART", 9600, timeout=1)
time.sleep(0.5)
#check module is working or not
port.write(b'AT+CPIN?,15\r')
#port.write(b'ATD0933576099\r')
time.sleep(5)
rcv = port.read(1000).decode("utf-8", errors="ignore").rstrip()
print(rcv)
