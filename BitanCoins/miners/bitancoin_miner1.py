# import the libraries
import cryptocode as crypto
import datetime as dt
import hashlib as md
import json as js
from flask import Flask, jsonify, request
import requests as rq
from uuid import uuid4
from urllib.parse import urlparse

# Part 1 - Building a Blockchain for Bitancoin

class Blockchain:
    def __init__(self):
        self.limit = 10
        self.secret_key = str(md.sha256("I am a secret key".encode()).hexdigest())
        self.bitancoin_system_id = str(md.sha256("Bitan Sarkar".encode()).hexdigest())
        self.prefix_zeros_increment_block_limit = 100
        self.current_target = '000'
        self.chain = []
        self.utxos = []
        self.transactions = []
        self.nodes = set()
        self.create_block(previous_hash = '0', id = str(md.sha256("Bitan Sarkar".encode()).hexdigest()))
    
    def create_block(self, previous_hash, id):
        self.transactions.sort(key=lambda transaction: transaction['fees'], reverse=True)
        check_proof = True
        ctr = 1
        sum_total = 0
        block = {}
        while check_proof:
            sum_total = sum([float(0 if transaction['fees'] is None else transaction['fees']) for transaction in self.transactions[0:self.limit]])
            block = {
                'index': len(self.chain)+1,
                'timestamp': str(dt.datetime.now().isoformat()),
                'nonce': ctr,
                'transactions': self.transactions[0:self.limit],
                'previous_hash': previous_hash
            }
            if block['index'] > self.prefix_zeros_increment_block_limit:
                self.prefix_zeros_increment_block_limit = 2*self.prefix_zeros_increment_block_limit
                self.current_target = self.current_target + '0'
            if self.hash(block).startswith(self.current_target):
                check_proof = False
                self.chain.append(block)
            ctr += 1
        self.transactions = self.transactions[self.limit:]
        self.add_transaction(sender=self.bitancoin_system_id, amount=sum_total*1.05+0.1, reciever=id, fees=sum_total*0.05+0.05)
        self.replace_chain_decentralized(id)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def hash(self, block) -> str:
        encoded_block = js.dumps(block, sort_keys=True).encode()
        return md.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        for i in range(1,len(chain)):
            block = chain[i]
            previous_block = chain[i-1]
            if block["previous_hash"] != self.hash(previous_block):
                return [i, False]
        return [-1, True]
    
    def add_transaction(self, sender, reciever, amount, fees = 0.0):
        if fees is None:
            fees = 0
        if amount < 0 or fees < 0:
            return False
        if sender != self.bitancoin_system_id and self.get_wallet_balance(sender) < amount + fees:
            return False
        utxo = {
            'id': '',
            'sender' : sender,
            'amount': amount,
            'reciever': reciever,
            'fees': fees,
            'timestamp': str(dt.datetime.now().isoformat())
        }
        utxo['id'] = self.hash(utxo)
        self.utxos.append(utxo)
        self.transactions.append(utxo)
        self.replace_transactions_decentralized(reciever if sender == self.bitancoin_system_id else sender)
        self.replace_utxos_decentralized(reciever if sender == self.bitancoin_system_id else sender)
        return True
    
    def add_node(self, address, node_address, neighbour_node_id):
        parsed_url = urlparse(address)
        node_string = js.dumps({
            'node_id': node_address,
            'node_address': parsed_url.netloc
            })
        if neighbour_node_id != None:
            neighbour_node_string = js.dumps({
                'node_id': neighbour_node_id,
                'node_address': crypto.decrypt(neighbour_node_id, self.secret_key)
            })
            self.nodes.add(neighbour_node_string)
        if node_string in self.nodes:
            return False
        self.nodes.add(node_string)
        self.update_nodes_decentralized(parsed_url.netloc)
        return True

    def get_wallet_balance(self, node_address):
        sum_amount = 0
        for transaction in self.utxos:
            if transaction['sender'] == node_address:
                sum_amount -= transaction['amount']
            if transaction['reciever'] == node_address:
                sum_amount += transaction['amount']
        return sum_amount
    
    def update_nodes(self, nodes):
        self.nodes = nodes

    def update_nodes_decentralized(self, self_node_address):
        network = self.nodes
        node_set = set()
        for node in network:
            node_address = js.loads(node)['node_address']
            if node_address != self_node_address:
                response = rq.get(f'http://{node_address}/get_all_nodes', headers={'Authorization': self.secret_key, 'Content-Type': 'application/json', 'Accept': 'application/json'})
                if response.status_code == 200:
                    nodes = response.json()
                    node_set.update(list(nodes))
        self.nodes.update(node_set)
        for node in network:
            node_address = js.loads(node)['node_address']
            if node_address != self_node_address:
                rq.post(f'http://{node_address}/update_all_nodes', json=list(self.nodes), headers={'Authorization': self.secret_key, 'Content-Type': 'application/json', 'Accept': 'application/json'})

    def replace_chain_decentralized(self, id):
        network = self.nodes
        longest_chain = self.chain
        max_length = len(self.chain)
        changed = False
        for node in network:
            node_address = js.loads(node)['node_address']
            if id != js.loads(node)['node_id']:
                response = rq.get(f'http://{node_address}/get_chain')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']
                    if length >= max_length and self.is_chain_valid(chain)[1]:
                        max_length = length
                        longest_chain = chain
                        changed = True
        if changed:
            longest_chain_transaction = set()
            self_chain_transaction = set()
            for index in range(0, max_length):
                if self.hash(self.chain[index]) != self.hash(longest_chain[index]):
                    longest_chain_transaction.update([js.dumps(transaction) for transaction in longest_chain[index]['transactions']])
                    self_chain_transaction.update([js.dumps(transaction) for transaction in self.chain[index]['transactions']])
            orphan_transaction = [js.loads(transaction) for transaction in list(self_chain_transaction-longest_chain_transaction)]
            self.transactions.extend(orphan_transaction)
            self.replace_transactions_decentralized(id)
            self.chain = longest_chain
        for node in network:
            node_address = js.loads(node)['node_address']
            if id != js.loads(node)['node_id']:
                response = rq.post(f'http://{node_address}/update_chain', json=self.chain, headers={'Authorization': self.secret_key, 'Content-Type': 'application/json', 'Accept': 'application/json'})
                if response.status_code == 200:
                    return True
        return False
    
    def replace_transactions_decentralized(self, sender):
        network = self.nodes
        for node in network:
            node_address = js.loads(node)['node_address']
            node_id = js.loads(node)['node_id']
            if node_id != sender:
                rq.post(f'http://{node_address}/update_transactions', json=self.transactions, headers={'Authorization': self.secret_key, 'Content-Type': 'application/json', 'Accept': 'application/json'})
    
    def replace_utxos_decentralized(self, sender):
        network = self.nodes
        transaction_set = set([] if self.utxos is None else [js.dumps(transaction) for transaction in self.utxos])
        for node in network:
            node_address = js.loads(node)['node_address']
            node_id = js.loads(node)['node_id']
            if node_id != sender:
                response = rq.get(f'http://{node_address}/get_utxos', headers={'Authorization': self.secret_key, 'Content-Type': 'application/json', 'Accept': 'application/json'})
                if response.status_code == 200:
                    transactions = response.json()
                    transaction_set.update([js.dumps(transaction) for transaction in transactions])
        self.utxos.extend([js.loads(transaction) for transaction in list(transaction_set)])
        for node in network:
            node_address = js.loads(node)['node_address']
            node_id = js.loads(node)['node_id']
            if node_id != sender:
                response = rq.post(f'http://{node_address}/update_all_utxos', json=self.utxos, headers={'Authorization': self.secret_key, 'Content-Type': 'application/json', 'Accept': 'application/json'})

    def replace_chain(self, chain):
        self.chain = chain

    def replace_transactions(self, transactions):
        self.transactions = transactions

    def replace_utxos(self, transactions):
        self.utxos = transactions

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain
blockchain = Blockchain()
node_address = None

