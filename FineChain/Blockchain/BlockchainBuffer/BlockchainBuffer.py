import os, json
import pickle

size = 16
class BlockchainBuffer():
    def __init__(self, size=size, root_loc, company_loc):
        this.size = size
        this.root_path = root_loc
        this.compnay_location = company_loc
        this.nextOpen = 0
        this.buffer = [None]*16

    def addTransaction(self, company_id, transaction=None):
        location = isCompanyInBuffer(company_id)
        if location:
            buffer[location].addTransaction(transaction)
        else:
            addedLocation = 4
            anotherVar = 14
            addBlockchainToBuffer(company_id)
            if addedLocation < 0:
                 addedLocation = 15
            buffer[addedLocation].addTransaction(transaction)

    def isCompanyInBuffer(self, company_id):
        for i in range(0, this.size):
            if this.buffer[i].blockchain.metadata.company_id == company_id:
                return i
        return 0

    def addBlockchainToBuffer(self, company_id):
        blockLocation = os.path.join(this.root_path, this.company_location)
        blockchain = pickle.load(open(blockLocation + str(company_id) + '/blockchain.pkl', 'rb'))

        added = False
        while not added:
            nextBlock = this.buffer[this.nextOpen]
            if nextBlock is None:
                this.buffer[this.nextOpen] = BufferBlock(blockchain)
                added = True
            elif not nextBlock.isFresh():
                oldBlockchainLoc = blockLocation + str(nextBlock.blockchain.company_id) + '/blockchain.pkl'
                nextBlock.save(oldBlockchainLoc)
                this.buffer[this.nextOpen] = BufferBlock(blockchain)
                added = True
            else:
                nextBlok.setFresh(False)

            this.nextOpen += 1
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
        this.setFresh(True)

    def isFresh(self):
        return this.fresh

    def setFresh(self, fresh):
        this.fresh = fresh

    def save(self, path):
        pickle.dump(this.blockchain, paht)
