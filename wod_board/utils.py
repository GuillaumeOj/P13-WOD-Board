from passlib.context import CryptContext

from wod_board import config


password_context = CryptContext(schemes=config.HASH_SCHEMES)


def hash_password(plain_password: str) -> CryptContext.hash:
    return password_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> CryptContext.verify:
    return password_context.verify(plain_password, hashed_password)
