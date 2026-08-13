import hashlib
import time
import json
import os

CHAIN_PATH = "blockchain/chain.json"

def load_chain():
    if not os.path.exists(CHAIN_PATH):
        return []

    try:
        with open(CHAIN_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_chain(chain):
    os.makedirs(os.path.dirname(CHAIN_PATH), exist_ok=True)
    with open(CHAIN_PATH, "w", encoding="utf-8") as f:
        json.dump(chain, f, indent=2)

blockchain = load_chain()

def get_previous_hash():
    if len(blockchain) == 0:
        return "0"
    return blockchain[-1]["hash"]

def compute_block_hash(block):
    block_copy = block.copy()
    block_copy.pop("hash", None)
    block_string = json.dumps(block_copy, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def create_block(file_id, previous_hash):
    block = {
        "index": len(blockchain) + 1,
        "timestamp": time.time(),
        "file_id": file_id,
        "previous_hash": previous_hash
    }

    block["hash"] = compute_block_hash(block)
    blockchain.append(block)
    save_chain(blockchain)
    return block

def is_chain_valid():
    for i, block in enumerate(blockchain):
        expected_hash = compute_block_hash(block)
        if block["hash"] != expected_hash:
            return False

        if i == 0:
            if block["previous_hash"] != "0":
                return False
        else:
            if block["previous_hash"] != blockchain[i - 1]["hash"]:
                return False

    return True

def verify_file_integrity(file_id):
    for block in blockchain:
        if block["file_id"] == file_id:
            return True
    return False