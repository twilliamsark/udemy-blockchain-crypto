from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
# wallet.load_keys()
blockchain = Blockchain(wallet.public_key)
CORS(app)

@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        return jsonify({
            'message': 'Keys created successfully.',
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'balance': blockchain.get_balance()
        }), 201
    else:
        return jsonify({
            'message': 'Failed to create keys.',
            'wallet_set_up': wallet.public_key != None
        }), 500

@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        return jsonify({
            'message': 'Keys loaded successfully.',
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'balance': blockchain.get_balance()
        }), 200
    else:
        return jsonify({
            'message': 'Failed to load keys.'
        }), 500

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        return jsonify({
            'message': 'Balance fetched successfully.',
            'balance': balance
        }), 200
    else:
        return jsonify({
            'message': 'Failed to fetch balance.',
            'wallet_set_up': wallet.public_key != None
        }), 500

@app.route('/', methods=['GET'])
def get_ui():
    # return send_from_directory('ui', 'node_placeholder.html')
    return send_from_directory('ui', 'node.html')

@app.route('/network', methods=['GET'])
def get_node_network():
    return send_from_directory('ui', 'network.html')

@app.route('/mine', methods=['POST'])
def mine_block():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__.copy() for tx in dict_block['transactions']]
        return jsonify({
            'message': 'Block mined successfully.',
            'block':  dict_block,
            'balance': blockchain.get_balance()
        }), 201
    else:
        return jsonify({
            'message': 'Mining failed.',
            'wallet_set_up': wallet.public_key != None
        }), 500

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for block in dict_chain:
        block['transactions'] = [tx.__dict__.copy() for tx in block['transactions']]
    return jsonify(dict_chain), 200

# curl --json '{"recipient": "John Doe", "amount": 3}' http://localhost:5001/transaction
@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        return jsonify({'message': 'Wallet not set up.'}), 400
    values = request.get_json()
    if not values:
        return jsonify({'message': 'No input data provided.'}), 400
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        return jsonify({'message': 'Missing required transaction fields.'}), 400
    signature = wallet.sign_transaction(
        wallet.public_key,
        values['recipient'],
        values['amount']
    )
    if signature == None:
        return jsonify({'message': 'Failed to sign the transaction.'}, 500)
    success = blockchain.add_transaction(
        wallet.public_key,
        values['recipient'],
        values['amount'],
        signature
    )
    if success:
        return jsonify({
            'message': 'Transaction added successfully.',
            'balance': blockchain.get_balance()
        }), 201
    else:
        return jsonify({'message': 'Transaction failed.'}), 500

@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    open_transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__.copy() for tx in open_transactions]
    return jsonify(dict_transactions), 200

@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if 'node' in values:
        blockchain.add_peer_node(values['node'])
        return jsonify({
            'message': 'Node added.',
            'all_nodes': blockchain.get_peer_nodes()
            }), 201
    return jsonify({'message': 'No node provided.'}), 400

# /node/localhost:5002
@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        return jsonify({'message': 'No node provided.'}), 400
    else:
        blockchain.remove_peer_node(node_url)
        return jsonify({
            'message': 'Node removed.',
            'all_nodes': blockchain.get_peer_nodes()
            }), 201

@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify({'all_nodes': blockchain.get_peer_nodes()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
