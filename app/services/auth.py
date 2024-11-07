import time
import uuid

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import settings
from app.internal import security
from app.schemas.auth import Claims, Refresh
from app.schemas.opa import OpaInput
from app.schemas.users import User
from app.services import opa, otp, users, aws_email
from app import models


def authenticate(db: Session, email: str, password: str) -> User:
    user = users.get_user_by_email(db, email)
    if user:
        if has_otp_not_expired(db, user):
            if security.verify_password(password, user.password):
                return user


def create_access_token(user: User, scopes: list[str]):
    exp = int(time.time() + settings.JWT_ACCESS_EXPIRY_MINUTES * 60)
    print("FIXME: DO SOME SCOPE STUFF")
    return security.create_token(
        Claims(
            sub=str(user.id), email=user.email, exp=exp, scopes=scopes
        ).model_dump()
    )


def create_refresh_token(user: User, scopes: list[str]):
    exp = int(time.time() + settings.JWT_REFRESH_EXPIRY_MINUTES * 60)
    return security.create_token(
        Refresh(
            sub=str(user.id), exp=exp, scopes=scopes, uuid=str(uuid.uuid4())
        ).model_dump()
    )


def decode_access_token(token: str) -> Claims:
    return Claims(**security.decode_token(token))


def decode_refresh_token(token: str) -> Refresh:
    return Refresh(**security.decode_token(token))


def opa_check(input: OpaInput):
    return opa.query(input).get("allow")
    # return httpx.post(
    #     settings.OPA_URL, json=input.model_dump()
    # ).json()


def generate_and_email_otp(email):
    generated_otp = otp.generate_otp()
    aws_email.send_otp_email(generated_otp, email)
    return generated_otp


def has_otp_not_expired(db, user):
    time_in_seconds = db.query(func.EXTRACT('epoch', func.now() - user.otp_valid_from)) \
                .filter(models.User.id == user.id) \
                .scalar()
    time_in_minutes = time_in_seconds / 60
    if time_in_minutes < settings.OTP_EXPIRY_IN_MINUTES:
        return True
