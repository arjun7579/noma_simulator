# comm/encryption.py

from Crypto.Cipher import ChaCha20
from config import CHACHA20_KEY, CHACHA20_NONCE

class ChaCha20Encryptor:
    def __init__(self):
        self.key   = CHACHA20_KEY
        self.nonce = CHACHA20_NONCE

    def encrypt(self, plaintext: bytes) -> bytes:
        cipher = ChaCha20.new(key=self.key, nonce=self.nonce)
        return cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        cipher = ChaCha20.new(key=self.key, nonce=self.nonce)
        return cipher.decrypt(ciphertext)