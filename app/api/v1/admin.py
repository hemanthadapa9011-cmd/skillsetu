from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import Base, engine
from app.deps import get_db, require_roles
from app.models.user import User

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.on_event("startup")
def ensure_schema():
    Base.metadata.create_all(bind=engine)


@router.get("/dashboard")
def admin_dashboard(current_user: User = Depends(require_roles("super_admin", "operations_admin", "hr_admin", "content_admin", "support_admin"))):
    return {
        "message": "Admin dashboard",
        "admin": current_user.full_name,
        "roles": [role.name for role in current_user.roles],
        "metrics": {
            "students": 0,
            "companies": 0,
            "jobs": 0,
            "internships": 0,
            "applications": 0,
        },
    }


@router.get("/users")
def list_users(
    current_user: User = Depends(require_roles("super_admin", "operations_admin")),
    db: Session = Depends(get_db),
):
    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "roles": [role.name for role in user.roles],
            "is_active": user.is_active,
        }
        for user in db.query(User).all()
    ]
