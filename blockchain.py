from functools import reduce
import json


import hash_util as hu
from block import Block
from transaction import Transaction


MINING_REWARD = 10
GENESIS_BLOCK = {
    'previous_hash': None,
    'index': 0,
    'transactions': [],
    'proof': 100
}


owner='Todd'
participants = {owner}
print(f"Current participants: {participants}")
blockchain = []
open_transactions = []


def load_data():
    global blockchain
    global open_transactions
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
            blockchain = updated_blockchain

            open_transactions = json.loads(file_content[1].strip())
            updated_transactions = []
            for tx in open_transactions:
                converted_tx = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(converted_tx)
            open_transactions = updated_transactions

    except (IOError, IndexError):
        blockchain = [Block(
            GENESIS_BLOCK['index'],
            GENESIS_BLOCK['previous_hash'],
            GENESIS_BLOCK['transactions'],
            GENESIS_BLOCK['proof'],
            0
        )]
        open_transactions = []


load_data()


def save_data():
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
            ) for block_el in blockchain]]   
            f.write(json.dumps(saveable_chain) + "\n")

            savable_transactions = [transaction.__dict__ for transaction in open_transactions]
            f.write(json.dumps(savable_transactions) + "\n")
    except IOError:
        print("Saving failed!")


def valid_proof(transactions, previous_hash, proof, difficulty=2):
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(previous_hash) + str(proof))
    guess_hash = hu.hash_string(guess)
    return guess_hash[0:difficulty] == "0" * difficulty


def proof_of_work():
    last_block = blockchain[-1]
    previous_hash = hu.hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, previous_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    # using reduce instead of sum to show example reduce
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + tx_amt, [txn for tx_list in tx_sender for txn in tx_list], 0)

    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    amount_received = sum([txn for tx_list in tx_recipient for txn in tx_list])

    return amount_received - amount_sent


def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount


def add_transaction(sender, recipient, amount=1.0):
    transaction = Transaction(sender, recipient, amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    else:
        print(f"Transaction from {sender} to {recipient} for {amount} is invalid due to insufficient balance.")
        return False


def mine_block():
    proof = proof_of_work()
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    
    block = Block(
        previous_hash=hu.hash_block(blockchain[-1]),
        index=len(blockchain),
        transactions=copied_transactions,
        proof=proof
    )
    blockchain.append(block)

    open_transactions.clear()
    save_data()


def verify_all_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def print_verify_all_transactions():
    if (len(open_transactions) > 0):
        if verify_all_transactions():
            print("All open transactions are valid.")
        else:
            print("Some open transactions are invalid.")


def get_transaction_value():
    tx_recipient = input("Your transaction recipient please: ").capitalize()
    tx_amount = float(input("Your transaction amount please: "))
    return tx_recipient, tx_amount


def get_user_choice():
    return input("Your choice: ")


def print_blockchain_elements():
    for index, block in enumerate(blockchain):
        print(f"Block {index}: {block}")


def print_open_transactions():
    for index, transaction in enumerate(open_transactions):
        print(f"Transaction {index}: {transaction}")


def verify_chain():
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hu.hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            return False
    return True


def get_balances():
    [print(f"{participant}: {get_balance(participant)}") for participant in participants]


while True:
    print("\nplease choose")
    print("1. Add a new transaction")
    print("2. Output the open transactions")
    print("3. Mine a new block")
    print("4. Output the blockchain blocks")
    print("5. Output participants")
    print("q. Quit")

    match get_user_choice():
        case "1":
            if add_transaction(owner, *get_transaction_value()):
                print("Transaction added successfully.")
            print_open_transactions()
            print_verify_all_transactions()
        case "2":
            print_open_transactions()
            print_verify_all_transactions()
        case "3":
            mine_block()
            print_blockchain_elements()
            get_balances()
            if not verify_chain():
                print("The blockchain has been manipulated!")
            else:
                print("The blockchain is valid.")
        case "4":
            print_blockchain_elements()
            if not verify_chain():
                print("The blockchain has been manipulated!")
            else:
                print("The blockchain is valid.")
        case "5":
            print(f"Current participants: {participants}")
            get_balances()
        case "q":
            break
        case _:
            print("Input was invalid, please pick a value from the list!")

print("Done!")
