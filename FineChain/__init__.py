#!/bin/usr/python

from flask import Flask
app = Flask(__name__)

@app.route('/user', methods=['POST', 'PUT'])
def hello_world():
	return 'Hello World!'

@app.route('/user/<int:user_id>', methods=['GET'])
def getUser(user_id):
    return f'GET-Gets the user with id {user_id}'


if __name__ == '__main__':
	app.run()
