from sqlalchemy.orm import Session

from app.models.user import Role, StudentProfile, User
from app.security import get_password_hash


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, *, full_name: str, email: str, password: str, mobile_number: str | None = None) -> User:
    user = User(
        full_name=full_name,
        email=email,
        mobile_number=mobile_number,
        password_hash=get_password_hash(password),
        is_active=True,
        is_verified=False,
    )
    db.add(user)
    db.flush()
    return user


def assign_role(db: Session, user: User, role_name: str) -> None:
    role = db.query(Role).filter(Role.name == role_name).first()
    if role is None:
        role = Role(name=role_name, description=f"{role_name} role")
        db.add(role)
        db.flush()
    if user not in role.users:
        role.users.append(user)


def create_student_profile(db: Session, user: User, **kwargs) -> StudentProfile:
    profile = StudentProfile(user_id=user.id, **kwargs)
    db.add(profile)
    db.flush()
    return profile


def seed_default_roles(db: Session) -> None:
    names = [
        "student",
        "company",
        "college",
        "employee",
        "super_admin",
        "operations_admin",
        "hr_admin",
        "content_admin",
        "support_admin",
    ]
    for name in names:
        if not db.query(Role).filter(Role.name == name).first():
            db.add(Role(name=name, description=f"{name} role"))
    db.commit()
