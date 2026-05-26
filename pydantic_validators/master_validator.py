from pydantic import BaseModel, BeforeValidator, StringConstraints, field_validator, SecretStr
from email_validator import EmailNotValidError, validate_email
from typing import Annotated


# email validation version 3.1
def process_mail(value: str):
    '''
    we will technically only get verified email here (email and login module TBD as of 22nd Feb)
    For now, I am adding from external library (I know we hate it mutually when we have to add external dependencies, but this is for MVP only)
    #Todo: make sure your custom email validator name is not same.
    '''
    try:
        validated_email = validate_email(value, check_deliverability=False)
        email = validated_email.normalized
        return email
    except EmailNotValidError as e:
        raise e


mail = Annotated[str, BeforeValidator(process_mail)]
class Mail(BaseModel):
    value: mail



uname = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=20,
        pattern=r'^[a-z0-9_.]+$' 
        # Not allowing white spaces either. But we strip them before validation so that's fine. 
        # No capitalized letters either because they are lowered before validation
    )
]

prohibited_usernames = {"admin", "root", "system", "null", "undefined"}
class UserName(BaseModel):
    '''
    constraints
    before
    after
    '''
    value: uname

    
    # BEFORE VALIDATOR
    @field_validator("value", mode="before")
    def normalize_uname(cls, v: str):
        if isinstance(v, str): #type: ignore
            return v.strip().lower()
        # if not string let it go as is, validation will catch it properly
        return v
    
    # AFTER VALIDATOR
    @field_validator("value")
    def check_username_rules(cls, v: str):
        if v.startswith("_") or v.endswith("_") or v.startswith(".") or v.endswith("."):
            raise ValueError("Username cannot start or end with '_' or '.'")
        
        if ".." in v or "__" in v:
            raise ValueError("Username cannot contain consecutive periods or underscores")
        
        if v in prohibited_usernames:
            raise ValueError("Username is prohibited")

        return v
    

password = Annotated[
    SecretStr,
    StringConstraints(
        min_length=8,
        max_length=64,
    )
]


class Password(BaseModel):
    value: password


    # BEFORE VALIDATOR
    @field_validator("value", mode="before")
    def stip_password(cls, v: str):
        if isinstance(v, str): #type: ignore
            return v.strip()
        return v
    
    # AFTER VALIDATOR
    @field_validator("value")
    def check_password_rules(cls, v: SecretStr):
        if " " in v.get_secret_value():
            raise ValueError("Password cannot contain spaces")
        

