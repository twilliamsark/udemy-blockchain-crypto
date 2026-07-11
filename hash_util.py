import hashlib as hl
import json


def hash_string(source):
    return hl.sha256(source.encode()).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    block_string = json.dumps(hashable_block, sort_keys=True)
    return hash_string(block_string)
