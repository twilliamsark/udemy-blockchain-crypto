from utility.verification import Verification
from blockchain import Blockchain

from uuid import uuid4

class Node:
    def __init__(self):
        # self.hosting_node_id = str(uuid4())
        self.hosting_node_id = 'Todd' # TODO: until we create the Wallet
        self.blockchain = Blockchain(self.hosting_node_id)

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
        for index, block in enumerate(self.blockchain.chain):
            print(f"Block {index}: {block}")


    def print_open_transactions(self):
        for index, transaction in enumerate(self.blockchain.get_open_transactions()):
            print(f"Transaction {index}: {transaction}")


    def print_balance(self):
        print(f"Your balance for {self.hosting_node_id} is: {self.blockchain.get_balance()}")


    def listen_for_input(self):
        while True:
            print("\nplease choose")
            print("1. Add a new transaction")
            print("2. Mine a new block")
            print("3. Output the open transactions")
            print("4. Output the blockchain blocks")
            print("5. Output your balance")
            print("q. Quit")
            match self.get_user_choice():
                case "1":
                    if self.blockchain.add_transaction(self.hosting_node_id, *self.get_transaction_value()):
                        print("Transaction added successfully.")
                    self.print_open_transactions()
                    self.print_verify_all_transactions()
                    self.print_balance()
                case "2":
                    self.blockchain.mine_block()
                    self.print_blockchain_elements()
                    if not Verification.verify_chain(self.blockchain.chain):
                        print("The blockchain has been manipulated!")
                    else:
                        print("The blockchain is valid.")
                case "3":
                    self.print_open_transactions()
                case "4":
                    self.print_blockchain_elements()
                    if not Verification.verify_chain(self.blockchain.chain):
                        print("The blockchain has been manipulated!")
                    else:
                        print("The blockchain is valid.")
                case "5":
                    self.print_balance()
                case "q":
                    break
                case _:
                    print("Input was invalid, please pick a value from the list!")

        print('Done!')

node = Node()
node.listen_for_input()
        