from provider import sim_processing

sim = sim_processing
#check balance
def balance(Device,tries:int):
    str = 'AT+CUSD=1,"*101#",15\r'
    port = Device.status["port"]
    result = ""
    while True:
        result = ""
        res = sim.try_to_get_res(str,port,tries)
        if res["type"]:
            for r in res["text"]:
                if "0.Quay lai" in r.decode("utf-8",errors="ignore"):
                    result = "False"
                    str = 'AT+CUSD=1,"0"\r'
            if result == "":
                for r in res["text"]:
                    r = r.decode("utf-8",errors="ignore")
                    if "+CUSD: 1" in r:
                        result = r.split(",")[1].split(":")[1].split("d")[0].strip()
                break
        else:
            result = "error"
            break
    return(result)

#get phone number-------------
def get_num(port,tries:int):
    str = 'AT+CUSD=1,"*098#"\r'
    result = ""
    while True:
        result = ""
        res = sim.try_to_get_res(str,port,tries)
        if res["type"]:
            for r in res["text"]:
                if "0.Quay lai" in r.decode("utf-8",errors="ignore"):
                    result = "False"
                    str = 'AT+CUSD=1,"0"\r'
            if result == "":
                result = res["text"][0].decode("utf-8",errors="ignore").split(",\"")[1].split()[1]
                break
        else:
            result = "error"
            break
    return(result)

#input money
def recharge(port,code):
    text = ''
    port.write('AT+CUSD=1,"*100*{}#",15\r'.format(code).encode())
    sim.check_signal(port)
    res = port.readlines()
    for r in res:
        r = r.decode("utf-8", errors = "ignore")
        text = text+"\n"+r
    if text == "":
        return({"Response":"errors"})
    else:
        return({"Response":text})
