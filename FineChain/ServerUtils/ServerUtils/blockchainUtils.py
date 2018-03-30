import os, json

root_path = None
company_location = None

def initBuffer(root, company)
    root_path=root
    company_location=company

def addTransaction(company_id, transaction=None):
    pass


size = 16
class BlockchainBuffer():
    def __init__(size=size):
        this.size = size
        this.nextOpen = 0
        this.buffer = [None]*16

    def addTransaction(self, company_id, transaction=None):
        if isCompanyInBuffer(company_id):
        else:
            addBlockchainToBuffer(company_id)

    def isCompanyInBuffer(self, company_id):
        for i in range(0, this.size):
            if this.buffer[i].blockchain.metadata.company_id == company_id:
                return True
        return False

    def addBlockchainToBuffer(self, company_id):
        blockLocation = os.path.join(root_path, company_location) + str(company_id) + '/blockchain.json'
        blockchainJson = json.loads(blockLocation)
