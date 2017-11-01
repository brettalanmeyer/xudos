from wtforms import Form
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import ValidationError
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Length
from xudos.services.OfficeService import OfficeService
from xudos.services.UserService import UserService

officeService = OfficeService()
userService = UserService()

class UserForm(Form):

	userId = None
	name = StringField("Name", [ DataRequired(), Length(max = 255) ])
	email = StringField("Email", [ DataRequired(), Length(max = 255) ])
	password = PasswordField("Password", [ EqualTo("confirm") ])
	confirm = PasswordField("Confirm Password")
	isAdmin = SelectField("Admin", [ DataRequired() ], choices = [("1", "Yes"), ("0", "No")], default = 0)

	offices = [(str(office.id), office.name()) for office in officeService.select()]
	officeId = SelectField("Office", [ DataRequired() ], choices = offices)

	def setUserId(self, userId):
		self.userId = userId

	def validate_email(form, field):
		user = userService.selectByEmail(field.data)

		if user != None and form.userId != user.id:
			raise ValidationError("The email address specified is already in use.")