def isValidNode(address):
    parsed_url = urlparse(address)
    return parsed_url.netloc in set([js.loads(node)['node_address'] for node in blockchain.nodes])

# Mining a block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    if not isValidNode(request.host_url):  # type: ignore
        return "Invalid host", 401
    global node_address
    if node_address is None:
        node_address = crypto.encrypt(urlparse(request.host_url).netloc, blockchain.secret_key)  # type: ignore
    previous_block = blockchain.get_previous_block()
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(previous_hash, node_address)
    response = {
        'message': "Congratulations, you just mined a block",
        'index': block['index'],
        'nonce': block['nonce'],
        'transactions': block['transactions'],
        'hash': blockchain.hash(block),
        'timestamp': block['timestamp']
    }
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    if not isValidNode(request.host_url):  # type: ignore
        return "Invalid host", 401
    global node_address
    if node_address is None:
        node_address = crypto.encrypt(urlparse(request.host_url).netloc, blockchain.secret_key)  # type: ignore
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'timestamp': str(dt.datetime.now().isoformat())
    }
    return jsonify(response), 200

# Getting the all UTXOs
@app.route('/get_all_utxos', methods=['GET'])
def get_all_utxos():
    if not isValidNode(request.host_url):  # type: ignore
        return "Invalid host", 401
    global node_address
    if node_address is None:
        node_address = crypto.encrypt(urlparse(request.host_url).netloc, blockchain.secret_key)  # type: ignore
    response = {
        'transactions': blockchain.transactions,
        'length': len(blockchain.transactions),
        'timestamp': str(dt.datetime.now().isoformat())
    }
    return jsonify(response), 200

