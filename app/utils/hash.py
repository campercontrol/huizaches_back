from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_str(string_hash: str):
    return pwd_context.hash(string_hash)


def verify_str_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
