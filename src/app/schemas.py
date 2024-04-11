from pydantic import BaseModel


class Login(BaseModel):
    """
    Represents the login credentials of a user.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """

    username: str
    password: str


class Signup(BaseModel):
    """
    Represents the signup credentials of a user.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """

    username: str
    password: str


class CreateChat(BaseModel):
    """
    Represents the data required to create a chat.

    Attributes:
        message (str): The message content of the chat.
    """

    message: str


class AddMessage(BaseModel):
    """
    Represents the data required to add a message to a chat.

    Attributes:
        message (str): The message content to be added.
    """

    message: str
