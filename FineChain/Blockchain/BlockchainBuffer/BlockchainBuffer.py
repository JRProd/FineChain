import os, json
import pickle

size = 16
class BlockchainBuffer():
    def __init__(self, root_loc, company_loc, size=size):
        self.size = size
        self.root_path = root_loc
        self.compnay_location = company_loc
        self.nextOpen = 0
        self.buffer = [None]*16

    def addTransaction(self, company_id, transaction=None):
        location = self.isCompanyInBuffer(company_id)
        if location:
            self.buffer[location].addTransaction(transaction)
        else:
            self.addBlockchainToBuffer(company_id)
            addedLocation = self.nextOpen - 1
            if addedLocation < 0:
                 addedLocation = 15
            self.buffer[addedLocation].addTransaction(transaction)

    def isCompanyInBuffer(self, company_id):
        for i in range(0, self.size):
            if self.buffer[i].blockchain.metadata.company_id == company_id:
                return i
        return 0

    def addBlockchainToBuffer(self, company_id):
        blockLocation = os.path.join(self.root_path, self.company_location)
        blockchain = pickle.load(open(blockLocation + str(company_id) + '/blockchain.pkl', 'rb'))

        added = False
        while not added:
            nextBlock = self.buffer[self.nextOpen]
            if nextBlock is None:
                self.buffer[self.nextOpen] = BufferBlock(blockchain)
                added = True
            elif not nextBlock.isFresh():
                oldBlockchainLoc = blockLocation + str(nextBlock.blockchain.company_id) + '/blockchain.pkl'
                nextBlock.save(oldBlockchainLoc)
                self.buffer[self.nextOpen] = BufferBlock(blockchain)
                added = True
            else:
                nextBlok.setFresh(False)

            self.nextOpen += 1
            if self.nextOpen >= 16:
                self.nextOpne = 0

    def saveBlockchain(self, company_id):
        location = self.isCompanyInBuffer(company_id)
        if location:
            self.buffer[location].save()


class BufferBlock():
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.fresh = True

    def addTransaction(self, transaction):
        self.blockchain.append_transaction(
            amount=transaction['amount'],
            sender=transaction['sender'],
            recipient=transaction['recipient']
        )
        self.setFresh(True)

    def isFresh(self):
        return self.fresh

    def setFresh(self, fresh):
        self.fresh = fresh

    def save(self, path):
        pickle.dump(self.blockchain, paht)
