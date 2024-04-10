from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Signup(BaseModel):
    username: str
    password: str


class CreateChat(BaseModel):
    message: str


class AddMessage(BaseModel):
    message: str
