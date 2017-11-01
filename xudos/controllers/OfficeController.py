from flask import abort
from flask import Blueprint
from flask import current_app as app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from xudos.decorators.AdminRequired import adminRequired
from xudos.forms.OfficeForm import OfficeForm
from xudos.services.OfficeService import OfficeService
from xudos.utils import util

officeController = Blueprint("officeController", __name__)

officeService = OfficeService()

@officeController.route("/offices", methods = ["GET"])
@adminRequired()
def index():
	offices = officeService.select()
	return render_template("offices/index.html", offices = offices)

@officeController.route("/offices/new", methods = ["GET"])
@adminRequired()
def new():
	form = OfficeForm(request.form)
	return render_template("offices/new.html", form = form)

@officeController.route("/offices", methods = ["POST"])
@adminRequired("officeController.new")
def create():
	form = OfficeForm(request.form)

	if form.validate():
		office = officeService.create(form)
		flash("Office '{}' has been successfully created.".format(office.name()), "success")
		return redirect(url_for("officeController.index"))
	else:
		return render_template("offices/new.html", form = form), 400

@officeController.route("/offices/<int:id>/edit", methods = ["GET"])
@adminRequired("officeController.index")
def edit(id):
	office = officeService.selectById(id)

	if office == None:
		abort(404)

	form = OfficeForm(obj = office)
	return render_template("offices/edit.html", office = office, form = form)

@officeController.route("/offices/<int:id>", methods = ["POST"])
@adminRequired("officeController.index")
def update(id):
	office = officeService.selectById(id)

	if office == None:
		abort(404)

	form = OfficeForm(request.form)

	if form.validate():
		officeService.update(id, form)
		flash("Office '{}' has been successfully updated.".format(office.name()), "success")
		return redirect(url_for("officeController.index"))
	else:
		return render_template("offices/edit.html", office = office, form = form), 400

@officeController.route("/offices/<int:id>/delete", methods = ["POST"])
@adminRequired("officeController.index")
def delete(id):
	office = officeService.selectById(id)

	if office == None:
		abort(404)

	officeService.delete(office)
	flash("The office '{}' has been successfully deleted.".format(office.name()), "success")
	return redirect(url_for("officeController.index"))

@officeController.route("/offices/select", methods = ["GET", "POST"])
def select():
	if request.method == "POST":
		officeId = util.paramForm("officeId", None, "int")
		office = officeService.selectById(officeId)
		if office == None:
			flash("Please select a valid office.", "danger")
		else:
			session["office"] = office
			return redirect(url_for("xudoController.slideshow"))

	offices = officeService.select()
	return render_template("offices/select.html", offices = offices)
