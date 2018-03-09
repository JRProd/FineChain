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

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x07-\n4K~\xe7\x1e|\xd0\x08\xa7\x95\xf1\xeeV"\x1f\x8f\x0f\x0e\n5YV\xb9\x87=#\x00\xa6b'
app.config['COMPANY_LOCATION'] = 'files/'

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

@app.errorhandler(404)
def pageNotFound(err):
    return basicUtils.MessageResponse(
        message='Default 404'
    ).toJson()

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
            blockLocation = os.path.join(app.root_path, app.config['COMPANY_LOCATION']) + str(company['id'])
            blockFile = blockLocation + '/blockchain.json'
            pathlib.Path(blockLocation).mkdir(parents=False, mode=0o774, exist_ok=True)
            blockchain = open(blockFile, 'w')
            blockchain.write('{}')

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
            infoUpdate = {}
            for change in changes:
                if change in body:
                    infoUpdate[change] = body[change]

            updated = sqlUtils.updateCompanyInfo(company_id=user['company_id'], data=infoUpdate)
            updated['updated_at'] = datetime.now()

            updateAdmin = False
            if 'admin' in body:
                admim = sqlUtils.updateCompanyAdmin(
                    company_id=user['company_id'],
                    id=body['admin']['id'],
                    username=body['admin']['username']
                )
                updateAdmin = True

            if updateAdmin:
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
            for user in users:
                addedUser = sqlUtils.addUserToCompany(
                    company_id=admin['company_id'],
                    user_id=user['id'],
                    username=user['username']
                )
                responses.append(addedUser)

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
            for user in users:
                removedUser = sqlUtils.removeUserFromCompany(
                    company_id=admin['company_id'],
                    user_id=user['id'],
                    username=user['username']
                )
                responses.append(removedUser)

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

    if authUtils.userPartOfCompany(session['user_id'], company_id):
        blockLocation = os.path.join(app.root_path, app.config['COMPANY_LOCATION']) + str(company_id)

        try:
            return send_from_directory(directory=blockLocation, filename='blockchain.json'), 200
        except NotFound as exc:
            return basicUtils.notFoundResponse(
                object='Company',
                value=company_id
            ).toJson(), 404
    else:
        return basicUtils.unauthroized_response.toJson(), 401

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
