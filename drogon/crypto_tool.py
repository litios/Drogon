import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryptor:
    def __init__(self, master_passwd, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_passwd))
        self.tool = Fernet(key)

    def encrypt_passwd(self, passwd):
        return self.tool.encrypt(passwd.encode())

    def decrypt_passwd(self, passwd):
        return self.tool.decrypt(passwd.encode())
