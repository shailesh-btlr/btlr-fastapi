from app.config import settings
from app.internal.ejabberd import Ejabberd

ejabbert_client = Ejabberd(
    base_url=settings.EJABBERD_BASE_URL,
    user=settings.EJABBERD_ADMIN_USER,
    password=settings.EJABBERD_ADMIN_PASSWORD,
)


def to_chat_username(user_id):
    return f"{user_id}@{settings.EJABBERD_DOMAIN}"


def create_user_for_id(user_id):
    ejabbert_client.register(
        user=user_id, host=settings.EJABBERD_DOMAIN, password="btlrbtlr"
    )
    return to_chat_username(user_id)
