import hashlib, random, sys
from datetime import datetime, timedelta
import sqlUtils

def authenticate(username, challenge):
    user = sqlUtils.getUserWithUsername(username)

    #TODO Handle errors like no user found

    salt = user[5]
    actual = user[6]

    #TODO Authenticate should not return true. TESTING
    return True
    #return compare(hass(challenge, salt), actual)

def compare(challenge, actual):
    return challenge == actual

def generateToken(seed):
    return hashlib.md5(seed)

def generateSalt():
    return random.randint(0, 2147483647)

def hash(password, salt):
    saltedPassword = str(password + str(salt)).encode('utf-8')
    return hashlib.sha512(saltedPassword).hexdigest()

def createSession(username):
    session = token(username + str(datetime.time))
    resession = token(datetime.time)

    user = getUserWithUsername(username)

    sessionExperation = (datetime.now() + timedelta(minutes=240)).strftime('%Y-%m-%d %H:%M:%S')

    return sqlUtils.openSession(username, session, resession, sessionExperation)
