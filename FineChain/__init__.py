#!/bin/usr/python

import sys, os, pathlib
from datetime import datetime

from flask import (
        Flask,
        request,
        Response,
        send_from_directory
)
from werkzeug.exceptions import NotFound
import flask_jwt_extended as JWT
import pickle

# Intialize the applicaiton
app = Flask(__name__)

# Defines SECRET_KEY for JWT and blockchain file location
app.config['SECRET_KEY'] = b'\x07-\n4K~\xe7\x1e|\xd0\x08\xa7\x95\xf1\xeeV"\x1f\x8f\x0f\x0e\n5YV\xb9\x87=#\x00\xa6b'
app.config['COMPANY_LOCATION'] = 'files/'

# Intialize the JWT manager
jwt = JWT.JWTManager(app)

from ServerUtils import authUtils, basicUtils, sqlUtils

# Import the blockchain for creating new chains when a company is created
from Blockchain.Blockchain import Blockchain
# Import the buffer that controls when files are loaded and deloaded
from BlockchainBuffer.BlockchainBuffer import BlockchainBuffer
# Initalze the buffer
blockchainBuffer = BlockchainBuffer(
    root_loc=app.root_path,
    company_loc=app.config['COMPANY_LOCATION']
)

####################
## TEST Endpoints ##
####################
@app.route('/')
def home():
    return "Homepage"
@app.route('/isrunning')
def isRunning():
    return 'Yes, the flask app is running!'

# Default 404 response
@app.errorhandler(404)
def pageNotFound(err):
    return basicUtils.MessageResponse(
        message='Default 404'
    ).toJson()

# Default JWT resposne
@jwt.expired_token_loader
def expiredTokenLoaderCallback():
    return basicUtils.expired_token.toJson(), 401

#####################
## REFRESH Endpoin ##
#####################
@app.route('/refresh', methods=['GET'])
@JWT.jwt_refresh_token_required
def refresh():
    # Get current session
    session = JWT.get_jwt_identity()
    # Create a new session
    newSession = {
        'session':JWT.create_access_token(identity=session)
    }
    # Return new session
    return basicUtils.MessageResponse(
        message='New session token created',
        body=newSession
    ).toJson(), 200

####################
## AUTH Endpoints ##
####################
@app.route('/auth', methods=['POST'])
@JWT.jwt_optional
def authenticate():
    if request.method == 'POST':
        body = request.get_json()

        # Check if challenge is valid
        success, user_id = authUtils.authenticate(body['username'], body['password'])

        if success:
            # Create a new session
            session = {
                'session':JWT.create_access_token(identity={'user_id':user_id}),
                'refresh':JWT.create_refresh_token(identity={'user_id':user_id})
            }
            # Return new session
            return basicUtils.MessageResponse(
                message="Successfully loged in",
                body=session
            ).toJson(), 200
        else:
            # Invlaid login resposne
            return basicUtils.MessageResponse(
                message='Invalid username or password'
            ).toJson(), 401
    else:
        return 'DELETE-Logout'


