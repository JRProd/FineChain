from rx import Observable
import requests

# Predefined enpoints
SERVER =     'http://159.89.159.158'
AUTH =       '/auth'
COMPANY =    '/company'
COMPANY_ID = '/company/%s'
FULLCHAIN =  '/fullchain'
POST =       '/post'
UPDATE =     '/update'
VERIFY =     '/verify'
REFRESH =    '/refresh'
USER =       '/user'
USER_ID=     '/user/%s'

def login(username, password):
    body = {
        'username':username,
        'password':password
    }
    return Observable.create(lambda  observer:
        rxRequest(observer, 'post', SERVER+AUTH, json=body)
    )


def refresh(session):
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


def updateCompany(name, admin=None, session=None):
    body = {
        'name':name
    }
    # Add admin to update if updating admin
    if admin is not None:
        body['admin'] = admin

    return Observable.create(lambda  observer:
        rxRequest(observer, 'put', SERVER+COMPANY, session=session, json=body)
    )


def addUsersToCompany(company_id, users, session=None):
    for user in users:
        if type(user) is not tuple:
            raise ValueError('The list must contain all tuples')
        if len(user) != 2:
            raise ValueError('Each tuple can only contain two entries')

    # Add users in the correct format
    users_to_add = {'users':[]}
    for id, username in users:
        users_to_add['users'].append({
            'id':id,
            'username':username
        })

    return Observable.create(lambda observer:
        rxRequest(observer, 'put', SERVER+(COMPANY_ID % company_id)+USER, session=session, json=users_to_add)
    )


def removeUsersFromCompany(company_id, users, session=None):
    for user in users:
        if type(user) is not tuple:
            raise ValueError('The list must contain all tuples')
        if len(user) != 2:
            raise ValueError('Each tuple can only contain two entries')

    # Add users in the correct format
    users_to_remove = {'users':[]}
    for id, username in users:
        users_to_remove['users'].append({
            'id':id,
            'username':username
        })

    return Observable.create(lambda observer:
        rxRequest(observer, 'delete', SERVER+(COMPANY_ID % company_id)+USER, session=session, json=users_to_remove)
    )


def getCompany(company_id):
    return Observable.create(lambda observer:
        rxRequest(observer, 'get', SERVER+COMPANY_ID % company_id)
    )


def getCompanyFullchain(compnay_id, session):
    return Observable.create(lambda observer:
        rxRequest(observer, 'get', SERVER+(COMPANY_ID % compnay_id)+FULLCHAIN, session=session)
    )


def postTransaction(company_id, to, recipient, amount, session=None):
    body = {
        'to':to,
        'recipient':recipient,
        'amount':amount
    }

    return Observable.create(lambda observer:
        rxRequest(observer, 'post', SERVER+(COMPANY_ID % company_id)+POST, session=session, json=body)
    )


def getCompanyUpdatedChain(company_id, prev_hash, current_transaction, session=None):
    body = {
        'prev_hash':prev_hash,
        'current_transaction':current_transaction
    }

    return Observable.create(lambda observer:
        rxRequest(observer, 'post', SERVER+(COMPANY_ID % company_id)+UPDATE, session=session, json=body)
    )


def verifyCompanyChain(company_id, prev_hash, current_transaction, session=None):
    body = {
        'prev_hash': prev_hash,
        'current_transaction': current_transaction
    }

    return Observable.create(lambda observer:
         rxRequest(observer, 'post', SERVER + (COMPANY_ID % company_id) + VERIFY, session=session, json=body)
    )


def createUser(name, username, password, email=None):
    body = {
        'name':name,
        'username': username,
        'password': password,
        'email': email
    }
    return Observable.create(lambda observer:
        rxRequest(observer, 'post', SERVER+USER, json=body)
    )


def updateUser(name=None, email=None, password=None, session=None):
    # Build what is needed to be updated
    body = {}
    if name is not None:
        body['name'] = name
    if email is not None:
        body['email'] = email
    if password is not None:
        body['password'] = password

    return Observable.create(lambda observer:
        rxRequest(observer, 'put', SERVER+USER, session=session, json=body)
    )


def getUser(user_id):
    return Observable.create(lambda observer:
        rxRequest(observer, 'get', SERVER+USER_ID % user_id)
    )

from pprint import pprint

def rxRequest(observer, method, url, session=None, refresh_token=False, **kwargs):
    # Create the auth headers if required
    def generateHeaders():
        headers = {}
        if session is not None:
            token = 'Bearer '
            # Switches between refresh or session token used
            if refresh_token == True:
                token += session.refresh_token
            else:
                token += session.session_token
            headers['Authorization'] = token
        return headers

    # Send HTTPS request
    response = requests.request(method, url, headers=generateHeaders(), **kwargs)

    # Define a callback if error response
    def observerCallback(r):
        # Convert to json
        try:
            json = r.json()
            observer.on_next(json)
        # Or just return the response
        except ValueError as e:
            observer.on_next(r)
        # Complete the observable
        observer.on_completed()

    # Unauthorized access
    if response.status_code == 401:
        if session is not None:
            # Send another request to refresh the token
            refresh(session).subscribe(
                # On refresh, update the session class
                on_next=lambda response:session.updateSession(response['body']['session']),
                # Once the session is updated, try the call again
                on_completed=lambda: observerCallback(requests.request(method, url, headers=generateHeaders(), **kwargs))
            )

    # Resource Not Found
    elif response.status_code == 404:
        observerCallback(response)
    else:
        observerCallback(response)
