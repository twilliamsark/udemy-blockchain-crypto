from functools import reduce
import json
import hash_util as hu

MINING_REWARD = 10

owner='Todd'
participants = {owner}
print(f"Current participants: {participants}")
genesis_block = {
    'previous_hash': None,
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = [genesis_block]
open_transactions = []


def load_data():
    with open('blockchain.txt', mode='r') as f:
        file_content = f.readlines()
        global blockchain
        global open_transactions
        if len(file_content) < 2:
            blockchain = [genesis_block]
            open_transactions = []
        else:
            blockchain = json.loads(file_content[0].strip())
            open_transactions = json.loads(file_content[1].strip())


load_data()


def save_data():
    with open('blockchain.txt', mode='w') as f:
        f.write(json.dumps(blockchain) + "\n")
        f.write(json.dumps(open_transactions) + "\n")


def add_transaction(sender, recipient, amount=1.0):
    participants.add(sender)
    participants.add(recipient)
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    else:
        print(f"Transaction from {sender} to {recipient} for {amount} is invalid due to insufficient balance.")
        return False


def valid_proof(transactions, previous_hash, proof, difficulty=2):
    guess = (str(transactions) + str(previous_hash) + str(proof))
    guess_hash = hu.hash_string(guess)
    return guess_hash[0:difficulty] == "0" * difficulty


def proof_of_work():
    last_block = blockchain[-1]
    previous_hash = hu.hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, previous_hash, proof):
        proof += 1
    return proof


def mine_block():
    proof = proof_of_work()
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD,
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hu.hash_block(blockchain[-1]),
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    open_transactions.clear()
    save_data()


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def verify_all_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def print_verify_all_transactions():
    if (len(open_transactions) > 0):
        if verify_all_transactions():
            print("All open transactions are valid.")
        else:
            print("Some open transactions are invalid.")


def get_balances():
    [print(f"{participant}: {get_balance(participant)}") for participant in participants]


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    # using reduce instead of sum to show example reduce
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + tx_amt, [txn for tx_list in tx_sender for txn in tx_list], 0)

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = sum([txn for tx_list in tx_recipient for txn in tx_list])

    return amount_received - amount_sent


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
        if block['previous_hash'] != hu.hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            return False
    return True


while True:
    print("\nplease choose")
    print("1. Add a new transaction")
    print("2. Output the open transactions")
    print("3. Mine a new block")
    print("4. Output the blockchain blocks")
    print("5. Output participants")
    print("6. Manipulate the blockchain")
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
        case "6":
            if len(blockchain) >= 1:
                blockchain[0] = {
                    'previous_hash': None,
                    'index': 0,
                    'transactions': [{
                        'sender': 'Malicious User',
                        'recipient': 'Evil Hacker',
                        'amount': 1000.0
                    }]
                }
        case "q":
            break
        case _:
            print("Input was invalid, please pick a value from the list!")

print("Done!")
