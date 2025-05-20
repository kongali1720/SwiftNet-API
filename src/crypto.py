# src/crypto.py
from Crypto.Cipher import AES
import base64
import hashlib

class AESCipher:
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw.encode())).decode()

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self._unpad(cipher.decrypt(enc).decode())

    def _pad(self, s):
        pad_len = self.bs - len(s) % self.bs
        return s + chr(pad_len) * pad_len

    def _unpad(self, s):
        return s[:-ord(s[-1])]

if __name__ == "__main__":
    aes = AESCipher("testkey")
    message = "Hello, MT103!"
    encrypted = aes.encrypt(message)
    decrypted = aes.decrypt(encrypted)

    print("Original :", message)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
