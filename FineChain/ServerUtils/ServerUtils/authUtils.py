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
    return (compare(challenge, actual), user['id'])

def compare(challenge, actual):
    return sha512.verify(challenge, actual)

def generateToken(seed):
    return hashlib.md5(str(seed).encode('utf-8')).hexdigest()

def hash(password):
    return sha512.hash(password)

def userPartOfCompany(user_id, company_id):
    user = sqlUtils.getUserWithId(user_id)
    return user['company_id'] == company_id
