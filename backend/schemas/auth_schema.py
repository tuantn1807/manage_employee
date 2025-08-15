from pydantic import BaseModel

class LoginByUsername(BaseModel):
    uname: str
    pwd: str
