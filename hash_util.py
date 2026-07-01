import hashlib as hl
import json


def hash_string(source):
    return hl.sha256(source.encode()).hexdigest()


def hash_block(block):
    block_string = json.dumps(block, sort_keys=True)
    return hash_string(block_string)
