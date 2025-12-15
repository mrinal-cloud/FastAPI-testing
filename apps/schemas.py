from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserIn(User):
    password: str

class UserOut(User):
    id: int
    created_at: datetime

class UserPasswordChange(User):
    password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int


class Message(BaseModel):
    content: str
    

class MessageOut(Message):
    id: int
    parent_message_id: Optional[int] = None
    receiver_id: int
    sender: UserOut
    time_stamp: datetime

    class Config:
        # from_attributes = True
        orm_mode=True
    

class MessageIn(Message):
    pass
    #i will take in the sender id from the token
    #and take in the receiver id from the path parameter
    

