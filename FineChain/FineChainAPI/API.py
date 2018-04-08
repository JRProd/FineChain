from rx import Observable
import requests

from time import sleep

SERVER = 'http://159.89.159.158'
AUTH = '/auth'
COMPANY = '/company'
COMPANY_ID = '/company/%i'
FULLCHAIN = '/fullchain'
REFRESH = '/refresh'
USER = '/user'
USER_ID= '/user/%i'

def login(username, password):
    body = {
        'username':username,
        'password':password
    }
    return Observable.create(lambda  observer:
        rxRequest(observer, 'post', SERVER+AUTH, json=body))


def refresh(session):
    print("REFRESHING")
    return Observable.create(lambda observer:
        rxRequest(observer, 'get', SERVER+REFRESH, session=session, refresh_token=True)
    )


def createCompany(name, session=None):
    body = {
        'name':name
    }
    return Observable.create(lambda observer:
        rxRequest(observer, 'post', SERVER+COMPANY, session=session, json=body)
    )


def updateCompany():
    pass


def addUsersToCompany():
    pass


def removeUsersFromCompnay():
    pass


def getCompany(company_id):
    return Observable.create(lambda observer:
        rxRequest(observer, 'get', SERVER+COMPANY_ID % company_id))


def getCompanyFullchain(compnay_id, session):
    return Observable.create(lambda observer:
        rxRequest(observer, 'get', SERVER+(COMPANY_ID% compnay_id)+FULLCHAIN, session=session))


def addTransaction():
    pass


def getCompanyUpdatedChain():
    pass


def verifyCompanyChain():
    pass


def createUser(name, username, password, email=None):
    body = {
        'name':name,
        'username': username,
        'password': password,
        'email': email
    }
    return Observable.create(lambda observer: rxRequest(observer, 'post', SERVER+USER, json=body))


def updateUser():
    pass


def getUser(user_id):
    return Observable.create(lambda observer: rxRequest(observer, 'get', SERVER+USER_ID % user_id))

from pprint import pprint

def rxRequest(observer, method, url, session=None, refresh_token=False, **kwargs):
    def generateHeaders():
        headers = {}
        if session is not None:
            token = 'Bearer '
            if refresh_token == True:
                token += session.refresh_token
            else:
                token += session.session_token
            headers['Authorization'] = token
        return headers
    
    print("REQUEST SENT")
    response = requests.request(method, url, headers=generateHeaders(), **kwargs)

    def observerCallback(r):
        try:
            json = r.json()
            observer.on_next(json)
        except ValueError as e:
            observer.on_next(r)
        observer.on_completed()

    # Unauthorized access
    if response.status_code == 401:
        print('UNAUTHORIZED ACCESS')
        if session is not None:
            refresh(session).subscribe(
                on_next=lambda response:session.updateSession(response['body']['session']),
                on_completed=lambda: observerCallback(requests.request(method, url, headers=generateHeaders(), **kwargs))
            )

    # Resource Not Found
    elif response.status_code == 404:
        observerCallback(response)
    else:
        observerCallback(response)
