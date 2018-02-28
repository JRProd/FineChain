import hashlib, random, sys

def compare(challenge, actual):
    return challenge == actual

def generateSalt():
    return random.randint(-sys.maxsize-1, sys.maxsize)

def hash(password, salt):
    saltedPassword = password + salt
    return hashlib.sha512(saltedPassword)
