from flask import Flask, jsonify
from flask_cors import CORS
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
wallet.load_keys()
blockchain = Blockchain(wallet.public_key)
CORS(app)

@app.route('/', methods=['GET'])
def get_ui():
    return jsonify({'message': 'Welcome to the blockchain node API.'}), 200

@app.route('/mine', methods=['POST'])
def mine_block():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__.copy() for tx in dict_block['transactions']]
        return jsonify({
            'message': 'Block mined successfully.',
            'block':  dict_block
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
