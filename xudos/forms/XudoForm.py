from flask import current_app as app
from wtforms import FileField
from wtforms import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.widgets import CheckboxInput
from wtforms.widgets import ListWidget
from xudos.services.OfficeService import OfficeService
from xudos.utils import util
import uuid

officeService = OfficeService()

class XudoForm(Form):

	text = TextAreaField("Text", [ DataRequired() ])
	submittedBy = StringField("Your Name", [ DataRequired(), Length(max = 255) ])
	image = FileField("Image")
	offices = QuerySelectMultipleField(
		"Offices",
		[ DataRequired() ],
		get_label = lambda office: office.name(),
		query_factory = officeService.select,
		option_widget = CheckboxInput(),
		widget = ListWidget(prefix_label = False)
	)
