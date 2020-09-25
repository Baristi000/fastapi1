from provider import sim_processing
import re

sim = sim_processing
#check balance
''' def balance(port,tries:int):
    str='AT+CUSD=1,"*101#",15\r'
    res = sim.try_to_get_res(str,port,tries)
    if res["type"]:
        res = res["text"]
        for r in res:
            print(r.decode("utf-8",errors="ignore"))
        if "+CUSD: 1" in res[0].decode("utf-8",errors = "ignore"):
            return(res["text"][0].decode("utf-8",errors = "ignore").split(":")[1].strip().split("d")[0])
    else:
        return("error") '''
def balance(Device,tries:int):
    str='AT+CUSD=1,"*101#",15\r'
    port = Device.status["port"]
    balance = ""
    indexs = []
    res = sim.try_to_get_res(str, port, tries, 0)["text"]
    for n in range(10):
        for r in res:
            r = r.decode("utf-8",errors="ignore")
            if "+CMTI: \"SM\"," in r:
                indexs.append(re.findall("[0-9]+",r)[0])
        for index in indexs:
            script = "AT+CMGR={}\r".format(index)
            res = sim.get_message(Device, index)
            for r in res:
                r = r.decode("utf-8",errors="ignore")
                if "TK Chinh: " in r:
                    balance = r.split("TK Chinh: ")[1].split("d,")[0]
                    break
            if balance != "":
                break
        if balance != "":
                break
        res = port.readlines()
    return balance

#get phone number
def get_num(port,tries:int):
    str = 'AT+CUSD=1,"*123#"\r'
    while True:
        res = sim.try_to_get_res(str,port,tries)
        if res["type"]:
             phone = re.findall("[0-9]+",res["text"][1].decode("utf-8",errors="ignore"))
             if len(phone) == 2:
                 return phone[1]
        else:
            return("error")

#input money
def recharge(port,code):
    str='AT+CUSD=1,"*100*{}#",15\r'.format(code)
    res = sim.port_write(port,str)
    for r in res:
        r = r.decode("utf-8", errors = "ignore")
        text = text+"\n"+r
    if text == "":
        return({"Response":"errors"})
    else:
        return({"Response":text})

#expired date
def check_expired(Device,tries:int):
    str='AT+CUSD=1,"*101#",15\r'
    port = Device.status["port"]
    date = ""
    indexs = []
    res = sim.try_to_get_res(str, port, tries, 0)["text"]
    for n in range(10):
        for r in res:
            r = r.decode("utf-8",errors="ignore")
            if "+CMTI: \"SM\"," in r:
                indexs.append(re.findall("[0-9]+",r)[0])
        for index in indexs:
            script = "AT+CMGR={}\r".format(index)
            res = sim.get_message(Device, index)
            for r in res:
                r = r.decode("utf-8",errors="ignore")
                if "het han" in r:
                    date = re.findall("[0-9]+/[0-9]+/[0-9]+",r)[0]
                    break
            if balance != "":
                break
        if date != "":
                break
        res = port.readlines()
    return date