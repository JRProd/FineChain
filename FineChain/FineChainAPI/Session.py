# Session class to help session persistance
class Session():
    session_token = ''
    refresh_token = ''

    # Created with a session and refresh token
    def __init__(self, session=None, refresh=None):
        self.session_token = session
        self.refresh_token = refresh

    def setSessionToken(self, session):
        self.session_token = session

    def setRefreshToken(self, refresh):
        self.refresh_token = refresh

    def getSessionToken(self):
        return self.session_token

    def getRefreshToekn(self):
        return self.refresh_token

    def updateSession(self, token):
        self.session_token = token
