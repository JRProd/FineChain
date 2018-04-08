from Blockchain.Blockchain import Blockchain
from FineChainAPI import API

from pprint import pprint
import pickle, codecs

class Session():
    session_token =''
    refresh_token = ''
    def __init__(self, session, refresh):
        self.session_token = session
        self.refresh_token = refresh

    def updateSession(self, token):
        self.session_token = token

if __name__ == '__main__':
    print('STARTING API TESTING')
    session = Session(
        refresh='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1MjMxNDQzNjAsImlkZW50aXR5Ijp7InVzZXJfaWQiOjQ4fSwianRpIjoiNTVhYjc4MjgtZWU3Mi00OTY3LWI5Y2MtMjJlZTUwMjdmYzJiIiwibmJmIjoxNTIzMTQ0MzYwLCJleHAiOjE1MjU3MzYzNjAsInR5cGUiOiJyZWZyZXNoIn0.jSo8Ts92ZQcWMLtfE5zYTThGtF8WFsPKV0_jwt3y_Wk',
        session='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1MjMxNDQzNjAsImlkZW50aXR5Ijp7InVzZXJfaWQiOjQ4fSwidHlwZSI6ImFjY2VzcyIsImp0aSI6IjIwMmMwMzkzLTk5MzgtNGU2Mi1hMTI2LWE5YmFiNzE3NTgyZSIsIm5iZiI6MTUyMzE0NDM2MCwiZXhwIjoxNTIzMTQ1MjYwLCJmcmVzaCI6ZmFsc2V9.qO83bH9OQ60_cTNl7oO_jxCdDpYLP3htELcuL-nvfZM'
    )

    response = API.getUser(18).subscribe(on_next=lambda response: {
        print(response)
    })

