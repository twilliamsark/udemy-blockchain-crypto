from time import time
from printable import Printable


class Block(Printable):
    def __init__(self, 
                 index, 
                 previous_hash, 
                 transactions, 
                 proof, 
                 timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time()
        self.transactions = transactions
        self.proof = proof
        