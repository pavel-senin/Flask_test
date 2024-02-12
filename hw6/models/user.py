# Таблица пользователей должна содержать следующие поля:
# id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    user_id: int
    firstname: str = Field(..., title='first name', max_length=40)
    lastname: str = Field(..., title='last name', max_length=80)
    email: EmailStr = Field(..., title='emai', max_length=120)


class UserIn(User):
    password: str = Field(..., title='password', min_length=6, max_length=20)