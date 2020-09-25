import time,re
import mysql.connector
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
#SLAB_USBtoUAR
def SLAB_USBtoUAR(res):
    for i in range(2):
        res.pop(0)
    return(res)
#check signal in realtime
def check_signal(port):
    r = 0
    while r == 0:
        r = port.inWaiting()
    time.sleep(1)
#write script into port
def port_write(port,script:str,cb = None):
    port.write(script.encode())
    check_signal(port)
    res = port.readlines()
    if cb == None:
        return(res)
    else:
        return cb(res)
#trying to get response in tries time
def try_to_get_res(script,port,tries:int,cb = None):
    n = 0
    while True:
        res = port_write(port,script)
        t = ""
        for r in res :
            t = t+r.decode("utf-8",errors="ignore")
        if (("+CUSD: 2"in t) or ("+CUSD: 4"in t) or ("ERROR" in t) or (len(res)<3)) and n < tries:
            pass
        else:
            break
    if n==10:
        return({"type": False,
                "text" : port.name})
    elif cb == 0:
        return({"type": True,
                "text" : res})
    elif cb == None:
        return({"type": True,
                "text" : SLAB_USBtoUAR(res)})
    else:
        return({"type": True,
                "text" : cb(res)})
#get message-------------------------
def get_message(Device, index, cb =None):
    script = "AT+CMGR={}\r".format(index)
    res = port_write(Device.status["port"],script)
    info = sms_info(res)
    if cb != None:
        res = cb(res)
    raw_sms = ""
    for r in res:
        r = r.decode("utf-8",errors="ignore")
        raw_sms = raw_sms + r
    otp = get_otp(res)
    if otp == "":
        print("message is stored without otp")
    else:
        print("message is stored with otp: "+otp)
    q = "insert into  message values(\""+Device.data["phone_number"]+"\",\""+info["time"]+"\",\""+otp+"\",\""+raw_sms+"\",\""+info["phone"]+"\",\""+info["date"]+","+info["time"]+"\",\"1\");"
    #get_info(q)
    print(q)
    isfull(Device.status["port"],index)
    return(res)
#check sim store full or not and remove all messages when full
def isfull(port,index):
    index = int(index)
    if index > 30:
        while True:
            str = "AT+CMGD=1,4\r"
            res = port_write(port,str)
            for r in res:
                if "OK" in r:
                    return True
                    break
    else:
        return False
#check and get otp:
def get_otp(res:list):
    otp = ""
    for r in res:
        r = r.decode("utf-8",errors="ignore")
        if len(re.findall('\d{6}', r))!=0:
            otp = re.findall('\d{6}', r)[0]
            break
    return otp
#check expire date:
def is_expired(res:list):
    date = []
    for r in res:
        r = r.decode("utf-8",errors="ignore")
        if len(re.findall("[0-9]+/[0-9]+/[0-9]+",r))!=0:
            date = re.findall("[0-9]+/[0-9]+/[0-9]+",r)
            break
    if date == []:
        return ("")
    else:
        return date[0]
#get message infor
def sms_info(res:list):
    for r in res:
        r = r.decode("utf-8",errors="ignore")
        if "+CMGR:" in r:
            phone = re.findall("[0-9]+",r)[0]
            date = re.findall("[0-9]+/[0-9]+/[0-9]+",r)[0]
            time = re.findall("[0-9]+:[0-9]+:[0-9]+",r)[0]
            return ({"phone":phone,
                     "date":date,
                     "time":time})
