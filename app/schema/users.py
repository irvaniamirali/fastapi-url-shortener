from pydantic import BaseModel, EmailStr, field_validator, constr

import re


class UserBase(BaseModel):
    user_id: int
    full_name: constr(strip_whitespace=True, max_length=50)
    email: EmailStr


class UserToken(BaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=8, max_length=25)


class UserCreate(BaseModel):
    email: EmailStr
    full_name: constr(strip_whitespace=True, max_length=50)
    password: constr(strip_whitespace=True, min_length=8, max_length=25)

    @field_validator("full_name")
    def fullname_must_not_be_empty(cls, value):
        if not value or value.isspace():
            raise ValueError("Fullname must not be empty or just whitespace")
        return value

    @field_validator("password")
    def password_must_meet_criteria(cls, password):
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one digit.')
        if not re.search(r'[@$!%*?&]', password):
            raise ValueError('Password must contain at least one special character: @$!%*?&')
        return password
