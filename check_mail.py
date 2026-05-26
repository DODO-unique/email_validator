from pydantic_validators.payload_validator import UserRegisterPayload
from uuid import uuid4


async def create_otp(package: UserRegisterPayload):
    # verified email of the user
    email = package.email

    # OTP here.
    OTP = uuid4()





