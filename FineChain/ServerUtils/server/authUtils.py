import hashlib, random, sys

def generateSalt():
    return random.randint(-sys.maxsize-1, sys.maxsize)

def hash(password, salt):
    saltedPassword = password + salt
    return hashlib.sha512(saltedPassword)
