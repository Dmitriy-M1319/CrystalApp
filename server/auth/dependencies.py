from passlib.context import CryptContext

from ..schemas.user_schemas import UserCreate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_user_password(user: UserCreate):
    # здесь сразу хешируем пароль у пользователя
    user.password = pwd_context.hash(user.password)
    return user


def verify_passwords(plain, hashed):
    return pwd_context.verify(plain, hashed)
