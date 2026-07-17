from collections import OrderedDict
from utility.printable import Printable


class Transaction(Printable):
    def __init__(self, sender, recipient, amount, signature):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature


    def to_ordered_dict(self):
        return OrderedDict([
            ('sender', self.sender),
            ('recipient', self.recipient),
            ('amount', self.amount),
            ('signature', self.signature)
        ])
    

    def __repr__(self):
        return str({
            'sender': '...' + self.sender[-15:] if self.sender != 'MINING' else 'MINING',
            'recipient': '...' + self.recipient[-15:],
            'amount': self.amount,
            'signature': '...' + self.signature[-15:] if self.signature else '<no signature>'
        })