from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal, engine, Base
from app.models.user import Role, User
from app.security import get_password_hash

client = TestClient(app)


def setup_function():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    for name in [
        "student",
        "company",
        "college",
        "employee",
        "super_admin",
        "operations_admin",
        "hr_admin",
        "content_admin",
        "support_admin",
    ]:
        if not db.query(Role).filter(Role.name == name).first():
            db.add(Role(name=name, description=f"{name} role"))
    db.commit()
    db.close()


def test_student_register_and_login():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Asha Student",
            "email": "asha@example.com",
            "mobile_number": "9876543210",
            "password": "Password123",
            "confirm_password": "Password123",
            "college": "IIT Delhi",
            "degree": "B.Tech",
            "branch": "Computer Science",
            "graduation_year": 2025,
            "location": "Delhi",
            "target_career_role": "Python Backend Developer",
        },
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert "access_token" in body
    assert body["user"]["role"] == "student"

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "asha@example.com", "password": "Password123"},
    )
    assert login.status_code == 200, login.text
    assert login.json()["user"]["email"] == "asha@example.com"


def test_student_cannot_access_admin_api():
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Student User",
            "email": "student.user@example.com",
            "mobile_number": "9999999999",
            "password": "Password123",
            "confirm_password": "Password123",
            "college": "NIT Trichy",
            "degree": "B.E.",
            "branch": "Electronics",
            "graduation_year": 2024,
            "location": "Chennai",
            "target_career_role": "Frontend Developer",
        },
    )

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "student.user@example.com", "password": "Password123"},
    )
    access_token = login.json()["access_token"]

    response = client.get(
        "/api/v1/admin/dashboard",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 403, response.text


def test_admin_login():
    db = SessionLocal()
    admin_user = User(
        full_name="Super Admin",
        email="admin@skillsetu.com",
        mobile_number="1111111111",
        password_hash=get_password_hash("AdminPass123"),
        is_active=True,
        is_verified=True,
    )
    admin_role = db.query(Role).filter(Role.name == "super_admin").first()
    admin_user.roles.append(admin_role)
    db.add(admin_user)
    db.commit()
    db.close()

    response = client.post(
        "/api/v1/auth/admin/login",
        json={"email": "admin@skillsetu.com", "password": "AdminPass123"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["user"]["role"] == "super_admin"
