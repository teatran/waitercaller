"""We need to create a User class that can work with flask_login.
We will have some methods that look redundant.
"""


class User:
    def __init__(self, email):
        self.email = email

    def get_id(self):
        '''This method is required. And returns a unique identifier.
        '''
        return self.email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        '''We only create User object when right username and password
        are entered. So this method returns True.
        '''
        return True
    
