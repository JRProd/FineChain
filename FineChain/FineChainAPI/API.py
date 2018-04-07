from rx import Observable
import requests

from time import sleep

SERVER = 'http://159.89.159.158'
AUTH = '/auth'
COMPANY = '/company'
REFRESH = '/refresh'
USER = '/user'

def login(username, password):
    body = {
        'username':username,
        'password':password
    }
    return Observable.create(lambda  observer:
        rxRequest(observer, 'post', SERVER+AUTH, json=body))


def refresh(session):
    print("REFRESSING")
    Observable.create(lambda observer:
        rxRequest(observer, 'get', SERVER+REFRESH, session=session, refresh=True)
    ).subscribe(
        on_next=lambda response:session.updateSession(response['body']['session'])
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


def getCompany():
    pass


def getCompanyFullchain():
    pass


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


def getUser():
    pass

def rxRequest(observer, method, url, session=None, refresh=False, **kwargs):
    headers = {}
    if session is not None:
        token = 'Bearer '
        if refresh == True:
            token += session['refresh']
        else:
            token += session['session']
        headers['Authorization'] = token
    response = requests.request(method, url, headers=headers, **kwargs)

    # Unauthorized access
    if response.status_code == 401:
        print('UNAUTHORIZED ACCESS')
        if session is not None:
            refresh(session)
            sleep(0.2)
            for i in range(1,3):
                print("SLEEPING")
                response = requests.request(method, url, headers=headers, **kwargs)
                if response.status_code == 401:
                    print("STILL SLEEPING")
                    sleep(0.1*i)
                else:
                    print("WORKED")
                    break
    # Resource Not Found
    elif response.status_code == 404:
        pass
    else:
        try:
            json = response.json()
            observer.on_next(json)
        except ValueError as e:
            print("ERROR in JSON")
            print(response)
            print(e)