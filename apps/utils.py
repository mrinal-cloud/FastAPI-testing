from passlib.hash import argon2

def hash(password: str):
    return argon2.hash(password)

def verify(plain, hashed):
    return argon2.verify(plain, hashed)