#######################
## COMPANY Endpoints ##
#######################
@app.route('/company', methods=['POST', 'PUT'])
@JWT.jwt_required
def updateCompany():
    if request.method == 'POST':
        session = JWT.get_jwt_identity()
        body = request.get_json()

        if session is not None:
            # Create company
            company = sqlUtils.postCompany(
                name=body['name'],
                admin_id=session['user_id']
            )

            # Create blockchain and file location
            company['blockchain'] = sqlUtils.postBlockchain(company_id=company['id'])
            companyBlockchain = Blockchain(id=company['blockchain']['id'], company_id=company['id'])
            # Create the directory for the company
            blockLocation = os.path.join(app.root_path, app.config['COMPANY_LOCATION']) + str(company['id'])
            pathlib.Path(blockLocation).mkdir(parents=False, mode=0o774, exist_ok=True)
            blockFile = open(blockLocation + '/blockchain.pkl', 'wb')

            pickle.dump(companyBlockchain, blockFile)

            # Update user after company is created
            infoUpdate = {'company_id':company['id']}
            company['admin'] = sqlUtils.updateUserInfo(user_id=session['user_id'], data=infoUpdate)
            company['admin']['updated_at'] = datetime.now()

            return basicUtils.MessageResponse(
                message='Successfully created new COMPANY',
                body=company
            ).toJson(), 201
        else:
            return basicUtils.unauthroized_response.toJson(), 401
    else:
        session = JWT.get_jwt_identity()
        body = request.get_json()

        if session is not None:
            user = sqlUtils.getUserWithId(session['user_id'])

            # Get all the possible changes that were submitted in the body
            if user['company_id'] is None:
                return basicUtils.notFoundResponse(
                    object='Company associated with this users',
                    value=user['id']
                ).toJson(), 404
            changes = ['name', 'user_ids']
            # Build updated info
            infoUpdate = {}
            for change in changes:
                if change in body:
                    infoUpdate[change] = body[change]

            # Update the info
            updated = sqlUtils.updateCompanyInfo(company_id=user['company_id'], data=infoUpdate)
            updated['updated_at'] = datetime.now()

            # Specifically check if admin is being updated
            if 'admin' in body:
                admin = sqlUtils.updateCompanyAdmin(
                    company_id=user['company_id'],
                    user_id=body['admin']['id'],
                    username=body['admin']['username']
                )
                updated['admin']=admin

            return basicUtils.MessageResponse(
                message='Company Updated',
                body=updated
            ).toJson(), 200

        else:
            return basicUtils.unauthroized_response.toJson(), 401

@app.route('/company/<int:company_id>', methods=['GET'])
def getCompany(company_id):
    try:
        return basicUtils.MessageResponse(
            message='Successfully got the COMPANY',
            body=sqlUtils.getCompanyWithId(company_id)
        ).toJson(), 200
    except ValueError:
        return basicUtils.notFoundResponse(
            object='Company',
            value=company_id
        ).toJson(), 404

@app.route('/company/<int:company_id>/user', methods=['POST', 'DELETE'])
@JWT.jwt_required
def addUserToCompany(company_id):
    if request.method == 'POST':
        session = JWT.get_jwt_identity()
        body = request.get_json()

        if session is not None:
            admin = sqlUtils.getUserWithId(session['user_id'])

            users = body['users']
            responses = []
            # Add users to the company
            for user in users:
                # Determine if successful
                success, addedUser = sqlUtils.addUserToCompany(
                    company_id=admin['company_id'],
                    user_id=user['id'],
                    username=user['username']
                )
                # Different values added based on success
                if success:
                    responses.append(addedUser)
                else:
                    responses.append({'user_id':user['id'], 'Failed':addedUser})

            return basicUtils.MessageResponse(
                message='Users added.',
                body={'users':responses}
            ).toJson(), 200
        else:
            return basicUtils.unauthroized_response.toJson(), 401
    else:
        session = JWT.get_jwt_identity()
        body = request.get_json()

        if session is not None:
            admin = sqlUtils.getUserWithId(session['user_id'])

            users = body['users']
            responses = []
            # Remove users from company
            for user in users:
                success, removedUser = sqlUtils.removeUserFromCompany(
                    company_id=admin['company_id'],
                    user_id=user['id'],
                    username=user['username']
                )
                # Differemt values added based on success
                if success:
                    responses.append(removedUser)
                else:
                    responses.append({'user_id':user['id'], 'Failed':removedUser})

            return basicUtils.MessageResponse(
                message='Users removed.',
                body={'users':responses}
            ).toJson(), 200
        else:
            return basicUtils.unauthroized_response.toJson(), 401

