#!/bin/usr/python

import json
from flask import Flask, request, Response, jsonify



#class FineChainResponse(Response):
#    default_mimetype = 'application/json'

class MessageResponse:
    message = 'Failure'
    body = '{}'

    def __init__(self, message, body):
        self.message = message
        self.body = body

    def toJson(self):
        return jsonify(
                    message=self.message,
                    body=self.body
                )

app = Flask(__name__)
#app.make_response = FineChainResponse


from mysql import connector
cnx = connector.connect(user='flaskUser', password='MMv8nN9*gVZn.gn0Df5L',
            host='127.0.0.1',
            database='FineChain')


####################
## TEST Endpoints ##
####################
@app.route('/')
def home():
    return "Homepage"
@app.route('/isrunning')
def isRunning():
    return 'Yes, the flask app is running!'


####################
## AUTH Endpoints ##
####################
@app.route('/auth', methods=['POST', 'DELETE'])
def authenticate():
    if request.method == 'POST':
        return 'POST-Login'
    else:
        return 'DELETE-Logout'


#######################
## COMPANY Endpoints ##
#######################
@app.route('/company', methods=['POST', 'PUT'])
def updateCompany():
    if request.method == 'POST':
        return 'POST-Create a new company here'
    else:
        return 'PUT-Update a company'

@app.route('/company/<int:company_id>', methods=['GET'])
def getCompany(company_id):
    returnVal = 'GET-Gets the company with id ' + str(company_id)
    return returnVal

@app.route('/company/<int:company_id>/user', methods=['POST', 'DELETE'])
def addUserToCompany(company_id):
    if request.method == 'POST':
        return 'POST-Add user to a company'
    else:
        return 'DELETE-Remove a user from a company'

@app.route('/company/<int:company_id>/fullchain', methods=['GET'])
def getFullchain(company_id):
    return 'GET-Gets the fullchain'

@app.route('/company/<int:company_id>/post', methods=['POST'])
def postTransaction(company_id):
    return 'POST-Add a transaction to a company'

@app.route('/company/<int:company_id>/update', methods=['GET'])
def getUpdatedBlockchain(company_id):
    return 'GET-Gets the updates from the blockchain'

@app.route('/company/<int:company_id>/verify', methods=['GET'])
def verifyBlockchain(company_id):
    return 'GET-Verify blockchain for company'


#####################
##  USER Endpoints ##
#####################
# Define sql commands commonly used
get_user_with_id = ("SELECT id, name, email, company_id, username, created_at, updated_at, deleted_at"
                    "FROM users"
                    "WHERE users.id = %(id)s")
insert_user = ("INSERT INTO users "
               "(name, username, password, salt) "
               "VALUES (%(name)s, %(username)s, %(password)s, %(salt)s)")
@app.route('/user', methods=['POST', 'PUT'])
def updateUser():
    cursor = cnx.cursor()
    if request.method == 'POST':

        body = request.get_json()
        email = None
        if 'email' in body:
            email = body['email']
        insertValues = {
            'name':body['name'],
            'email':email,
            'username':body['username'],
            'password':body['password'],
            'salt':body['salt'],
        }

        cursor.execute(insert_user, insertValues)
        id = cursor.lastrowid

        user = {
            'id':id,
            'name':insertValues['name'],
            'email':insertValues['email'],
            'company_id':None,
            'username':insertValues['username'],
        }

        cnx.commit()
        cursor.close()

        return MessageResponse(
                    message='Successfully created new USER',
                    body=user
                ).toJson()
    else:
        return 'PUT-Update a user'


@app.route('/user/<int:user_id>', methods=['GET'])
def getUser(user_id):
    returnVal = 'GET-Gets the user with id ' + str(user_id)
    return returnVal


if __name__ == '__main__':
	app.run()
