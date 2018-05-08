import hashlib, sys
from random import random

from ServerUtils import sqlUtils

# Import a cryptographically secure password hashing library 
from passlib.hash import pbkdf2_sha512 as sha512

def authenticate(username, challenge):
    try:
        # Get the user with associated username
        user = sqlUtils.getUserWithUsername(username)
        actual = user['password']

        # Compare the challenge and the actual password
        return (compare(challenge, actual), user['id'])
    except ValueError as e:
        return False

def compare(challenge, actual):
    return sha512.verify(challenge, actual)

def hash(password):
    return sha512.hash(password)

# Quick check if user is part of the company
def userPartOfCompany(user_id, company_id):
    user = sqlUtils.getUserWithId(user_id)
    return user['company_id'] == company_id
