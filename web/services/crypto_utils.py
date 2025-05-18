from web.config import Config  # ou de onde está seu SECRET_KEY
from cryptography.fernet import Fernet


def get_fernet():
    return Fernet(
        Config.SECRET_KEY.encode()
        if isinstance(Config.SECRET_KEY, str)
        else Config.SECRET_KEY
    )


def encrypt_password(password: str) -> str:
    f = get_fernet()
    return f.encrypt(password.encode()).decode()


def decrypt_password(token: str) -> str:
    f = get_fernet()
    return f.decrypt(token.encode()).decode()
