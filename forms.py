from flaskext.wtf import Form, TextField, PasswordField 

class RegistrationForm(Form):
    username = TextField('Username')
    password = PasswordField('New Password')

class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')

class GameForm(Form):
    out = TextField() 
    inp = TextField() 

