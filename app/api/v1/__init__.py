from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterStudentRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    mobile_number: str | None = None
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)
    college: str | None = None
    degree: str | None = None
    branch: str | None = None
    graduation_year: int | None = None
    location: str | None = None
    target_career_role: str | None = None

    model_config = ConfigDict(str_strip_whitespace=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class TokenUser(BaseModel):
    id: int
    full_name: str
    email: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: TokenUser


class UserSummary(BaseModel):
    id: int
    full_name: str
    email: str
    roles: list[str]
    is_active: bool = True
    is_verified: bool = False


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = None
    college: str | None = None
    degree: str | None = None
    branch: str | None = None
    location: str | None = None
    target_career_role: str | None = None


class DashboardMetrics(BaseModel):
    students: int
    companies: int
    internships: int
    jobs: int
    applications: int
