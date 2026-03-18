import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, previousHash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previousHash = previousHash
        self.nonce = nonce
        self.hash = self.calculateHash()

    def calculateHash(self):
        blockString = json.dumps({
            "index": self.index,
            "txns": self.transactions,
            "prev": self.previousHash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(blockString).hexdigest()