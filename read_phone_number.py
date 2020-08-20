import serial
import os
import time

list_path = os.popen('ls -al /dev/ | grep tty.SLAB_USBtoUART | awk \'{print $10}\'').read()
list_path = list_path.rstrip().split('\n')
path = "/dev/{}".format(list_path[0])
print("path: ")
print(path)
port = serial.Serial(path, 9600, timeout=1)
time.sleep(0.5)
port.write(b'AT+CUSD=1,"*102#",15\r')
time.sleep(2)
res = port.read(1000)
res=res.decode("utf-8", errors="ignore")
res = res.rstrip().split('\n')
print("respone:")
print("phone number is: "+str(res[3][19:29]))
