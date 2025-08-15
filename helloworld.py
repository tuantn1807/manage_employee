# test_hash.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = ""
hashed = pwd_context.hash(password)
print("Hashed password:", hashed)