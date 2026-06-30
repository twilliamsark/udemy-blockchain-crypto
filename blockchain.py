import functools

MINING_REWARD = 10

owner='Todd'
participants = {owner}
print(f"Current participants: {participants}")
genesis_block = {
    'previous_hash': None,
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []

def get_last_blockchain_value():
    if len(blockchain) == 0:
        return None
    return blockchain[-1]


def add_transaction(sender, recipient, amount=1.0):
    participants.add(sender)
    participants.add(recipient)
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        return True
    else:
        print(f"Transaction from {sender} to {recipient} for {amount} is invalid due to insufficient balance.")
        return False


def mine_block():
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': calculate_hash(blockchain[-1]),
        'index': len(blockchain),
        'transactions': copied_transactions
    }
    blockchain.append(block)
    open_transactions.clear()


def calculate_hash(block):
    return "-".join([str(block[key]) for key in block])


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
    print(f"Transactions sent by {participant}: {tx_sender}")
    # amount_sent = 0
    # for tx_list in tx_sender:
    #     for txn in tx_list:
    #         amount_sent += txn
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + tx_amt, [txn for tx_list in tx_sender for txn in tx_list], 0)

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    # amount_received = 0
    # for tx_list in tx_recipient:
    #     for txn in tx_list:
    #         amount_received += txn
    amount_received = sum([txn for tx_list in tx_recipient for txn in tx_list])

    print(f" Balance for {participant} -> Amount sent: {amount_sent:.2f}, Amount received: {amount_received:.2f}")
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
        elif block['previous_hash'] != calculate_hash(blockchain[index - 1]):
            return False
    return True


while True:
    print("\nplease choose")
    print("1. Add a new transaction value")
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
            # print(f"Balance of {owner}: {get_balance(owner)}")
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
