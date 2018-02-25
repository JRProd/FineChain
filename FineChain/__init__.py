#!/bin/usr/python

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Homepage"

@app.route('/isrunning')
def isRunning():
    return 'Yes, the flask app is running!'

@app.route('/user', methods=['POST', 'PUT'])
def hello_world():
	return 'Hello World!'

@app.route('/user/<int:user_id>', methods=['GET'])
def getUser(user_id):
    temp = f'GET-Gets the user with id {user_id}'
    return temp


if __name__ == '__main__':
	app.run()
