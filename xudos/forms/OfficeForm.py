from wtforms import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class OfficeForm(Form):

	city = StringField("City", [ DataRequired(), Length(max = 255) ])
	state = StringField("State", [ DataRequired(), Length(max = 255) ])
