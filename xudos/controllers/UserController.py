from flask import abort
from flask import Blueprint
from flask import current_app as app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from xudos.decorators.AdminRequired import adminRequired
from xudos.decorators.LoginRequired import loginRequired
from xudos.forms.ProfileForm import ProfileForm
from xudos.forms.UserForm import UserForm
from xudos.services.UserService import UserService
from xudos.utils import util

userController = Blueprint("userController", __name__)

userService = UserService()

@userController.route("/users", methods = ["GET"])
@adminRequired()
def index():
	users = userService.select()
	return render_template("users/index.html", users = users)

@userController.route("/users/new", methods = ["GET"])
@adminRequired()
def new():
	form = UserForm(request.form)
	return render_template("users/new.html", form = form)

@userController.route("/users", methods = ["POST"])
@adminRequired("userController.new")
def create():
	form = UserForm(request.form)

	if form.validate():
		user = userService.create(form)
		flash("User '{}' has been successfully created.".format(user.name), "success")
		return redirect(url_for("userController.index"))
	else:
		return render_template("users/new.html", form = form), 400

@userController.route("/users/<int:id>/edit", methods = ["GET"])
@adminRequired("userController.index")
def edit(id):
	user = userService.selectById(id)

	if user == None:
		abort(404)

	form = UserForm(obj = user)
	return render_template("users/edit.html", user = user, form = form)

@userController.route("/users/<int:id>", methods = ["POST"])
@adminRequired("userController.index")
def update(id):
	user = userService.selectById(id)

	if user == None:
		abort(404)

	form = UserForm(request.form)

	form.setUserId(user.id)

	if form.validate():
		user = userService.update(id, form)
		flash("User '{}' has been successfully updated.".format(user.name), "success")
		return redirect(url_for("userController.index"))
	else:
		return render_template("users/edit.html", user = user, form = form), 400

@userController.route("/users/<int:id>/delete", methods = ["POST"])
@adminRequired("userController.index")
def delete(id):
	user = userService.selectById(id)

	if user.id == current_user.id:
		abort(400)

	if user == None:
		abort(404)

	userService.delete(user)

	flash("The user '{}' has been successfully deleted.".format(user.name), "success")
	return redirect(url_for("userController.index"))

@userController.route("/profile", methods = ["GET"])
@loginRequired()
def profile():
	user = userService.selectById(current_user.id)
	return render_template("users/profile.html", user = user)

@userController.route("/profile/edit", methods = ["GET"])
@loginRequired()
def editProfile():
	user = userService.selectById(current_user.id)
	form = ProfileForm(obj = user)
	return render_template("users/profile-form.html", form = form)

@userController.route("/profile", methods = ["POST"])
@loginRequired("userController.editProfile")
def updateProfile():
	user = userService.selectById(current_user.id)
	form = ProfileForm(request.form)

	if form.validate():
		user = userService.updateProfile(user.id, form)
		flash("Your profile has been successfully updated.", "success")
		return redirect(url_for("userController.profile"))
	else:
		return render_template("users/profile-form.html", form = form), 400
