"""User Account Management System API.

This module provides a simple FastAPI backend for user registration,
login, logout, profile management, forgot password, and password reset.

SQLite is used for demonstration purposes.
"""

import hashlib
import re
import secrets
import sqlite3
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, EmailStr


DATABASE_NAME = "user_account_system.db"
PASSWORD_HASH_ITERATIONS = 100_000
RESET_TOKEN_EXPIRY_MINUTES = 30


# -----------------------------
# Database Setup
# -----------------------------

def get_database_connection() -> sqlite3.Connection:
    """Create and return a SQLite database connection."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables() -> None:
    """Create required database tables if they do not already exist."""
    with get_database_connection() as connection:
        cursor = connection.cursor()

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

        connection.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Run application startup tasks."""
    create_tables()
    yield


app = FastAPI(
    title="User Account Management System",
    lifespan=lifespan,
)


# -----------------------------
# Request Models
# -----------------------------

class RegisterRequest(BaseModel):
    """Request body for user registration."""

    full_name: str
    date_of_birth: date
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str


class UpdateProfileRequest(BaseModel):
    """Request body for updating user profile."""

    full_name: str
    date_of_birth: date


class ForgotPasswordRequest(BaseModel):
    """Request body for forgot password."""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Request body for resetting password."""

    token: str
    new_password: str


# -----------------------------
# Helper Functions
# -----------------------------

def validate_full_name(full_name: str) -> None:
    """Validate the user's full name."""
    if not full_name or len(full_name.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Full name must contain at least 2 characters.",
        )


def validate_password(password: str) -> None:
    """Validate password complexity."""
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 8 characters.",
        )

    if not re.search(r"[A-Za-z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one letter.",
        )

    if not re.search(r"[0-9]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one number.",
        )


def hash_password(password: str) -> str:
    """Hash a password with a random salt."""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_HASH_ITERATIONS,
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password: str, stored_password_hash: str) -> bool:
    """Verify a plain password against the stored salted hash."""
    salt, password_hash = stored_password_hash.split("$")

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_HASH_ITERATIONS,
    ).hex()

    return secrets.compare_digest(new_hash, password_hash)


def generate_session_token() -> str:
    """Generate a secure session token."""
    return secrets.token_urlsafe(32)


def generate_reset_token() -> str:
    """Generate a secure password reset token."""
    return secrets.token_urlsafe(32)


def extract_bearer_token(authorization: Optional[str]) -> str:
    """Extract the token from the Authorization header."""
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization token is required.",
        )

    return authorization.replace("Bearer ", "")


def get_current_user(authorization: Optional[str]) -> sqlite3.Row:
    """Return the currently authenticated user."""
    token = extract_bearer_token(authorization)

    with get_database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT users.id, users.full_name, users.date_of_birth, users.email
            FROM login_sessions
            JOIN users ON login_sessions.user_id = users.id
            WHERE login_sessions.session_token = ?
        """, (token,))

        user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
        )

    return user


# -----------------------------
# Authentication APIs
# -----------------------------

@app.post("/api/auth/register")
def register_user(request: RegisterRequest) -> dict[str, str]:
    """Register a new user account."""
    validate_full_name(request.full_name)
    validate_password(request.password)

    with get_database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (request.email,),
        )
        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists.",
            )

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
            now,
        ))

        connection.commit()

    return {"message": "User registered successfully."}


@app.post("/api/auth/login")
def login_user(request: LoginRequest) -> dict[str, str]:
    """Log in a user and return a session token."""
    with get_database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, email, password_hash
            FROM users
            WHERE email = ?
        """, (request.email,))

        user = cursor.fetchone()

        if not user or not verify_password(request.password, user["password_hash"]):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

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
            now,
        ))

        connection.commit()

    return {
        "message": "Login successful.",
        "token": session_token,
    }


@app.post("/api/auth/logout")
def logout_user(authorization: Optional[str] = Header(None)) -> dict[str, str]:
    """Log out the current user."""
    token = extract_bearer_token(authorization)

    with get_database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM login_sessions WHERE session_token = ?",
            (token,),
        )
        connection.commit()

    return {"message": "Logout successful."}


# -----------------------------
# User Profile APIs
# -----------------------------

@app.get("/api/users/me")
def get_profile(authorization: Optional[str] = Header(None)) -> dict[str, object]:
    """Return the current user's profile."""
    user = get_current_user(authorization)

    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "date_of_birth": user["date_of_birth"],
        "email": user["email"],
    }


@app.put("/api/users/me")
def update_profile(
    request: UpdateProfileRequest,
    authorization: Optional[str] = Header(None),
) -> dict[str, str]:
    """Update the current user's profile."""
    user = get_current_user(authorization)
    validate_full_name(request.full_name)

    with get_database_connection() as connection:
        cursor = connection.cursor()
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
            user["id"],
        ))

        connection.commit()

    return {
        "message": "Profile updated successfully.",
        "full_name": request.full_name.strip(),
        "date_of_birth": request.date_of_birth.isoformat(),
    }


# -----------------------------
# Forgot Password APIs
# -----------------------------

@app.post("/api/auth/forgot-password")
def forgot_password(request: ForgotPasswordRequest) -> dict[str, str]:
    """Generate a password reset token for an existing email."""
    with get_database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, email
            FROM users
            WHERE email = ?
        """, (request.email,))

        user = cursor.fetchone()

        if not user:
            return {
                "message": "If the email exists, a password reset link has been generated."
            }

        reset_token = generate_reset_token()
        expires_at = (
            datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRY_MINUTES)
        ).isoformat()
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
            now,
        ))

        connection.commit()

    reset_link = f"http://localhost:5173/reset-password?token={reset_token}"

    return {
        "message": "Password reset link generated successfully.",
        "reset_link": reset_link,
    }


@app.post("/api/auth/reset-password")
def reset_password(request: ResetPasswordRequest) -> dict[str, str]:
    """Reset the user's password using a valid reset token."""
    validate_password(request.new_password)

    with get_database_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, user_id, expires_at, used
            FROM password_reset_tokens
            WHERE token = ?
        """, (request.token,))

        reset_record = cursor.fetchone()

        if not reset_record:
            raise HTTPException(
                status_code=400,
                detail="Invalid reset token.",
            )

        if reset_record["used"] == 1:
            raise HTTPException(
                status_code=400,
                detail="Reset token has already been used.",
            )

        expires_at = datetime.fromisoformat(reset_record["expires_at"])

        if datetime.utcnow() > expires_at:
            raise HTTPException(
                status_code=400,
                detail="Reset token has expired.",
            )

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
            reset_record["user_id"],
        ))

        cursor.execute(
            "UPDATE password_reset_tokens SET used = 1 WHERE id = ?",
            (reset_record["id"],),
        )

        connection.commit()

    return {"message": "Password has been reset successfully."}


# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def root() -> dict[str, str]:
    """Return API health check message."""
    return {"message": "User Account Management System API is running."}
    