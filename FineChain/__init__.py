#!/bin/usr/python

from flask import Flask
app = Flask(__name__)

# These are only test methods
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
def getCompany():
    returnVal = 'GET-Gets the company with id ' + str(company_id)
    return returnVal

@app.route('/company/<int:company_id>/user', methods=['POST', 'DELETE'])
def addUserToCompany():
    if request.method == 'POST':
        return 'POST-Add user to a company'
    else:
        return 'DELETE-Remove a user from a company'

@app.route('/company/<int:company_id>/fullchain', methods=['GET'])
def getFullchain():
    return 'GET-Gets the fullchain'

@app.route('/company/<int:company_id>/post', methods=['POST'])
def postTransaction():
    return 'POST-Add a transaction to a company'

@app.route('/company/<int:company_id>/update', methods=['GET'])
def getUpdatedBlockchain():
    return 'GET-Gets the updates from the blockchain'

@app.route('/company/<int:company_id>/verify', methods=['GET'])
def verifyBlockchain():
    return 'GET-Verify blockchain for company'


#####################
##  USER Endpoints ##
#####################
@app.route('/user', methods=['POST', 'PUT'])
def updateUser():
    if request.method == 'POST':
        return 'POST-Create a new user here'
    else:
        return 'PUT-Update a user'

@app.route('/user/<int:user_id>', methods=['GET'])
def getUser(user_id):
    returnVal = 'GET-Gets the user with id ' + str(user_id)
    return returnVal





if __name__ == '__main__':
	app.run()
