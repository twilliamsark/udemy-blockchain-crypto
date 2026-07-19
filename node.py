from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
wallet.load_keys()
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
            'private_key': wallet.private_key
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
            'private_key': wallet.private_key
        }), 200
    else:
        return jsonify({
            'message': 'Failed to load keys.'
        }), 500

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    return jsonify({
        'message': 'Balance fetched successfully.',
        'balance': balance
    }), 200

@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('ui', 'node.html')

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
    return jsonify({'chain': dict_chain}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
