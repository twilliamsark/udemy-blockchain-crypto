from functools import reduce
import json

import hash_util as hu
from block import Block
from transaction import Transaction
from verification import Verification


MINING_REWARD = 10
GENESIS_BLOCK = {
    'previous_hash': None,
    'index': 0,
    'transactions': [],
    'proof': 100
}


class Blockchain:
    def __init__(self, hosting_node_id):
        self.open_transactions = []
        self.chain = [Block(
            GENESIS_BLOCK['index'],
            GENESIS_BLOCK['previous_hash'],
            GENESIS_BLOCK['transactions'],
            GENESIS_BLOCK['proof'],
            0
        )]
        self.hosting_node_id = hosting_node_id
        self.load_data()


    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0].strip())
                updated_blockchain = []
                for block in blockchain:
                    converted_txs = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_txs,
                        block['proof'],
                        block['timestamp']
                    )
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain

                open_transactions = json.loads(file_content[1].strip())
                updated_transactions = []
                for tx in open_transactions:
                    converted_tx = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    updated_transactions.append(converted_tx)
                self.open_transactions = updated_transactions

        except (IOError, IndexError):
            pass


    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                # dict_chain = []
                # for block_el in blockchain:
                #     dict_txs = []
                #     for tx in block_el.transactions:
                #         dict_txs.append(tx.__dict__)
                #     new_block = Block(
                #         block_el.index,
                #         block_el.previous_hash,
                #         dict_txs,
                #         block_el.proof,
                #         block_el.timestamp
                #     )
                #     dict_chain.append(new_block.__dict__)
                # f.write(json.dumps(dict_chain) + "\n")

                # Convert the blockchain into a list of dictionaries that can be
                # serialized into JSON. Each block is converted into a dictionary, 
                # and each transaction within the block is also converted into a 
                # dictionary. This ensures that the blockchain can be saved to a 
                # file in a JSON-compatible format.
                # 
                # Note: block_el is only ever read here. We create a new Block 
                # instance for each block in the blockchain to ensure that we have 
                # a proper dictionary representation for serialization, without 
                # modifying the original blockchain objects.
                saveable_chain = [block.__dict__ for block in [Block(
                    block_el.index,
                    block_el.previous_hash,
                    [tx.__dict__ for tx in block_el.transactions],
                    block_el.proof,
                    block_el.timestamp
                ) for block_el in self.chain]]   
                f.write(json.dumps(saveable_chain) + "\n")

                savable_transactions = [
                    transaction.__dict__ for transaction in self.open_transactions
                ]
                f.write(json.dumps(savable_transactions) + "\n")
        except IOError:
            print("Saving failed!")


    def proof_of_work(self):
        last_block = self.chain[-1]
        previous_hash = hu.hash_block(last_block)
        proof = 0
        while not Verification.validate_proof(self.open_transactions, previous_hash, proof):
            proof += 1
        return proof


    def get_balance(self):
        participant = self.hosting_node_id
        tx_sender = [
            [tx.amount for tx in block.transactions if tx.sender == participant] 
            for block in self.chain
        ]
        open_tx_sender = [
            tx.amount for tx in self.open_transactions if tx.sender == participant
        ]
        tx_sender.append(open_tx_sender)
        # using reduce instead of sum to show example reduce
        amount_sent = reduce(
            lambda tx_sum, tx_amt: tx_sum + tx_amt, 
            [txn for tx_list in tx_sender for txn in tx_list], 
            0
        )

        tx_recipient = [
            [tx.amount for tx in block.transactions if tx.recipient == participant] 
            for block in self.chain
        ]
        amount_received = sum([txn for tx_list in tx_recipient for txn in tx_list])

        return amount_received - amount_sent


    def add_transaction(self, sender, recipient, amount=1.0):
        transaction = Transaction(sender, recipient, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        else:
            print(f"Transaction from {sender} to {recipient} for {amount} is invalid due to insufficient balance.")
            return False


    def mine_block(self):
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.hosting_node_id, MINING_REWARD)
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)
        
        block = Block(
            previous_hash=hu.hash_block(self.chain[-1]),
            index=len(self.chain),
            transactions=copied_transactions,
            proof=proof
        )
        self.chain.append(block)

        self.open_transactions = []
        self.save_data()








