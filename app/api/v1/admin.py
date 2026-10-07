from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.crud.user import assign_role, create_student_profile, create_user, get_user_by_email, seed_default_roles
from app.database import Base, engine
from app.deps import get_current_user, get_db
from app.models.user import Role, User
from app.schemas.user import LoginRequest, RegisterStudentRequest, TokenResponse
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.on_event("startup")
def ensure_roles():
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    try:
        seed_default_roles(db)
    finally:
        db.close()


@router.post("/register", response_model=TokenResponse)
def register_student(payload: RegisterStudentRequest, db: Session = Depends(get_db)):
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if get_user_by_email(db, str(payload.email)):
        raise HTTPException(status_code=400, detail="User with this email already exists")

    user = create_user(
        db,
        full_name=payload.full_name,
        email=str(payload.email),
        password=payload.password,
        mobile_number=payload.mobile_number,
    )
    assign_role(db, user, "student")
    create_student_profile(
        db,
        user,
        college=payload.college,
        degree=payload.degree,
        branch=payload.branch,
        graduation_year=payload.graduation_year,
        location=payload.location,
        target_career_role=payload.target_career_role,
    )
    db.commit()

    access_token = create_access_token(subject=user.email, expires_delta=timedelta(days=7))
    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": "student",
        },
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, str(payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is inactive")

    access_token = create_access_token(subject=user.email, expires_delta=timedelta(days=7))
    role = user.roles[0].name if user.roles else "student"
    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": role,
        },
    )


@router.post("/admin/login", response_model=TokenResponse)
def admin_login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, str(payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    role_names = {role.name for role in user.roles}
    if not role_names.intersection({"super_admin", "operations_admin", "hr_admin", "content_admin", "support_admin"}):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    access_token = create_access_token(subject=user.email, expires_delta=timedelta(days=7))
    role = sorted(role_names)[0]
    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": role,
        },
    )


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "roles": [role.name for role in current_user.roles],
    }
