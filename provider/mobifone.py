from provider import sim_processing
import re

sim = sim_processing
#check balance
def balance(Device,tries:int):
    str='AT+CUSD=1,"*101#",15\r'
    port = Device.status["port"]
    res = sim.try_to_get_res(str,port,tries)
    if res["type"]:
        res = res["text"]
        for r in res:
            r = r.decode("utf-8", errors = "ignore")
            if "+CUSD: 0" in r:
                return(r.split(",")[1].split(":")[1].split(" ")[0])
    else:
        return("error")

#get phone number
def get_num(port,tries:int):
    str = 'AT+CUSD=1,"*0#"\r'
    phone = []
    while True:
        res = sim.try_to_get_res(str,port,tries)
        if res["type"]:
            phone = re.findall("\d{11}",res["text"][1].decode("utf-8",errors="ignore"))
            if len(phone)==0:
                pass
            else:
                break
    return (phone[0])

#input money
def recharge(port,code):
    str='AT+CUSD=1,"*100*{}#",15\r'.format(code)
    res = sim.port_write(port,str)
    for r in res:
        r = r.decode("utf-8", errors = "ignore")
        text = text+r
    if text == "":
        return({"Response":"errors"})
    else:
        return({"Response":text})

#expired date
def check_expired(port,tries:int):
    str='AT+CUSD=1,"*101#",15\r'
    res = sim.try_to_get_res(str,port,tries)
    if res["type"]:
        res = res["text"]
        for r in res:
            r = r.decode("utf-8", errors = "ignore")
            if "+CUSD: 0," in r:
                r = re.findall("[0-9]+/[0-9]+/[0-9]+",r)[0]
                return(r)

    else:
        return("error")