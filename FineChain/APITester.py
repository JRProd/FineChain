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
    session = Session(
        refresh="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjZmY4ODdmMi02ZTA0LTQxNmUtOTc2NC03NjcyMTM3NDBmZGYiLCJuYmYiOjE1MjM0NzQ0ODQsImV4cCI6MTUyNjA2NjQ4NCwiaWF0IjoxNTIzNDc0NDg0LCJpZGVudGl0eSI6eyJ1c2VyX2lkIjo0OX0sInR5cGUiOiJyZWZyZXNoIn0.agwsag5AVUfx_gCKTzgRCs-RtCQua6LwZmO4T5REfqY",
        session="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzMzZiOTc2Yi1lNTQ1LTQwNzctOTNhMS03MTJlNTQyNWQ5OTYiLCJuYmYiOjE1MjM0NzQ0ODQsImV4cCI6MTUyMzQ3NTM4NCwiaWF0IjoxNTIzNDc0NDg0LCJpZGVudGl0eSI6eyJ1c2VyX2lkIjo0OX0sInR5cGUiOiJhY2Nlc3MiLCJmcmVzaCI6ZmFsc2V9.vmd7C-acgvyWEEOYAt9rmbRqkQetQF9EsMq9cp8irFw"
    )

    response = API.updateUser('TestUser1', session=session).subscribe(on_next=lambda response: {
        pprint(response)
    })

