#working
from typing import Optional
import mysql.connector
import responses, requests, json
#authen
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


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
    a = "{\"key1\": \"hahaa\",\"key2\": \"hihii\",\"key3\": \"hohoo\"}"
    c = json.loads(a)
    print(c["key2"])
    return c
    


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "trieu.com",
        "hashed_password": "$2b$12$XnzNIHFiuU9FSCgXFOFgeO1X5UZLPTlf/7J8K0JWIw8Ev6tsTHsla",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#def verify_password(plain_password, hashed_password):
#    return pwd_context.verify(plain_password, hashed_password)


#def get_password_hash(password):
#    return pwd_context.hash(password)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if pwd_context.verify(form_data.password, fake_users_db["hashed_password"]) == true:
        print ("true")

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]