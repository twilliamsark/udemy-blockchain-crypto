from utility.verification import Verification
from blockchain import Blockchain
from wallet import Wallet
from uuid import uuid4

class Node:
    def __init__(self):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_user_choice(self):
        return input("Your choice: ")


    def get_transaction_value(self):
        tx_recipient = input("Your transaction recipient please: ").capitalize()
        tx_amount = float(input("Your transaction amount please: "))
        return tx_recipient, tx_amount


    def print_verify_all_transactions(self):
        if (len(self.blockchain.get_open_transactions()) > 0):
            if Verification.verify_all_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                print("All open transactions are valid.")
            else:
                print("Some open transactions are invalid.")


    def print_blockchain_elements(self):
        if self.blockchain:
            for index, block in enumerate(self.blockchain.chain):
                print(f"Block {index}: {block}")


    def print_open_transactions(self):
        for index, transaction in enumerate(self.blockchain.get_open_transactions()):
            print(f"Transaction {index}: {transaction}")


    def print_balance(self):
        print(f"Your balance for ...{self.wallet.public_key[-10:] if self.wallet else None} is: {self.blockchain.get_balance()}")


    def listen_for_input(self):
        while True:
            print("\nplease choose")
            print("1. Add a new transaction")
            print("2. Mine a new block")
            print("3. Output the open transactions")
            print("4. Output the blockchain blocks")
            print("5. Create a new wallet")
            print("6. Load wallet")
            print("q. Quit")
            match self.get_user_choice():
                case "1":
                    if self.blockchain.add_transaction(self.wallet.public_key if self.wallet else None, *self.get_transaction_value()):
                        print("Transaction added successfully.")
                    self.print_open_transactions()
                    self.print_verify_all_transactions()
                    self.print_balance()
                case "2":
                    if self.blockchain and self.blockchain.mine_block():
                        self.print_blockchain_elements()
                        self.print_balance()
                        if not Verification.verify_chain(self.blockchain.chain):
                            print("The blockchain has been manipulated!")
                        else:
                            print("The blockchain is valid.")
                    else:
                        print("Mining failed. Make sure you have a wallet and sufficient balance.")
                case "3":
                    self.print_open_transactions()
                case "4":
                    self.print_blockchain_elements()
                    if not Verification.verify_chain(self.blockchain.chain):
                        print("The blockchain has been manipulated!")
                    else:
                        print("The blockchain is valid.")
                case "5":
                    self.wallet.create_keys()
                    self.blockchain = Blockchain(self.wallet.public_key)
                case "6":
                    pass
                case "q":
                    break
                case _:
                    print("Input was invalid, please pick a value from the list!")

        print('Done!')

# only run this if the file is executed directly, not imported
if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
        