from Crypto.PublicKey import RSA
import Crypto.Random
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import binascii
from utility.printable import Printable

class Wallet(Printable):
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def __repr__(self):
        return str({
            'public_key': '...' + self.public_key[-15:] if self.public_key else '<no public key>',
            'private_key': '...' if self.private_key else '<no private key>'
        })

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet.txt', 'w') as f:
                    f.write(f'{self.public_key}\n{self.private_key}')
                return True
            except (IOError, IndexError):
                print("Saving wallet failed...")
                return False
        else:
            return False

    def load_keys(self):
        try:
            with open('wallet.txt', 'r') as f:
                keys = f.read().splitlines()
                self.public_key = keys[0]
                self.private_key = keys[1]
            return True
        except (IOError, IndexError):
            print("Loading wallet failed...")
            return False

    def generate_keys(self):
        private_key = RSA.generate(2048, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (
            binascii.hexlify(private_key.export_key(format='DER')).decode('ascii'),
            binascii.hexlify(public_key.export_key(format='DER')).decode('ascii'),
        )

    def sign_transaction(self, sender, recipient, amount):
        if self.private_key == None:
            return None
        private_key = RSA.import_key(binascii.unhexlify(self.private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA256.new(f'{sender}{recipient}{amount}'.encode('utf-8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')
    
    @staticmethod
    def verify_transaction(transaction):
        public_key = RSA.import_key(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new(f'{transaction.sender}{transaction.recipient}{transaction.amount}'.encode('utf-8'))
        return verifier.verify(h, binascii.unhexlify(transaction.signature))