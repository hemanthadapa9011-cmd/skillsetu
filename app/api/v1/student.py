from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db, require_roles
from app.models.user import User

router = APIRouter(prefix="/api/v1/students", tags=["students"])


@router.get("/dashboard")
def student_dashboard(current_user: User = Depends(require_roles("student")), db: Session = Depends(get_db)):
    profile = current_user.student_profile
    return {
        "student": current_user.full_name,
        "email": current_user.email,
        "target_career_role": profile.target_career_role if profile else "Not set",
        "college": profile.college if profile else "Not set",
        "profile_completion": 35 if profile else 15,
        "career_readiness_score": 0,
        "skills": [],
        "projects": [],
        "internships": [],
        "jobs": [],
        "applications": [],
    }


@router.get("/profile")
def student_profile(current_user: User = Depends(require_roles("student"))):
    profile = current_user.student_profile
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "college": profile.college if profile else None,
        "degree": profile.degree if profile else None,
        "branch": profile.branch if profile else None,
        "target_career_role": profile.target_career_role if profile else None,
    }
