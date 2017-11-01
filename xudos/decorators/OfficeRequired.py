from flask import redirect
from flask import session
from flask import url_for
from functools import update_wrapper

def officeRequired(endpoint = None):
	def decorator(fn):
		def wrapped_function(*args, **kwargs):

			if "office" not in session:
				return redirect(url_for("officeController.select"))

			return fn(*args, **kwargs)

		return update_wrapper(wrapped_function, fn)
	return decorator
