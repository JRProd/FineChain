import hashlib, random, sys

def generateSalt():
    return random.randomint(-sys.maxint-1, sys.maxint)

def hash(password, salt):
    saltedPassword = password + salt
    return hashlib.sha512(saltedPassword)
