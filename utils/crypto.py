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
        return self.pwd_context.hash(secret)

    def verify(self, secret: str, hash: str) -> bool:
        return self.pwd_context.verify(secret, hash)