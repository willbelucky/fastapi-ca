from typing import cast
from passlib.context import CryptContext

class Crypto:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"], 
            deprecated="auto",
            pbkdf2_sha256__default_rounds=100000,
            pbkdf2_sha256__min_rounds=10000,
            pbkdf2_sha256__max_rounds=500000
        )

    def encrypt(self, secret: str) -> str:
        # passlib의 타입 스텁이 없어서 Any를 반환하므로 명시적 캐스팅
        return cast(str, self.pwd_context.hash(secret))

    def verify(self, secret: str, hash: str) -> bool:
        # passlib의 타입 스텁이 없어서 Any를 반환하므로 명시적 캐스팅
        return cast(bool, self.pwd_context.verify(secret, hash))