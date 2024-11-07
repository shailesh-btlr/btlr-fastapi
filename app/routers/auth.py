from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status, Request
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer,
    SecurityScopes,
)
from sqlalchemy.orm import Session
from app.config import settings

from app.database import get_db
from app.schemas.auth import TokenInfo
from app.schemas.users import User, UserBase
from app.schemas.opa import OpaInput

from app.services import auth, users
import time

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.TOKEN_URL,
    scopes=settings.SCOPES,
)


def raise_authentication_exception(required_scopes, detail):
    www_authenticate = (
        f"Bearer scope={required_scopes.scope_str}"
        if required_scopes.scopes
        else "Bearer"
    )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": www_authenticate},
    )


def authorized_user(
    req: Request,
    required_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> User:
    try:
        claims = auth.decode_access_token(token)
    except Exception as e:
        raise_authentication_exception(
            required_scopes, detail=f"JWT error: {e}"
        )
    if claims.exp < int(time.time()):
        raise_authentication_exception(
            required_scopes, detail="Token expired."
        )
    if not all(scope in claims.scopes for scope in required_scopes.scopes):
        raise_authentication_exception(
            required_scopes, detail="Not enough permissions (scope)."
        )
    user = users.get_user(db, user_id=claims.sub)
    if not user:
        raise_authentication_exception(
            required_scopes, detail="Could not validate credentials."
        )
    if not auth.opa_check(
        OpaInput(
            method=req.method, path=req.url.path.split("/")[1:], claims=claims
        )
    ):
        raise_authentication_exception(
            required_scopes, detail="Not enough permissions (policy)."
        )
    return user


@router.post("/request-otp")
def request_otp(user: UserBase, db: Session = Depends(get_db)):
    db_user = users.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    otp = auth.generate_and_email_otp(user.email)
    users.update_user_password(db, db_user.id, otp)


@router.post("")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> TokenInfo:
    user = auth.authenticate(
        db,
        form_data.username,  # oAuth requires the field to be called username
        form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenInfo(
        access_token=auth.create_access_token(user, form_data.scopes),
        refresh_token=auth.create_refresh_token(user, form_data.scopes),
        id_token=""
    )


@router.post("/refresh")
def refresh(
    token: Annotated[str, Form()], db: Session = Depends(get_db)
) -> TokenInfo:
    refresh_data = auth.decode_refresh_token(token)
    if refresh_data.exp < int(time.time()):
        raise_authentication_exception(
            refresh_data.scopes, detail="Refresh token expired."
        )
    user = users.get_user(db, user_id=refresh_data.sub)
    if not user:
        raise_authentication_exception(
            refresh_data.scopes, detail="Could not validate refresh data."
        )
    return TokenInfo(
        access_token=auth.create_access_token(user, refresh_data.scopes),
        refresh_token=auth.create_refresh_token(user, refresh_data.scopes),
        id_token=""
    )
