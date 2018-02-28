import hashlib, random, sys

def compare(challenge, actual):
    return challenge == actual

def generateSalt():
    return random.randint(0, 2147483647)

def hash(password, salt):
    saltedPassword = str(password + str(salt)).encode('utf-8')
    return hashlib.sha512(saltedPassword).hexdigest()
