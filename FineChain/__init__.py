#!/bin/usr/python

import sys
from datetime import datetime

from flask import Flask, request, Response
import flask_jwt_extended as JWT

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x07-\n4K~\xe7\x1e|\xd0\x08\xa7\x95\xf1\xeeV"\x1f\x8f\x0f\x0e\n5YV\xb9\x87=#\x00\xa6b'

jwt = JWT.JWTManager(app)

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
@JWT.jwt_optional
def authenticate():
    if request.method == 'POST':
        body = request.get_json()

        username = body['username']
        password = body['password']

        success, user_id = authUtils.authenticate(username, password)

        if success:
            session = {
                'session':JWT.create_access_token(identity={'user_id':user_id})
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
@JWT.jwt_optional
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
@JWT.jwt_required
def addUserToCompany(company_id):
    if request.method == 'POST':
        return 'POST-Add user to a company'
    else:
        return 'DELETE-Remove a user from a company'

@app.route('/company/<int:company_id>/fullchain', methods=['GET'])
@JWT.jwt_required
def getFullchain(company_id):
    return 'GET-Gets the fullchain'

@app.route('/company/<int:company_id>/post', methods=['POST'])
@JWT.jwt_required
def postTransaction(company_id):
    return 'POST-Add a transaction to a company'

@app.route('/company/<int:company_id>/update', methods=['GET'])
@JWT.jwt_required
def getUpdatedBlockchain(company_id):
    return 'GET-Gets the updates from the blockchain'

@app.route('/company/<int:company_id>/verify', methods=['GET'])
@JWT.jwt_required
def verifyBlockchain(company_id):
    return 'GET-Verify blockchain for company'


#####################
##  USER Endpoints ##
#####################
# Define sql commands commonly used

@app.route('/user', methods=['POST', 'PUT'])
@JWT.jwt_optional
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
        user = JWT.get_jwt_identity()
        body = request.get_json()

        if user is not None:
            # Get all the possible changes that were submitted in the body
            changes = ['name', 'email']
            infoUpdate = {}
            for change in changes:
                if change in body:
                    infoUpdate[change] = body[change]

            updated = sqlUtils.updateUserInfo(user_id=user['user_id'], data=infoUpdate)
            updated['updated_at'] = datetime.now()

            updatePass = False
            if 'password' in body:
                sqlUtils.updateUserPassword(data={'id':user['user_id'], 'password':body['password']})
                updatePass = True

            if updatePass:
                updated['password']='Password Updated'

            return basicUtils.MessageResponse(
                message='Account Updated',
                body=updated
            ).toJson(), 200

        else:
            return basicUtils.unauthroized_response.toJson(), 401



@app.route('/user/<int:user_id>', methods=['GET'])
def getUser(user_id):
    return basicUtils.MessageResponse(
        message='Successfully retrieved the USER',
        body=sqlUtils.getUserWithId(user_id)
    ).toJson(), 200


if __name__ == '__main__':
	app.run()
