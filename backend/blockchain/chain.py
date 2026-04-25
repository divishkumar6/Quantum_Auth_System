import hashlib
import json
import time


class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "data": self.data,
                "prev_hash": self.prev_hash,
            },
            sort_keys=True,
        ).encode()
        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev_block = self.get_last_block()
        new_block = Block(len(self.chain), data, prev_block.hash)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for index in range(1, len(self.chain)):
            current = self.chain[index]
            previous = self.chain[index - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.prev_hash != previous.hash:
                return False

        return True
