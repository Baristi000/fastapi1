from typing import Optional
from fastapi import FastAPI, Form
import mysql.connector
import responses, requests, json
import uvicorn

app = FastAPI()
db = mysql.connector.connect(user='trieu', 
                     password='T123',
                     host='localhost',
                     database='trieudb')

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{id}")
def read_item(id: int, q: Optional[str] = None):
    return {"id": id, "q": id+1}

@app.post("/get-input/")
async def input1(name: str = Form(...)):
    q = "INSERT INTO table1 (name) VALUES('"+name+"');"
    db.cursor().execute(q)
    db.commit()
    return {"name": name}

@app.get("/get-data")
def lelect_id(id : str):
    q = "SELECT * FROM table1 WHERE ID = "+id+";"
    db.cursor().execute(q)
    r = db.cursor().fetchall()
    x = {id: r[0][0], name:r[0][1]}
    return x

@app.post("/delete")
def delete_id(id: str):
    q = "DELETE FROM table1 WHERE ID = "+id+";"
    db.cursor().execute(q)
    r = db.cursor().fetchall()
    print(r)

@responses.activate
@app.get("/slack")
def send_mes(messages: str):
    slack_url = "https://hooks.slack.com/services/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"
    payload={"text": messages}
    data = json.dumps(payload)
    res = requests.post(slack_url,data,headers={'content-type': 'application/json'},)
    print(json.loads(data))
    print(data)
    return data

@app.get("/get-json")
def set_json():
    a = {"key1": "hahaa",
        "key2": "hihii",
        "key3": "hohoo"}
    b = json.dumps(a)
    c = json.loads(b)
    print(c["key2"])
    return c

uvicorn.run(app, host="0.0.0.0", port= -5000, log_level="info")