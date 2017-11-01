from wtforms import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import HiddenField
from wtforms.validators import DataRequired

class LoginForm(Form):

	email = StringField("Email", [ DataRequired() ])
	password = PasswordField("Password", [ DataRequired() ])
	next = HiddenField ("next")
