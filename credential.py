import os

class CredentialProvider:
    """Class providing trello api credentials"""

    def __init__(self):
        self.access_key = os.getenv('access_key')
        self.token = os.getenv('token')

    def get_access_key(self):
        return self.access_key

    def get_token(self):
        return self.token
