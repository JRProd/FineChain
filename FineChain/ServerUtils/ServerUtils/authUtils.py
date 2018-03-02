import hashlib, random, sys
import sqlUtils

def authenticate(username, challenge):
    user = sqlUtils.getUserWithUsername(username)

    #TODO Handle errors like no user found

    salt = user[5]
    actual = user[6]

    return compare(hass(challenge, salt), actual)

def compare(challenge, actual):
    return challenge == actual

def generateSalt():
    return random.randint(0, 2147483647)

def hash(password, salt):
    saltedPassword = str(password + str(salt)).encode('utf-8')
    return hashlib.sha512(saltedPassword).hexdigest()
