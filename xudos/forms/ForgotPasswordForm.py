from wtforms import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class ForgotPasswordForm(Form):

	email = StringField("Email", [ DataRequired() ])