@app.route('/company/<int:company_id>/fullchain', methods=['GET'])
@JWT.jwt_required
def getFullchain(company_id):
    session = JWT.get_jwt_identity()

    if session is not None:
        if authUtils.userPartOfCompany(session['user_id'], company_id):
            # Saves the changes to a file
            blockchainBuffer.saveBlockchain(company_id)
            blockLocation = os.path.join(app.root_path, app.config['COMPANY_LOCATION']) + str(company_id)

            try:
                # Tries to provide the file
                return send_from_directory(directory=blockLocation, filename='blockchain.pkl'), 200
            except NotFound as exc:
                # Not found response
                return basicUtils.notFoundResponse(
                    object='Company',
                    value=company_id
                ).toJson(), 404
        else:
            return basicUtils.unauthroized_response.toJson(), 401
    else:
        return basicUtils.unauthroized_response.toJson(), 401

import sys
@app.route('/company/<int:company_id>/post', methods=['POST'])
@JWT.jwt_required
def postTransaction(company_id):
    print('postTransaction', file=sys.stderr)
    session = JWT.get_jwt_identity()
    body = request.get_json()

    if session is not None:
        if authUtils.userPartOfCompany(session['user_id'], company_id):
            # Adds transaction to the blockchain
            transaction = {
                'to':body['to'],
                'recipient':body['recipient'],
                'amount':body['amount']
            }
            blockchainBuffer.addTransaction(company_id=company_id, transaction=transaction)

            return basicUtils.MessageResponse(
                message='Transaction added',
                body=transaction
            ).toJson(), 200
        else:
            return basicUtils.unauthroized_response.toJson(), 401
    else:
        return basicUtils.unauthroized_response.toJson(), 401

@app.route('/company/<int:company_id>/update', methods=['POST'])
@JWT.jwt_required
def getUpdatedBlockchain(company_id):
    session = JWT.get_jwt_identity()
    body = request.get_json()

    if session is not None:
        if authUtils.userPartOfCompany(session['user_id'], company_id):
            # Gets the updated list of transactions
            transactions = blockchainBuffer.getListOfTransactions(company_id, body['prev_hash'], body['current_transaction'])

            # Returns them as a list with 0 being oldest and n being newest
            return basicUtils.MessageResponse(
                message='Updated Transactions',
                body=transactions
            ).toJson(), 200
        else:
            return basicUtils.unauthroized_response.toJson(), 401
    else:
        return basicUtils.unauthroized_response.toJson(), 401

@app.route('/company/<int:company_id>/verify', methods=['POST'])
@JWT.jwt_required
def verifyBlockchain(company_id):
    session = JWT.get_jwt_identity()
    body = request.get_json()

    if session is not None:
        if authUtils.userPartOfCompany(session['user_id'], company_id):
            if blockchainBuffer.verify(company_id, body['prev_hash'], body['current_transaction']):
                return basicUtils.MessageResponse(
                    message='Current hash matches the serverside hash',
                    body=True
                ).toJson(), 200
            else:
                return basicUtils.MessageResponse(
                    message='Your current hash does not match the server\'s hash',
                    body=False
                ).toJson(), 200
        else:
            return basicUtils.unauthroized_response.toJson(), 401
    else:
        return basicUtils.unauthroized_response.toJson(), 401


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
        session = JWT.get_jwt_identity()
        body = request.get_json()

        if session is not None:
            # Get all the possible changes that were submitted in the body
            changes = ['name', 'email']
            infoUpdate = {}
            for change in changes:
                if change in body:
                    infoUpdate[change] = body[change]

            updated = sqlUtils.updateUserInfo(user_id=session['user_id'], data=infoUpdate)
            updated['updated_at'] = datetime.now()

            updatePass = False
            if 'password' in body:
                password = authUtils.hash(body['password'])
                sqlUtils.updateUserPassword(id=session['user_id'], password=password)
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
    try:
        return basicUtils.MessageResponse(
            message='Successfully retrieved the USER',
            body=sqlUtils.getUserWithId(user_id)
        ).toJson(), 200
    except ValueError:
        return basicUtils.notFoundResponse(
            object='User',
            value=user_id
        ).toJson(), 404


if __name__ == '__main__':
	app.run()
