from flask import *
from flaskext.login import *

class User(UserMixin):
    def __init__(self, id, username="Lady Gaga", active=True, anonymous=False):
        self.id = id # is username
        self.active = active
        self.anonymous = anonymous   
        self.check_rep()
    
    def is_authenticated(self):
        return True   
 
    def get_password(self):
        return self.password

    def check_rep(self):
        pass  
   
