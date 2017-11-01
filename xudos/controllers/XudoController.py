from flask import abort
from flask import Blueprint
from flask import current_app as app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_login import current_user
from xudos.decorators.LoginRequired import loginRequired
from xudos.decorators.OfficeRequired import officeRequired
from xudos.forms.XudoForm import XudoForm
from xudos.services.UserService import UserService
from xudos.services.XudoService import XudoService
from xudos.utils import util

xudoController = Blueprint("xudoController", __name__)

xudoService = XudoService()
userService = UserService()

@xudoController.route("/", methods = ["GET"])
@officeRequired()
def slideshow():
	xudos = xudoService.selectAcceptedByOffice(session["office"])
	return render_template("xudos/slideshow.html", xudos = xudos, delay = app.config["SLIDESHOW_DELAY"])

@xudoController.route("/xudos", methods = ["GET"])
@loginRequired("xudoController.index")
def index():
	if current_user.is_admin():
		xudos = xudoService.select()
	else:
		xudos = xudoService.selectByOffice(current_user.office)

	page = util.param("page", 1, "int")
	pagedXudos = xudoService.paged(xudos, page, 20)

	return render_template("xudos/index.html", xudos = pagedXudos["records"], paging = pagedXudos)

@xudoController.route("/xudos/<int:id>", methods = ["GET"])
@loginRequired("xudoController.index")
def show(id):
	xudo = xudoService.selectById(id)

	if xudo == None:
		abort(404)

	return render_template("xudos/show.html", xudo = xudo)

@xudoController.route("/xudos/new", methods = ["GET"])
def new():
	form = XudoForm(request.form)
	return render_template("xudos/new.html", form = form)

@xudoController.route("/xudos", methods = ["POST"])
def create():
	form = XudoForm(request.form)

	if form.validate():

		uploaded, fileName = util.uploadFile(request.files, "image")
		form.image.data = fileName if uploaded else None

		xudo = xudoService.create(form)

		flash("Xudo has been successfully created.", "success")

		sendNotifications(xudo)

		if current_user.is_authenticated:
			return redirect(url_for("xudoController.index"))
		else:
			return redirect(url_for("xudoController.slideshow"))
	else:
		return render_template("xudos/new.html", form = form), 400

@xudoController.route("/xudos/<int:id>/edit", methods = ["GET"])
@loginRequired("xudoController.index")
def edit(id):
	xudo = xudoService.selectById(id)

	if xudo == None:
		abort(404)

	form = XudoForm(obj = xudo)

	return render_template("xudos/edit.html", xudo = xudo, form = form)

@xudoController.route("/xudos/<int:id>", methods = ["POST"])
@loginRequired("xudoController.index")
def update(id):
	xudo = xudoService.selectById(id)

	if xudo == None:
		abort(404)

	form = XudoForm(request.form)

	if form.validate():
		uploaded, fileName = util.uploadFile(request.files, "image", xudo.image)
		form.image.data = fileName if uploaded else None

		xudo = xudoService.update(id, form)
		flash("Xudo has been successfully updated.", "success")
		return redirect(url_for("xudoController.index"))
	else:
		return render_template("xudos/edit.html", xudo = xudo, form = form), 400

@xudoController.route("/xudos/<int:id>/accept", methods = ["POST"])
@loginRequired("xudoController.index")
def accept(id):
	xudo = xudoService.selectById(id)

	if xudo == None:
		abort(404)

	xudoService.accept(xudo)

	flash("Xudo has been accepted.", "success")

	return redirect(url_for("xudoController.index"))

@xudoController.route("/xudos/<int:id>/reject", methods = ["POST"])
@loginRequired("xudoController.index")
def reject(id):
	xudo = xudoService.selectById(id)

	if xudo == None:
		abort(404)

	xudoService.reject(xudo)

	flash("Xudo has been rejected.", "success")

	return redirect(url_for("xudoController.index"))

@xudoController.route("/xudos/<int:id>/delete", methods = ["POST"])
@loginRequired("xudoController.index")
def delete(id):
	xudo = xudoService.selectById(id)

	if xudo == None:
		abort(404)

	xudoService.delete(xudo)

	flash("Xudo has been successfully deleted.", "success")
	return redirect(url_for("xudoController.index"))

def sendNotifications(xudo):
	for office in xudo.offices:
		for user in office.users:
			subject = "Xudos for Approval"
			html = render_template("xudos/submitted-email.html").format(user.name, xudo.submittedBy, xudo.createdAt, request.url_root, xudo.id)
			util.sendMail(user.email, subject, html)
