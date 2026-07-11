import hashlib as hl
import json


def hash_string(source):
    return hl.sha256(source.encode()).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    block_string = json.dumps(hashable_block, sort_keys=True)
    return hash_string(block_string)
