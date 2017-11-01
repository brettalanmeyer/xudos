from flask import Blueprint
from flask import current_app as app
from flask import request
from xudos.utils import database as db

mainController = Blueprint("mainController", __name__)

@mainController.after_app_request
def afterRequest(response):
	db.session.close()
	return response

@mainController.before_app_request
def beforeRequest():
	app.logger.access("%s \"%s %s\"", request.remote_addr, request.environ["REQUEST_METHOD"], request.url)
