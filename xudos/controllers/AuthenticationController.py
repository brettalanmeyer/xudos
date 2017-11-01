from flask import Blueprint
from flask import current_app as app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from xudos.app import login_manager
from xudos.forms.ForgotPasswordForm import ForgotPasswordForm
from xudos.forms.LoginForm import LoginForm
from xudos.forms.ResetPasswordForm import ResetPasswordForm
from xudos.services.UserService import UserService
from xudos.utils import util

authenticationController = Blueprint("authenticationController", __name__)

userService = UserService()

@authenticationController.route("/login", methods = ["GET"])
def index():
	form = LoginForm(request.form)
	form.next.data = next = util.param("next", "")
	return render_template("authentication/form.html", form = form)

@authenticationController.route("/login", methods = ["POST"])
def login():
	form = LoginForm(request.form)

	if form.validate():
		user = userService.authenticate(form)

		if user != None:
			login_user(user)
			flash("Welcome {}.".format(user.name), "success")
			next = util.paramForm("next", "/")
			return redirect(next)

		flash("Incorrect email or password.", "danger")

	return render_template("authentication/form.html", form = form), 401

@authenticationController.route("/logout", methods = ["GET"])
def logout():
	if current_user.is_authenticated:
		logout_user()
		flash("You've been logged out.", "success")

	return redirect(url_for("authenticationController.login"))

@login_manager.user_loader
def load_user(id):
	return userService.selectById(id)

@authenticationController.route("/forgot-password", methods = ["GET"])
def forgotPassword():
	form = ForgotPasswordForm()
	return render_template("authentication/forgot-password.html", form = form)

@authenticationController.route("/forgot-password", methods = ["POST"])
def sendForgotPassword():
	form = ForgotPasswordForm(request.form)

	if form.validate():
		user = userService.selectByEmail(form.email.data)

		if user is not None:
			token = userService.passwordResetToken(user)
			subject = "Xudos Password Reset"
			html = render_template("authentication/password-reset-email.html").format(user.name, request.url_root, token)
			util.sendMail(user.email, subject, html)

		return render_template("authentication/forgot-password-confirm.html")

	else:
		return render_template("authentication/forgot-password.html", form = form), 400

@authenticationController.route("/reset-password/<path:token>", methods = ["GET"])
def resetPassword(token):
	user = userService.selectByToken(token)

	if user is None:
		flash("The reset password token is invalid.", "danger")
		return redirect(url_for("authenticationController.forgotPassword"))

	form = ResetPasswordForm(request.form)
	return render_template("authentication/reset-password.html", token = token, form = form)


@authenticationController.route("/reset-password/<path:token>", methods = ["POST"])
def doResetPassword(token):
	user = userService.selectByToken(token)

	if user is None:
		flash("The reset password token is invalid.", "danger")
		return redirect(url_for("authenticationController.forgotPassword"))

	form = ResetPasswordForm(request.form)

	if form.validate():
		userService.updatePassword(user, form.password.data)
		flash("Your password has been successfully reset.", "success")
		return redirect(url_for("authenticationController.login"))

	else:
		return render_template("users/reset-password.html", token = token, form = form), 400
