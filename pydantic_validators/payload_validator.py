from master_validator import UserName, Password, Mail
from pydantic import BaseModel

class UserRegisterPayload(BaseModel):
    uname: UserName
    password: Password
    email: Mail