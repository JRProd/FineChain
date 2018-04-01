import sys
from datetime import datetime as time
import hashlib
import json
import urllib
import requests
from flask import Flask, jsonify, request

class Blockchain:
	def __init__(self, id, company_id):
		self.chain = []
		self.current_transactions = []
		self.append_block(prev_hash='1')
		self.nodes = set()
		self.id = None
		self.company_id = None
		self.created = time.now()

	def append_block(self, prev_hash):
		# Create new block and append to blockchain
		# param prev_hash: previous block's hash
		# return: the new block

		block = {
			'index': len(self.chain) + 1,
			'timestamp': str(time.now()),
			'transactions': self.current_transactions,
			'prev_hash': prev_hash
		}
		self.current_transactions = []
		self.chain.append(block)
		return block

	def append_transaction(self, amount, to, recipient):
		# Create new transaction and put into current block
		# param amount: amount of money being exchanged
		# param to: who money is being sent from
		# param from: who money is being sent to
		# return: the previous block's location incremented
		#print(self.prev_block()['prev_hash'])
		if len(self.current_transactions) == 100:
			self.append_block(self.hash(self.prev_block())) #setting a limit of 100 transactions per block

		transaction = {
			'amount': amount,
			'to': to,
			'recipient': recipient,
			'timestamp': str(time.now())

		}
		self.current_transactions.append(transaction)



		return self.prev_block()['index'] + 1

	def prev_block(self):
		# Return the previous block
		# return: previous block
		return self.chain[-1]

	def hash(self,block):
		# Create hash of block
		# param block: block in json format which is then hashed
		# return: a SHA256 hash of the block

		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	def register_node(self, address):
		# Add new node to list of nodes
		# param address: IP address of node to be added

		parsed_url = urlparse(address)
		self.nodes.add(parsed_url.netloc)

	def valid_chain(self, chain):
		# Determine if blockchain is valid
		# param chain: a blockchain
		# return: true if valid, false if not
		last_block = chain[0]
		currentindex = 1

		while currentindex < len(chain):
			block = chain[currentindex]
	                # Check that the hash of the block is correct
			if block['previous_hash'] != self.hash(last_block):
				return False
			last_block = block
			currentindex += 1
			return True

	def fix_collision(self):
		# If there's a multiple blockchains detected, take the longest one.
		# return: true if chain is replaced, false if chain is not

		network = self.nodes
		longest = len(self.chain)
		newchain = None
		for node in network:
                        pass
#			response = requests.get(f'http://{node}/chain') #change to https later?
#			if response.status_code == 200:
#				length = response.json()['length']
#				chain = response.json()['chain']
#				if length > longest and self.valid_chain(chain):
#					longest = length
#					newchain = chain
		if newchain:
			self.chain = newchain
			return True
		return False

	def print_chain(self):
		# Displays the chain
		for block in self.chain:
			print(block)
			print('\n')

	def set_id(self, num):
		self.id = num

	def get_id(self):
		return self.id
