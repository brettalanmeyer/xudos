from flask import Flask
from flask_assets import Bundle
from flask_assets import Environment
from flask_login import LoginManager
from flask_session import Session
from xudos.utils import assets
from xudos.utils import logger

app = Flask(__name__)
app.config.from_pyfile("../config.cfg")

logger.setupLogging(app)
assets.setupAssets(app)

login_manager = LoginManager()
login_manager.init_app(app)

sess = Session()
sess.init_app(app)

app.url_map.strict_slashes = False

from xudos.controllers.AuthenticationController import authenticationController
from xudos.controllers.ErrorController import errorController
from xudos.controllers.MainController import mainController
from xudos.controllers.OfficeController import officeController
from xudos.controllers.UserController import userController
from xudos.controllers.XudoController import xudoController

app.register_blueprint(authenticationController)
app.register_blueprint(errorController)
app.register_blueprint(mainController)
app.register_blueprint(officeController)
app.register_blueprint(userController)
app.register_blueprint(xudoController)
