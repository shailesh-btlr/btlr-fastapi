from pydantic_settings import BaseSettings


with open("btlr-policy.rego") as f:
    BLTR_POLICY = f.read()


class Settings(BaseSettings):
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./test_db.db"
    TEST_SQLALCHEMY_DATABASE_URI: str = "sqlite:///./pytest.db"
    ZAWS_ACCESS_KEY_ID: str
    ZAWS_SECRET_ACCESS_KEY: str
    ZAWS_S3_BUCKET_NAME: str
    ZAWS_REGION_NAME: str
    OPENAI_KEY: str
    OPA_URL: str = "http://localhost:8000/opa"
    JWT_ACCESS_EXPIRY_MINUTES: int = 15
    JWT_REFRESH_EXPIRY_MINUTES: int = 60 * 24 * 30
    TOKEN_URL: str = "auth"
    SCOPES: dict = {
        "me": "Read and write access to user's personal data.",
        "business": "Read and write access to user's business data.",
        "admin": "BTLR administrator access",
    }
    BLTR_POLICY: str = BLTR_POLICY
    ZEP_URL: str
    ZEP_API_KEY: str
    EJABBERD_DOMAIN: str = "chat.btlr.vip"
    EJABBERD_BASE_URL: str = "https://chat.btlr.vip"
    EJABBERD_ADMIN_USER: str = "admin@chat.btlr.vip"
    EJABBERD_ADMIN_PASSWORD: str
    OTP_EMAIL_FROM_ADDRESS: str
    OTP_EXPIRY_IN_MINUTES: int


settings = Settings()
