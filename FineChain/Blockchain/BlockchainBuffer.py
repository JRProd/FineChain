import os, json
import pickle

root_path = None
company_location = None

def initBuffer(root, company):
    root_path=root
    company_location=company
    this.buffer = BlockchainBuffer()

def addTransaction(company_id, transaction=None):
    this.buffer = addTransaction(company_id=company_id, transaction=transaction)


size = 16
class BlockchainBuffer():
    def __init__(size=size):
        this.size = size
        this.nextOpen = 0
        this.buffer = [None]*16

    def addTransaction(self, company_id, transaction=None):
        location = isCompanyInBuffer(company_id):
        if location:
            this.buffer[location].addTransaction(transaction)
        else:
            addBlockchainToBuffer(company_id)
            addTransaction(company_id, transaction)

    def isCompanyInBuffer(self, company_id):
        for i in range(0, this.size):
            if this.buffer[i].blockchain.metadata.company_id == company_id:
                return i
        return 0

    def addBlockchainToBuffer(self, company_id):
        blockLocation = os.path.join(root_path, company_location) + str(company_id) + '/blockchain.pkl'
        blockchain = pickle.load(open(blockLocation, 'rb'))

        added = False
        while not added:
            if this.buffer[this.nextOpen] is None:
                this.buffer[this.nextOpen] = BufferBlock(blockchain)
                added = True
            elif not this.buffer[this.nextOpen].fresh
                this.buffer[this.nextOpen].save()
                this.buffer[this.nextOpne] = BufferBlock(blockchain)
                added = True
            else:
                this.buffer[this.nextOpne].fresh = False

            this.nextOpen++
            if this.nextOpen >= 16:
                this.nextOpne = 0

class BufferBlock():
    def __init__(self, blockchain):
        this.blockchain = blockchain
        this.fresh = True

    def addTransaction(self, transaction):
        this.blockchain.append_transaction(
            amount=transaction['amount'],
            sender=transaction['sender'],
            recipient=transaction['recipient']
        )
        this.fresh = True

    def save():
        blockLocation = os.path.join(root_path, company_location) + str(this.blockchain.company_id) + '/blockchain.pkl'
        pickle.dump(this.blockchain, blockLocation)
