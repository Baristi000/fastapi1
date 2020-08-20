import serial
import os
import time

list_path = os.popen('ls -al /dev/ | grep tty.SLAB_USBtoUART | awk \'{print $10}\'').read()
list_path = list_path.rstrip().split('\n')

class Device:
    device_data = {}
    device_status = {}

def main():
    for path in list_path:
        path = "/dev/{}".format(path)
        print('init port: ' + path)
        port = serial.Serial(path, 9600, timeout=5)
        time.sleep(0.5)
        port.write(b'AT+CUSD=1,"*123#",15\r')
        time.sleep(1)
        response = port.readlines()
        if len(response) >= 2 and len(response[1].decode("utf-8", errors="ignore")) > 16:
            phone_number = response[1].decode("utf-8", errors="ignore")[10:-6]
        else:
            phone_number = ""
        if phone_number == "":
            print("Try to get phone number again!")
            port.write(b'AT+CUSD=1,"*101#",15\r')
            time.sleep(3)
            response = port.readlines()
            if len(response[1].decode("utf-8", errors="ignore")) > 16:
                phone_number = response[1].decode("utf-8", errors="ignore")[10:-6]
            else:
                phone_number = "unknown"
        print("success, phone number is: " + phone_number)
        Device.device_data[phone_number] = port
        Device.device_status[phone_number] = {"port": path}
        port.write(b'AT+CPMS?\r')
        time.sleep(1)
        result_check = port.readlines()
        sms_storage = result_check[1].decode("utf-8", errors="ignore").split(',')[1]
        if int(sms_storage) > 30:
            print('delete all sms')
            port.write(b'AT+QMGDA="DEL ALL"\r')
            time.sleep(5)
        port.write(b'AT+CMGF=1\r')  # Set Sim receive SMS turn to text mode
        port.write(b'AT+CSCS="GSM"\r')  # Set character to GSM


main()