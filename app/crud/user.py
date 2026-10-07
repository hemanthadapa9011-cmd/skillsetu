from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    mobile_number: str | None = None


class RegisterStudentRequest(UserBase):
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    college: str | None = None
    degree: str | None = None
    branch: str | None = None
    graduation_year: int | None = None
    location: str | None = None
    target_career_role: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    mobile_number: str | None = None
    is_active: bool
    is_verified: bool
