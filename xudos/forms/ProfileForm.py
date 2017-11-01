from wtforms import Form
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Length
from xudos.services.OfficeService import OfficeService

class ProfileForm(Form):

	name = StringField("Name", [ DataRequired(), Length(max = 255) ])
	email = StringField("Email", [ DataRequired(), Length(max = 255) ])
	password = PasswordField("Password", [ EqualTo("confirm") ])
	confirm = PasswordField("Confirm Password")
