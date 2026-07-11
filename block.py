from time import time

class Block:
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

    def __repr__(self):
        return f"Block(index={self.index}, previous_hash={self.previous_hash}, timestamp={self.timestamp}, transactions={self.transactions}, proof={self.proof})"
    
