#!/usr/bin/env python3
# coding=utf-8
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from uuid import uuid4

try:
  from urllib.parse import urlparse
except:
  from urlparse import urlparse

# import Modified Blockchain Framework
from Blockchain import Blockchain
# A Globally unique address for this node
node_identifier  = str(uuid4()).replace('-','')

#  Instatiate the Blockchain
blockchain = Blockchain()

# response header
JSON_HEADER = [('Content-type', 'application/json')]
STATUS_OK =  '200 OK'
STATUS_400 = '400'
STATUS_201 = '201'

app = Flask(__name__)

base_path = ''

@app.route('/', methods=['GET', 'POST'])
def home():
    resp = make_response('<h1>Home<h1>', 200)
    return resp

@app.route('/signin', methods=['GET'])
def signin_form():
    global base_path
    html = '''<form action="{}/signin" method="post">
         <p><input name="username"></p>
         <p><input name="password" type="password"></p>
         <p><button type="submit">Sign In</button></p>
         </form>'''.format(base_path)

    resp = make_response(html, 200)
    return resp

@app.route('/signin', methods=['POST'])
def signin():
    if request.form['username']=='admin' and request.form['password']=='password':
        html = '<h3>Hello, admin!</h3>'
    else:
        html = '<h3>Bad username or password.</h3>'
    resp = make_response(html, 200)
    return resp

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return make_response(jsonify(response), STATUS_OK)

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        response = {'error': 'Missing values'}
        return make_response(jsonify(response), STATUS_400)

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    
    response = {'message': f'Transaction will be added to Block {index}'}
    return make_response(jsonify(response), STATUS_201)


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return make_response(jsonify(response), STATUS_OK)


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        response = {'error':'Please supply a valid list of nodes'}
        return make_response(jsonify(response), STATUS_400)

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return make_response(jsonify(response), STATUS_201)


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return make_response(jsonify(response), STATUS_OK)



def handler(environ, start_response):
    parsed_tuple = urlparse(environ['fc.request_uri'])
    li = parsed_tuple.path.split('/')
    global base_path
    if not base_path:
        base_path = "/".join(li[0:5])
    return app(environ, start_response)
