from textwrap import dedent
from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    return "We're mining a new block!"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Ensure that all the required fields are in the POST
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/', methods=['GET'])
def index():
    return f"Cody's blockchain node #{node_identifier}"

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3000)
    app.run(host='0.0.0.0', port=3000, debug=True)
