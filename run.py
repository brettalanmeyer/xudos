from xudos.app import app
import sys

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding("UTF8")
	app.run(host = app.config["HOST"], port = app.config["PORT"], debug = app.config["DEBUG"])
