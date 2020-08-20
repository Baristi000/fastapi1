from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


password = "$2b$12$5PqYyMn4gtELzBuOLO8Bhe6N1l4esxUjoC7O/PxL6D3imVuKmCuJe"
hs1 = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

hs = pwd.hash(password)
#print("password: "+password+"\nhashed: "+hs)

print(pwd.verify(password, hs1))