# Update chain
@app.route('/update_chain', methods=['POST'])
def update_chain():
    json = request.get_json(force=True, silent=True, cache=False)  # type: ignore
    auth = request.headers['Authorization']  # type: ignore
    if auth is None and auth is not blockchain.secret_key:
        return jsonify({'message': 'sho sho'}), 401
    blockchain.replace_chain(json)
    return jsonify({'message':'success'}) , 200

# Update transactions
@app.route('/update_transactions', methods=['POST'])
def update_transactions():
    json = request.get_json(force=True, silent=True, cache=False)  # type: ignore
    auth = request.headers['Authorization']  # type: ignore
    if auth is None and auth is not blockchain.secret_key:
        return jsonify({'message': 'sho sho'}), 401
    blockchain.replace_transactions(json)
    return jsonify({'message':'success'}) , 200

# Add transaction to block chain
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if not isValidNode(request.host_url):  # type: ignore
        return "Invalid host", 401
    global node_address
    if node_address is None:
        node_address = crypto.encrypt(urlparse(request.host_url).netloc, blockchain.secret_key)  # type: ignore
    json = request.get_json(force=True, silent=True, cache=False)  # type: ignore
    transaction_keys = ['reciever', 'amount']
    if not all (key in json for key in transaction_keys):
        return 'Some elements of transation are missing', 400
    success_response = {
        'timestamp': str(dt.datetime.now().isoformat()),
        'message' : 'Transaction successfully added'
    }
    failure_response = {
        'timestamp': str(dt.datetime.now().isoformat()),
        'message' : 'Bad Amount added'
    }
    if blockchain.add_transaction(sender=node_address, reciever=json['reciever'], amount=json['amount'], fees=json['fees']):
        return jsonify(success_response), 201 
    else:
        return jsonify(failure_response), 400

# Part 3 - De centralizing the blockchain

# Connecting new nodes
@app.route('/connect_node', methods=['POST'])
def connect_node():
    global node_address
    if node_address is None:
        node_address = crypto.encrypt(urlparse(request.host_url).netloc, blockchain.secret_key)  # type: ignore
    try:
        response = request.get_json(force=True, silent=True, cache=False)['neighbour_node']  # type: ignore
    except KeyError as e:
        response = None
    res = '' if blockchain.add_node(request.host_url, node_address, response) else 'already '  # type: ignore
    return jsonify({
        'message': f'Your node is {res}connected',
        'your_public_id': node_address
    }), 201

# Get all node ids (similar to public keys)
@app.route('/get_nodes', methods=['GET'])
def get_nodes():
    global node_address
    if node_address is None:
        node_address = crypto.encrypt(urlparse(request.host_url).netloc, blockchain.secret_key)  # type: ignore
    return jsonify([js.loads(node)['node_id'] for node in list(blockchain.nodes)]), 200

# Get all nodes
@app.route('/get_all_nodes', methods=['GET'])
def get_all_nodes():
    auth = request.headers['Authorization']  # type: ignore
    if auth is None and auth is not blockchain.secret_key:
        return jsonify({'message': 'sho sho'}), 401
    return jsonify(list(blockchain.nodes)), 200

# Update all nodes
@app.route('/update_all_nodes', methods=['POST'])
def update_all_nodes():
    auth = request.headers['Authorization']  # type: ignore
    if auth is None and auth is not blockchain.secret_key:
        return jsonify({'message': 'sho sho'}), 401
    blockchain.update_nodes(request.get_json(force=True, silent=True, cache=False))  # type: ignore
    return jsonify({"message":"Success"}), 200

# Get all utxos
@app.route('/get_utxos', methods=['GET'])
def get_utxos():
    auth = request.headers['Authorization']  # type: ignore
    if auth is None and auth is not blockchain.secret_key:
        return jsonify({'message': 'sho sho'}), 401
    return jsonify([] if blockchain.utxos is None else blockchain.utxos), 200

# Update all utxos
@app.route('/update_all_utxos', methods=['POST'])
def update_all_utxos():
    auth = request.headers['Authorization']  # type: ignore
    if auth is None and auth is not blockchain.secret_key:
        return jsonify({'message': 'sho sho'}), 401
    blockchain.replace_utxos(request.get_json(force=True, silent=True, cache=False))  # type: ignore
    return 'Success', 200

# Get Balance in wallet
@app.route('/get_wallet', methods=['GET'])
def get_wallet():
    if not isValidNode(request.host_url):  # type: ignore
        return "Invalid host", 401
    global node_address
    if node_address is None:
        node_address = crypto.encrypt(urlparse(request.host_url).netloc, blockchain.secret_key)  # type: ignore
    return jsonify({'public_id': node_address,'wallet_balance': blockchain.get_wallet_balance(node_address)}), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000, threaded=True)