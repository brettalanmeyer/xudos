from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import request

errorController = Blueprint("errorController", __name__)

@errorController.app_errorhandler(400)
@errorController.route("/errors/bad-request", methods = ["GET"])
def bad_request(error = None):
	return render_template("errors/400.html"), 400

@errorController.app_errorhandler(404)
@errorController.route("/errors/not-found", methods = ["GET"])
def not_found(error = None):
	return render_template("errors/404.html"), 404

@errorController.app_errorhandler(405)
@errorController.route("/errors/not-found", methods = ["GET"])
def method_not_allowed(error = None):
	return render_template("errors/404.html"), 405

@errorController.app_errorhandler(500)
@errorController.route("/errors/server-error", methods = ["GET"])
def server_error(error = None):
	return render_template("errors/500.html"), 500
