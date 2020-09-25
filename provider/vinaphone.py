from provider import sim_processing
import re

sim = sim_processing
#check balance
def balance(Device,tries:int):
    port = Device.status["port"]
    str='AT+CUSD=1,"*101#",15\r'
    res = sim.try_to_get_res(str,port,tries)
    if res["type"]:
        res = res["text"]
        for r in res:
            r = r.decode("utf-8", errors = "ignore")
            if "+CUSD: 0" in r:
                r = r.split(",")[1].split("=")[1].split(" ")[0]
                if "None" in r:
                    return("unsupport")
                else:
                    return(r)
    else:
        return("error")

#get phone number
def get_num(port,tries:int):
    str = 'AT+CUSD=1,"*110#"\r'
    res = sim.try_to_get_res(str,port,tries)
    if res["type"]:
        for r in res["text"]:
            print(r.decode("utf-8",errors="ignore"))
        res = re.findall("[0-9]+",res["text"][0].decode("utf-8",errors = "ignore").split(",")[1])
        print(res)
        text = ""
        for r in res:
            text += r
        return (text)
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
    port = Device.status["port"]
    str='AT+CUSD=1,"*101#",15\r'
    res = sim.try_to_get_res(str,port,tries)
    if res["type"]:
        res = res["text"]
        for r in res:
            r = r.decode("utf-8", errors = "ignore")
            if "Han su dung" in r:
                r = re.findall("[0-9]+/[0-9]+/[0-9]+",r)
                return(r[0])
    else:
        return("error")