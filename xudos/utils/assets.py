from flask_assets import Environment
from flask_assets import Bundle

def setupAssets(app):
	assets = Environment(app)
	assets.init_app(app)
	assets.register("js_all", bundleJavascripts())
	assets.register("css_all", bundleStylesheets())

def bundleJavascripts():
	return Bundle(
		"libraries/jquery/3.2.1/jquery.min.js",
		"libraries/popper.js/1.12.3/popper.min.js",
		"libraries/bootstrap/4.0.0.beta/js/bootstrap.min.js",
		"javascripts/app.js",
		filters = "jsmin",
		output = ".webassets-cache/xudos.min.js"
	)

def bundleStylesheets():
	return Bundle(
		"libraries/bootstrap/4.0.0.beta/css/bootstrap.min.css",
		"stylesheets/app.css",
		filters = "cssmin",
		output = ".webassets-cache/xudos.min.css"
	)
