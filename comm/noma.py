from config import NOMA_POWER_LEVELS
from comm.encryption import ChaCha20Encryptor
import numpy as np

class NOMAProtocol:
    def __init__(self, num_drones):
        self.enc = {i: ChaCha20Encryptor() for i in range(num_drones)}
        self.power = {i: NOMA_POWER_LEVELS[i] for i in range(num_drones)}
        self.buf = 1024

    def superpose(self, messages):
        total = np.zeros(self.buf)
        raw = {}
        for i, msg in messages.items():
            e = self.enc[i].encrypt(msg)
            raw[i] = e
            arr = np.frombuffer(e, dtype=np.uint8)
            arr = np.pad(arr, (0, self.buf - len(arr)))
            total += arr * self.power[i]
        return total, raw

    def decode(self, raw):
        decoded = {}
        for i in sorted(self.power, key=lambda x: -self.power[x]):
            decoded[i] = self.enc[i].decrypt(raw[i])
        return decoded
