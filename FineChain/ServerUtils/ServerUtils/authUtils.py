import hashlib, sys
from random import random

from ServerUtils import sqlUtils

from passlib.hash import pbkdf2_sha512 as sha512

def authenticate(username, challenge):
    user = sqlUtils.getUserWithUsername(username)

    #TODO Handle errors like no user found
    actual = user['password']

    #TODO Authenticate should not return true. TESTING
    #return (True, user['id'])
    return (compare(challenge, actual), user)

def compare(challenge, actual):
    return sha512.verify(challenge, actual)

def generateToken(seed):
    return hashlib.md5(str(seed).encode('utf-8')).hexdigest()

def hash(password):
    return sha512.hash(password)

def getSession(headers):
    authHeader = headers['Authorization']
    print(authHeader, file=sys.stderr)
    #tokenType = authHeader[0]
    #token = authHeader[1]

    #if tokenType == 'Bearer':
        #return (True, sqlUtils.getSession(token))
    #else:
        #return (False, None)


def createSession(user_id):
    session = generateToken(str(user_id) + str(datetime.time))
    resession = generateToken(datetime.time)

    sessionExperation = (datetime.now() + timedelta(minutes=240)).strftime('%Y-%m-%d %H:%M:%S')

    return sqlUtils.openSession(user_id, session, resession, sessionExperation)
