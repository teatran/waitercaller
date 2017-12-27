import os
import base64
import hashlib


class PasswordHelper:

    def get_hash(self, plain):
        return hashlib.sha512(plain).hexdigest()

    def get_random_salt(self):
        return base64.b64encode(os.urandom(20))

    def validate_password(self, plain, salt, cipher):
        return self.get_hash(plain+salt) == cipher

    
    
