from wtforms import Form
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo

class ResetPasswordForm(Form):

	password = PasswordField("Password", [ EqualTo("confirm") ])
	confirm = PasswordField("Confirm Password")
