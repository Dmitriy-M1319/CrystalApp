import re

from pydantic import BaseModel, EmailStr, ValidationError, validator


_password_regex: str = r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d).*$'


class Token(BaseModel):
    access_token: str


class AuthenticateUserData(BaseModel):
    email: EmailStr
    password: str


class PasswordUpdate(BaseModel):
    new_password: str
    new_password_confirm: str

    @validator('new_password')
    def validate_password(cls, passwd: str):
        if re.match(_password_regex, passwd) is None:
            raise ValidationError("password doesn't match with template")
        return passwd

    @validator('new_password_confirm')
    def validate_password_confirm(cls, passwd: str, values):
        if 'new_password' in values and passwd != values['new_password']:
            raise ValidationError("passwords don't match")
        return passwd
