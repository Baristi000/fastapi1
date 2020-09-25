from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request, Response, Header 
from sqlalchemy.orm import Session
from models import user
from db.database import SessionLocal, engine
from api.api_v1.api import api_router
user.Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector, responses, requests, json
import serial, os, time, queue
from fastapi_utils.tasks import repeat_every
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from provider import vinaphone, mobifone, viettel, vietnamobile, sim_processing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

app.include_router(api_router)

#declare------------------------------------------
list_port_url = ["tty.SLAB_USBtoUART"]
sim = sim_processing
gateway = sim.SLAB_USBtoUAR
trial = 10
providers = {"45204":"viettel",
             "45201":"mobifone",
             "45202":"vinaphone",
             "45205":"vietnamobile",
             "i-tel":"vietnamobile",
             "45208":"vietnamobile"}


#class device informaiton
class Device():
    data = {}
    status = {}


#function------------------------------------------
#auto+condition
#open mysql connection
def connection():
    cnx = mysql.connector.connect(user='trieu', 
                                    password='T123',
                                    host='localhost',
                                    database='sim_card_management')
    return cnx
#execute query 
def get_info(q):
    cnx = connection()
    cursor = cnx.cursor()
    cursor.execute(q)
    if q.split()[0].upper()=="SELECT":
        r = cursor.fetchall();
        cnx.close()
        cursor.close()
        return(r)
    else:
        cnx.commit()
        cnx.close()
        cursor.close()
#check ready of thread
def check_ready(name:str,cThread:list):
    while True:
        time.sleep(0.2)
        if (cThread[0].getName() == name):
            break
    return True
#check provider
def check_provider(port):
    while True:
        str = 'AT+CIMI\r'
        res = sim.port_write(port, str)
        if res != []:
            break
    res = res[1].decode("utf-8", errors="ignore")[0:5]
    if providers[res] == "vinaphone":
        print("vinaphone")
        return(vinaphone)
    elif providers[res] == "mobifone":
        print("mobifone")
        return(mobifone)
    elif providers[res] == "viettel":
        print("viettel")
        return(viettel)
    elif providers[res] == "vietnamobile":
        print("vietnamobile")
        return(vietnamobile)
#check sim number
def check_sim(Device):
    cnx = connection()
    cursor = cnx.cursor()
    port = Device.status["port"]
    phone_number = Device.status["provider"].get_num(port,trial)
    q="select * from sim where sim_number = '"+phone_number+"';"
    r = get_info(q)
    if r == []:
        q = "insert into sim values('tty.SLAB_USBtoUART','"+phone_number+"','none');"
        cursor.execute(q)
        cnx.commit()
        print("not exist")
    cnx.close()
    return phone_number
#check incoming message
def check_message(Device):
    print("checking ...")
    port = Device.status['port']
    signal = port.readlines()
    full = 0
    if len(signal)>0:
        for element in signal:
            element = element.decode("utf-8",errors="ignore").rstrip().split(",")
            if(element[0]=='+CMTI: "SM"'):
                index = element[1]
                if int(index)>30:
                    full = 1
                print("index: "+index)
                sim.get_message(Device,index,gateway)
#open port 
def open_port(list_port_url):
    list_Device = []
    for port_url in list_port_url:
        cmd = 'ls -al /dev/ | grep '+port_url+' | awk \'{print $10}\''
        list_path = os.popen(cmd).read()
        list_path = list_path.rstrip().split('\n')
        path = "/dev/{}".format(list_path[0])
        port = serial.Serial(path, 9600, timeout=3)
        Device.status["port"] = port
        Device.status["provider"] = check_provider(port)
        Device.status["cThread"] = []
        Device.data["phone_number"] = check_sim(Device)
        print("phone number: "+Device.data["phone_number"])
        list_Device.append(Device)
    return(list_Device)
#check mass
def checkmass():
    for Device in list_Device:
        q = queue.Queue()
        t = Thread(target= lambda queue,arg : queue.put(check_message(arg)),args=(q,Device,))
        Device.status["cThread"].append(t)
        while not(check_ready(t.getName(),Device.status["cThread"])):
            pass
        t.start()
        t.join()
        Device.status["cThread"].pop(0)

#manual
#get*101#
def single_check_balance(Device,trial:int):
    r = ""
    while True:
        q = queue.Queue()
        t = Thread(target= lambda queue,Device,trial : queue.put(Device.status["provider"].balance(Device, trial)),args=(q,Device,trial,))
        Device.status["cThread"].append(t)
        while not(check_ready(t.getName(),Device.status["cThread"])):
            pass
        t.start()
        t.join()
        Device.status["cThread"].pop(0)
        r = q.get()
        if r!="" and r!=None:
            break
    return ({Device.data["phone_number"]:r})
#expired date
def single_check_expried(Device,trial:int):
    r = ""
    while True:
        q = queue.Queue()
        t = Thread(target= lambda queue,Device,trial : queue.put(Device.status["provider"].check_expired(Device, trial)),args=(q,Device,trial,))
        Device.status["cThread"].append(t)
        while not(check_ready(t.getName(),Device.status["cThread"])):
            pass
        t.start()
        t.join()
        Device.status["cThread"].pop(0)
        r = q.get()
        if r!="" and r!=None:
            break
    return ({Device.data["phone_number"]:r})

list_Device = open_port(list_port_url)

#API
@app.on_event("startup")
@repeat_every(seconds=10) # 10 seconds 
def e():
    Thread(target=checkmass).start()


#check wallet
@app.get("/balance-{phone}",tags=["sim"])
def e(phone: str = Header(None)):
    for Device in list_Device:
       if phone == Device.data["phone_number"]:
            return ({"balance":single_check_balance(Device,trial)})
#check all wallet
@app.get("/balance_all",tags=["sim"])
def e():
    arr = {}
    thread_list = []
    exe = ThreadPoolExecutor()
    for Device in list_Device:
        t = exe.submit(single_check_balance,Device,trial)
        thread_list.append(t)
    for t in thread_list:
        arr.update(t.result())
    return ({"balance":arr})
#check expired date:
@app.get("/expired-date-{phone}",tags=["sim"])
def e(phone: str = Header(None)):
   for Device in list_Device:
       if phone == Device.data["phone_number"]:
            return ({"expired_date":single_check_expried(Device,trial)})
#check expired date of all sim
@app.get("/expired_date_all",tags=["sim"])
def e():
    arr = {}
    thread_list = []
    exe = ThreadPoolExecutor()
    for Device in list_Device:
        t = exe.submit(single_check_expried,Device,trial)
        thread_list.append(t)
    for t in thread_list:
        arr.update(t.result())
    return ({"expired_date":arr})
#push money into sim using code
@app.get("/push-money",tags=["sim"])
def e(code: str = Header(None), phone: str = Header(None),tags=["Sim"]):
    for Device in list_Device:
        if Device.data["phone_number"] == phone:
            return(Device.status["provider"].recharge(Device.status["port"],code))
#push money into sim using bank
