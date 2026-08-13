from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from app.auth import create_access_token, hash_password, verify_password
from app.config import settings
from app.database import get_supabase_admin
from app.schemas import TokenResponse, UserLogin, UserResponse, UserSignup

router = APIRouter()


@router.post("/signup", response_model=TokenResponse)
async def signup(payload: UserSignup):
    supabase = get_supabase_admin()

    existing = supabase.table("users").select("id").eq("email", payload.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="User already exists")

    user_payload = {
        "email": payload.email,
        "name": payload.name,
        "password_hash": hash_password(payload.password),
        "role": payload.role,
    }

    response = supabase.table("users").insert(user_payload).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Could not create user")

    user = response.data[0]
    token = create_access_token(
        {"sub": str(user["id"]), "email": user["email"]},
        expires_delta=timedelta(hours=settings.jwt_expiration_hours),
    )

    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=str(user["id"]),
            email=user["email"],
            name=user.get("name", ""),
            role=user.get("role", "store_manager"),
            created_at=user.get("created_at"),
        ),
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin):
    supabase = get_supabase_admin()

    result = supabase.table("users").select("*").eq("email", payload.email).limit(1).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = result.data[0]
    stored_hash = user.get("password_hash")
    if not stored_hash or not verify_password(payload.password, stored_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"sub": str(user["id"]), "email": user["email"]},
        expires_delta=timedelta(hours=settings.jwt_expiration_hours),
    )

    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=str(user["id"]),
            email=user["email"],
            name=user.get("name", ""),
            role=user.get("role", "store_manager"),
            created_at=user.get("created_at"),
        ),
    )
