import hashlib

from zep_python.memory import Session
from zep_python.user import CreateUserRequest
from zep_python.zep_client import ZepClient

from app.config import settings

client = ZepClient(settings.ZEP_URL, settings.ZEP_API_KEY)


def to_zep_username(username):
    """
    ZEP collections and sessions names are constrained. In particular
    collection names must be strictly aplhanumeric and max 40 chars long.

    Since we want to use the same name across user, session and collection
    the username is sha256-hashed and truncated.
    """
    return hashlib.sha256(username.encode()).hexdigest()[:40]


def to_zep_business_name(business_id: int):
    return f"business{business_id}"


def create_user_with_session_and_add_collection(username: str):
    hashed_name = to_zep_username(username)
    client.user.add(
        CreateUserRequest(
            user_id=hashed_name,
            email=username,
            metadata=dict(username=username),
        )
    )
    client.memory.add_session(
        Session(
            session_id=hashed_name,
            user_id=hashed_name,
            metadata=dict(username=username),
        )
    )
    client.document.add_collection(
        name=hashed_name,
        description=username,
        embedding_dimensions=1536,
        is_auto_embedded=False,
    )


def create_business_collection(business_id: int):
    client.document.add_collection(
        name=to_zep_business_name(business_id),
        description=f"BTLR Business {business_id}",
        embedding_dimensions=1536,
        is_auto_embedded=False,
    )
