from fastapi import Depends, HTTPException, Security, status
from jose import jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from fastapi.security.api_key import APIKeyHeader

# --- JWT settings ---
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

# --- Swagger UI: single input field for JWT ---
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)

# --- Dependency to get the current authenticated user ---
def get_current_user(
    token: str = Security(api_key_header),  # JWT comes from Authorization header
    db: Session = Depends(get_db)
):
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[len("Bearer "):].strip()

    # Decode JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Fetch user from database
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return user