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
    return 'This works!'

@app.route('/mine', methods=['POST'])
def mine_block():
    return mine()
def mine():
    if blockchain.mine_block():
        return jsonify({'message': 'Block mined successfully.'}), 200
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
