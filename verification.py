import hash_util as hu


class Verification:
    def validate_proof(self, transactions, previous_hash, proof, difficulty=2):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(previous_hash) + str(proof))
        guess_hash = hu.hash_string(guess)
        return guess_hash[0:difficulty] == "0" * difficulty


    def verify_transaction(self, transaction, get_balance):
        sender_balance = get_balance(transaction.sender)
        return sender_balance >= transaction.amount


    def verify_all_transactions(self, open_transactions, get_balance):
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions])


    def verify_chain(self, blockchain):
        for index, block in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hu.hash_block(blockchain[index - 1]):
                return False
            if not self.validate_proof(block.transactions[:-1], block.previous_hash, block.proof):
                return False
        return True
