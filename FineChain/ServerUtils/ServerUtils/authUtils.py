import hashlib, random, sys
from datetime import datetime, timedelta
from ServerUtils import sqlUtils

def authenticate(username, challenge):
    user = sqlUtils.getUserWithUsername(username)

    #TODO Handle errors like no user found

    salt = user['salt']
    actual = user['password']

    #TODO Authenticate should not return true. TESTING
    #return (True, user['id'])
    return (compare(hash(challenge, salt), actual), user['id'])

def compare(challenge, actual):
    return challenge == actual

def generateToken(seed):
    return hashlib.md5(str(seed).encode('utf-8')).hexdigest()

def generateSalt():
    return random.randint(0, 2147483647)

def hash(password, salt):
    saltedPassword = str(password + str(salt)).encode('utf-8')
    return hashlib.sha512(saltedPassword).hexdigest()

def getSession(headers):
    authHeader = headers['Authorization'].split()
    tokenType = authHeader[0]
    token = authHeader[1]

    if tokenType == 'Bearer':
        return (True, sqlUtils.getSession(token))
    else:
        return (False, None)


def createSession(user_id):
    session = generateToken(str(user_id) + str(datetime.time))
    resession = generateToken(datetime.time)

    sessionExperation = (datetime.now() + timedelta(minutes=240)).strftime('%Y-%m-%d %H:%M:%S')

    return sqlUtils.openSession(user_id, session, resession, sessionExperation)
