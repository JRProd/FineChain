class Session():
    session_token = ''
    refresh_token = ''

    def __init__(self, session, refresh):
        self.session_token = session
        self.refresh_token = refresh

    def getSessionToken(self):
        return self.session_token

    def getRefreshToekn(self):
        return self.refresh_token

    def updateSession(self, token):
        self.session_token = token