import os, json
import pickle

import sys

size = 16
class BlockchainBuffer():
    def __init__(self, root_loc, company_loc, size=size):
        self.size = size
        self.blockLocation = os.path.join(root_loc, company_loc)
        self.nextOpen = 0
        self.buffer = [None]*16

    def __del__(self):
        for block in self.buffer:
            if block is not None:
                block.saveBlockchain(block.blockchain['company_id'])

    def addTransaction(self, company_id, transaction=None):
        print('addTransaction', file=sys.stderr)
        location = self.isCompanyInBuffer(company_id)
        if location != -1:
            self.buffer[location].addTransaction(transaction)
        else:
            self.addBlockchainToBuffer(company_id)
            addedLocation = self.nextOpen - 1
            if addedLocation < 0:
                 addedLocation = 15
            self.buffer[addedLocation].addTransaction(transaction)

    def isCompanyInBuffer(self, company_id):
        for i in range(0, self.size):
            if self.buffer[i] is not None and self.buffer[i].blockchain.company_id == company_id:
                return i
        return -1

    def addBlockchainToBuffer(self, company_id):
        blockchain = pickle.load(open(self.blockLocation + str(company_id) + '/blockchain.pkl', 'rb'))

        added = False
        while not added:
            nextBlock = self.buffer[self.nextOpen]
            if nextBlock is None:
                self.buffer[self.nextOpen] = BufferBlock(blockchain)
                added = True
            elif not nextBlock.isFresh():
                oldBlockchainLoc = self.blockLocation + str(nextBlock.blockchain.company_id) + '/blockchain.pkl'
                nextBlock.save(oldBlockchainLoc)
                self.buffer[self.nextOpen] = BufferBlock(blockchain)
                added = True
            else:
                nextBlok.setFresh(False)

            self.nextOpen += 1
            if self.nextOpen >= 16:
                self.nextOpne = 0

    def getListOfTransactions(self, company_id, prev_hash, current_transaction):
        location = self.isCompanyInBuffer(company_id)
        if location != -1:
            return self.buffer[location].getListOfTransactions(prev_hash, current_transaction)
        else:
            self.addBlockchainToBuffer(company_id)
            addedLocation = self.nextOpen - 1
            if addedLocation < 0:
                 addedLocation = 15
            return self.buffer[addedLocation].getListOfTransactions(prev_hash, current_transaction)

    def verify(self, company_id, prev_hash, current_transaction):
        location = self.isCompanyInBuffer(company_id)
        if location != -1:
            return self.buffer[location].verify(prev_hash, current_transaction)
        else:
            self.addBlockchainToBuffer(company_id)
            addedLocation = self.nextOpen - 1
            if addedLocation < 0:
                 addedLocation = 15
            return self.buffer[addedLocation].verify(prev_hash, current_transaction)

    def saveBlockchain(self, company_id):
        location = self.isCompanyInBuffer(company_id)
        if location != -1:
            self.buffer[location].save(self.blockLocation + str(company_id) + '/blockchain.pkl')


class BufferBlock():
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.fresh = True

    def addTransaction(self, transaction):
        self.blockchain.append_transaction(
            amount=transaction['amount'],
            to=transaction['to'],
            recipient=transaction['recipient']
        )
        self.setFresh(True)

    def getListOfTransactions(self, prev_hash, current_transaction):
        return self.blockchain.get_list_of_transactions(prev_hash, current_transaction)

    def verify(self, prev_hash, current_transaction):
        return self.blockchain.verify(prev_hash, current_transaction)

    def isFresh(self):
        return self.fresh

    def setFresh(self, fresh):
        self.fresh = fresh

    def save(self, path):
        print('save', file=sys.stderr)
        pickle.dump(self.blockchain, open(path, 'wb'))
