#!/bin/usr/python

from flask import Flask, request, Response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x07-\n4K~\xe7\x1e|\xd0\x08\xa7\x95\xf1\xeeV"\x1f\x8f\x0f\x0e\n5YV\xb9\x87=#\x00\xa6b'

jwt = JWTManager(app)

from ServerUtils import authUtils, basicUtils, sqlUtils

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
        body = request.get_json()

        username = body['username']
        password = body['password']

        success, user_id = authUtils.authenticate(username, password)

        if success:
            session = {
                'session':create_access_token(identifier=user_id)
            }
            return basicUtils.MessageResponse(
                message="Successfully loged in",
                body=session
            ).toJson(), 200
        else:
            return basicUtils.MessageResponse(
                message='Invalid username or password'
            ).toJson(), 401
    else:
        return 'DELETE-Logout'


#######################
## COMPANY Endpoints ##
#######################
@app.route('/company', methods=['POST', 'PUT'])
def updateCompany():
    if request.method == 'POST':
        body = request.get_json()

        company = sqlUtils.postCompany(
            name=body['name'],
            admin_id=body['admin_id']
        )

        return basicUtils.MessageResponse(
            message='Successfully created new COMPANY',
            body=company
        ).toJson(), 201
    else:
        return 'PUT-Update a company'

@app.route('/company/<int:company_id>', methods=['GET'])
def getCompany(company_id):
    return basicUtils.MessageResponse(
        message='Successfully got the COMPANY',
        body=sqlUtils.getCompany(company_id)
    ).toJson(), 200

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

@app.route('/user', methods=['POST', 'PUT'])
def updateUser():
    if request.method == 'POST':
        body = request.get_json()
        email = None
        if 'email' in body:
            email = body['email']

        password = authUtils.hash(body['password'])

        user = sqlUtils.postUser(
            name=body['name'],
            email=email,
            username=body['username'],
            password=password
        )

        return basicUtils.MessageResponse(
            message='Successfully created new USER',
            body=user
        ).toJson(), 201
    else:
        open, session = authUtils.getSession(request.headers)
        body = request.get_json()

        if open:
            # Get all the possible changes that were submitted in the body
            changes = {'name','email','password'}
            updates = {}
            for change in changes:
                if change in body:
                    updates[change] = body[change]

            updated = sqlUtils.updateUser(user_id=session['user_id'], data=updates)

            return basicUtils.MessageResponse(
                message='Account Updated',
                body=updated
            ).toJson(), 200

        else:
            return unauthroized_response.toJson(), 401



@app.route('/user/<int:user_id>', methods=['GET'])
def getUser(user_id):
    return basicUtils.MessageResponse(
        message='Successfully retrieved the USER',
        body=sqlUtils.getUserWithId(user_id)
    ).toJson(), 200


if __name__ == '__main__':
	app.run()
