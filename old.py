import time
import serial
import os
import json
import requests
from time import strftime, localtime
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

app = FastAPI()
# list_path = os.popen('ls -al /dev/ | grep ttyXRUSB | awk \'{print $11}\'').read()
# list_path = os.popen('ls -al /dev/ | grep ttyACM | head -n 7 | awk \'{print $10}\'').read()
list_path = os.popen('ls -al /dev/ | grep ttyACM | awk \'{print $10}\'').read()
list_path = list_path.rstrip().split('\n')
print("run file")


class Device:
    device_data = {}
    device_status = {}


def parse_response(response):
    error_message = ""
    error_code = 0
    data = []
    print(response.text)
    if hasattr(response, 'text'):
        try:
            response_data = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            error_code = 500
            error_message = "Something wrong with Passport server"
        else:
            error_code = int(response_data["code"])
            error_message = response_data["message"]
            data = response_data["data"]
    return {
        "response_code": error_code,
        "response_message": error_message,
        "response_data": data
    }


def connect_with_retry(url, payload, headers):
    retry = 3
    response = {}
    while retry > 0:
        try:
            response = requests.request("POST", url, data=payload,
                                        headers=headers)
        except requests.exceptions.RequestException:
            print("Connect to passport failed, retrying...")
            retry = retry - 1
            time.sleep(40)
        else:
            break
    data_parse = parse_response(response)
    print("try: ", retry, "data_parse: ", data_parse)
    if retry > 0 and int(data_parse["response_code"]) == 0:
        zero_code_retry_times = 3
        while zero_code_retry_times > 0:
            print("zero code, retrying...")
            response = requests.request("POST", url, data=payload, headers=headers)
            data_parse = parse_response(response)
            if data_parse["response_code"] == 1:
                break
            else:
                zero_code_retry_times = zero_code_retry_times - 1
            # time.sleep(40)
    return data_parse


async def get_and_send_otp(device_slot):
    port = device_slot['port']
    phone_number = device_slot['phone']
    sms_available = port.readlines()
    print("check OTP in phone number: " + phone_number)
    code_otp = ""
    if len(sms_available) > 0:
        file = open("sms-phone.log", "a")
        file.write("-----------------------{}--------------------------".format(phone_number))
        for info in sms_available:
            if info.decode("utf-8", errors="ignore").split(',')[0] == '+CMTI: "SM"':
                index = info.decode("utf-8", errors="ignore").split(',')[1]
                port.write(b'AT+CMGR=' + index.encode() + b'\r')
                response = port.readlines()
                if int(index) > 30:
                    port.write(b'AT+QMGDA="DEL ALL"\r')
                    print("Full SMS memory, delete all...")
                    time.sleep(5)
                for data in response:
                    file.write(data.decode("utf-8", errors="ignore"))
                    time_stamp = strftime("%Y-%m-%d %H:%M:%S", localtime())

                    if data.decode("utf-8", errors="ignore").split(':')[0] == 'SHOPEE verification code':
                        code_otp = data.decode("utf-8", errors="ignore").split('.')[0][-6:]
                        print("New OTP code found in {} is {}".format(phone_number, code_otp))
                        Device.device_status[phone_number]["otp"] = code_otp

                        passport_url = "https://api-staging-passport.epsilo.io/receive-otp/shopee"

                        passport_payload = "{\"phone\": \"" + phone_number + "\", \"otp\": \"" + code_otp + \
                                           "\", \"timestamp\": \"" + time_stamp + "\"}"
                        passport_headers = {
                            'accept': "application/json",
                            'cache-control': "no-cache"
                        }
                        passport_response = connect_with_retry(passport_url, passport_payload, passport_headers)
                        print("passport_response: ", passport_response)
                        passport_response_error_code = int(passport_response["response_code"])
                        error_message = passport_response["response_message"]
                        slack_url = "https://hooks.slack.com/services/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"
                        slack_headers = {
                            'accept': "application/x-www-form-urlencoded",
                            'cache-control': "no-cache"
                        }

                        if passport_response_error_code == 1:
                            print("send success")
                            passport_response_data = dict(passport_response["response_data"])
                            shop_name = passport_response_data["shopName"]
                            country = passport_response_data["country"]
                            slack_payload = "{\"channel\": \"#alert-otp\", \"text\": \"\n>Phone number: " \
                                            + phone_number + "\n>OTP: *" + code_otp + "*\n>Time: " + time_stamp \
                                            + "\n>Shop: " + shop_name + "\n>Country: " + country + "\n>\"}"
                        else:
                            print("send failed")
                            slack_payload = "{\"channel\": \"#alert-otp\", \"text\": \"\n>Phone number: " \
                                            + phone_number + "\n>OTP: *" + code_otp + "*\n>Time: " + time_stamp \
                                            + "\n>Error: " + error_message + "\n>\"}"
                        print("slack_url", slack_url, "slack_payload", slack_payload, "slack_headers", slack_headers)
                        response_slack = requests.request("POST", slack_url, data=slack_payload
                                                          , headers=slack_headers)
                        print(response_slack.text)

        file.close()
    return code_otp


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
            port.write(b'AT+CUSD=1,"*123#",15\r')
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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/status/")
def view_slot():
    return Device.device_status


@app.on_event("startup")
@repeat_every(seconds=30)  # 30 sec
async def mass_check():
    device_slot = {}
    for phone_number in Device.device_data:
        device_slot['phone'] = phone_number
        device_slot['port'] = Device.device_data[phone_number]
        await get_and_send_otp(device_slot)