from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, date
import sqlite3
import secrets
import hashlib
import re
from typing import Optional


app = FastAPI(title="User Account Management System")


DATABASE_NAME = "user_account_system.db"


# -----------------------------
# Database Setup
# -----------------------------

def get_database_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT NOT NULL UNIQUE,
            expires_at TEXT NOT NULL,
            used INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


@app.on_event("startup")
def startup_event():
    create_tables()


# -----------------------------
# Request Models
# -----------------------------

class RegisterRequest(BaseModel):
    full_name: str
    date_of_birth: date
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UpdateProfileRequest(BaseModel):
    full_name: str
    date_of_birth: date


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


# -----------------------------
# Helper Functions
# -----------------------------

def validate_full_name(full_name: str):
    if not full_name or len(full_name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Full name must contain at least 2 characters.")


def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must contain at least 8 characters.")

    if not re.search(r"[A-Za-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one letter.")

    if not re.search(r"[0-9]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number.")


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password: str, stored_password_hash: str) -> bool:
    salt, password_hash = stored_password_hash.split("$")

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()

    return new_hash == password_hash


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)


def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)


def get_current_user(authorization: Optional[str]):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token is required.")

    token = authorization.replace("Bearer ", "")

    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.id, users.full_name, users.date_of_birth, users.email
        FROM login_sessions
        JOIN users ON login_sessions.user_id = users.id
        WHERE login_sessions.session_token = ?
    """, (token,))

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    return user


# -----------------------------
# Authentication APIs
# -----------------------------

@app.post("/api/auth/register")
def register_user(request: RegisterRequest):
    validate_full_name(request.full_name)
    validate_password(request.password)

    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ?", (request.email,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists.")

    now = datetime.utcnow().isoformat()
    password_hash = hash_password(request.password)

    cursor.execute("""
        INSERT INTO users (
            full_name,
            date_of_birth,
            email,
            password_hash,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        request.full_name.strip(),
        request.date_of_birth.isoformat(),
        request.email,
        password_hash,
        now,
        now
    ))

    conn.commit()
    conn.close()

    return {
        "message": "User registered successfully."
    }


@app.post("/api/auth/login")
def login_user(request: LoginRequest):
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, email, password_hash
        FROM users
        WHERE email = ?
    """, (request.email,))

    user = cursor.fetchone()

    if not user:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    if not verify_password(request.password, user["password_hash"]):
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    session_token = generate_session_token()
    now = datetime.utcnow().isoformat()

    cursor.execute("""
        INSERT INTO login_sessions (
            user_id,
            session_token,
            created_at
        )
        VALUES (?, ?, ?)
    """, (
        user["id"],
        session_token,
        now
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Login successful.",
        "token": session_token
    }


@app.post("/api/auth/logout")
def logout_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token is required.")

    token = authorization.replace("Bearer ", "")

    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM login_sessions
        WHERE session_token = ?
    """, (token,))

    conn.commit()
    conn.close()

    return {
        "message": "Logout successful."
    }


# -----------------------------
# User Profile APIs
# -----------------------------

@app.get("/api/users/me")
def get_profile(authorization: Optional[str] = Header(None)):
    user = get_current_user(authorization)

    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "date_of_birth": user["date_of_birth"],
        "email": user["email"]
    }


@app.put("/api/users/me")
def update_profile(
    request: UpdateProfileRequest,
    authorization: Optional[str] = Header(None)
):
    user = get_current_user(authorization)
    validate_full_name(request.full_name)

    conn = get_database_connection()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()

    cursor.execute("""
        UPDATE users
        SET full_name = ?,
            date_of_birth = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        request.full_name.strip(),
        request.date_of_birth.isoformat(),
        now,
        user["id"]
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Profile updated successfully.",
        "full_name": request.full_name,
        "date_of_birth": request.date_of_birth
    }


# -----------------------------
# Forgot Password APIs
# -----------------------------

@app.post("/api/auth/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, email
        FROM users
        WHERE email = ?
    """, (request.email,))

    user = cursor.fetchone()

    # Security practice:
    # Always return a generic message even if the email does not exist.
    if not user:
        conn.close()
        return {
            "message": "If the email exists, a password reset link has been generated."
        }

    reset_token = generate_reset_token()
    expires_at = (datetime.utcnow() + timedelta(minutes=30)).isoformat()
    now = datetime.utcnow().isoformat()

    cursor.execute("""
        INSERT INTO password_reset_tokens (
            user_id,
            token,
            expires_at,
            used,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user["id"],
        reset_token,
        expires_at,
        0,
        now
    ))

    conn.commit()
    conn.close()

    # For assignment demonstration, the reset link is returned directly.
    # In a real system, this link should be sent by email.
    reset_link = f"http://localhost:5173/reset-password?token={reset_token}"

    return {
        "message": "Password reset link generated successfully.",
        "reset_link": reset_link
    }


@app.post("/api/auth/reset-password")
def reset_password(request: ResetPasswordRequest):
    validate_password(request.new_password)

    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_id, expires_at, used
        FROM password_reset_tokens
        WHERE token = ?
    """, (request.token,))

    reset_record = cursor.fetchone()

    if not reset_record:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid reset token.")

    if reset_record["used"] == 1:
        conn.close()
        raise HTTPException(status_code=400, detail="Reset token has already been used.")

    expires_at = datetime.fromisoformat(reset_record["expires_at"])

    if datetime.utcnow() > expires_at:
        conn.close()
        raise HTTPException(status_code=400, detail="Reset token has expired.")

    new_password_hash = hash_password(request.new_password)
    now = datetime.utcnow().isoformat()

    cursor.execute("""
        UPDATE users
        SET password_hash = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        new_password_hash,
        now,
        reset_record["user_id"]
    ))

    cursor.execute("""
        UPDATE password_reset_tokens
        SET used = 1
        WHERE id = ?
    """, (reset_record["id"],))

    conn.commit()
    conn.close()

    return {
        "message": "Password has been reset successfully."
    }


# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "User Account Management System API is running."
    }