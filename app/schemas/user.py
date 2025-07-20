from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    """Base schema for user, containing common fields."""
    email: EmailStr

class UserCreate(UserBase):
    """Schema for creating a new user, inherits from UserBase and adds password."""
    password: str

class UserResponse(UserBase):
    """Schema for returning user data, includes the user ID."""
    id: int

    model_config = ConfigDict(from_attributes=True)
