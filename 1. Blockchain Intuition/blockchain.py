# Module 1 - create a Blockchain

# import the libraries
from asyncio.windows_events import NULL
from cmath import nan
import datetime as dt
import hashlib as md
import http
import json as js
from http import HTTPStatus
from random import randint
import re
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain)+1,
            'timestamp': str(dt.datetime.now().isoformat()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof) -> int:
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = md.sha256(str(new_proof**4+previous_proof**2).encode()).hexdigest()
            if hash_operation.startswith("00000"):
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block) -> str:
        encoded_block = js.dumps(block, sort_keys=True).encode()
        return md.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain) -> bool:
        for i in range(1,len(chain)):
            block = chain[i]
            previous_block = chain[i-1]
            if block["previous_hash"] != self.hash(previous_block):
                return [i, False]
            hash_operation = md.sha256(str(block["proof"]**4+previous_block["proof"]**2).encode()).hexdigest()
            if not hash_operation.startswith("00000"):
                return [i, False]
        return [-1, True]

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain
blockchain = Blockchain()

# Mining a block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': "Congratulations!!! >_< You just ruined the blockchain",
        'index': block['index'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'timestamp': block['timestamp']
    }
    return jsonify(response), HTTPStatus.OK

# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'timestamp': str(dt.datetime.now().isoformat())
    }
    return jsonify(response), HTTPStatus.OK  if response['length'] > 1 else HTTPStatus.BAD_REQUEST


# Check if chain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid_chain():
    [ptr, isValid] = blockchain.is_chain_valid(blockchain.chain)
    response = {
        'is_valid': isValid if len(blockchain.chain)>1 else False,
        'length': len(blockchain.chain),
        'error_at_index': ptr+1 if not isValid else NULL,
        'timestamp': str(dt.datetime.now().isoformat())
    }
    return jsonify(response), HTTPStatus.OK  if response['length'] > 1 else HTTPStatus.BAD_REQUEST

# Disturb chain
@app.route('/disturb', methods=['GET'])
def disturb():
    previous_block = blockchain.get_previous_block()
    proof = previous_block["proof"]
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': "Congratulations, you just mined a block",
        'index': block['index'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'timestamp': block['timestamp']
    }
    return jsonify(response), HTTPStatus.OK

# Running the app
app.run(host = '0.0.0.0', port = 5000)
