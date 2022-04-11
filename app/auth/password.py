from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    hashed_password = pwd_context.hash(password)


def make_hashed_password_with_salt(plain_password: str, salt):
    salted_password = f"{plain_password}_{salt}"
    hashed_password = hash_password(salted_password)
    return hashed_password


def hash_password_with_salt(password, salt):
    return hash_password(f"{password}_{salt}")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
