from datetime import datetime
from flask import current_app as app
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from xudos.models.UserModel import UserModel
from xudos.utils import database as db
from xudos.utils import util

class UserService():

	def select(self):
		app.logger.info("Selecting users")
		return db.session.query(UserModel).order_by(UserModel.name)

	def selectById(self, id):
		app.logger.info("Selecting user by id=%d", id)
		users = db.session.query(UserModel).filter(UserModel.id == id)

		if users.count() == 0:
			return None

		return users.one()

	def selectByOffice(self, office):
		app.logger.info("Selecting user by office=%d", office.id)
		return db.session.query(UserModel).filter(UserModel.office == office)

	def selectByEmail(self, email):
		app.logger.info("Selecting user by email=%s", email)
		users = db.session.query(UserModel).filter(UserModel.email == email)

		if users.count() == 1:
			return users.one()

		return None

	def selectByToken(self, token):
		app.logger.info("Selecting user by token=%s", token)
		users = db.session.query(UserModel).filter(UserModel.token == token)

		if users.count() == 1:
			return users.one()

		return None

	def create(self, form):
		password = None
		if len(form.password.data) > 0:
			password = generate_password_hash(form.password.data)

		user = UserModel(form.officeId.data, form.name.data, form.email.data, password, form.isAdmin.data)
		db.session.add(user)
		db.session.commit()

		app.logger.info("Creating user officeId=%d, name=%s, email=%s, isAdmin=%d", user.officeId, user.name, user.email, user.is_admin())

		return user

	def update(self, id, form):
		user = self.selectById(id)
		user.officeId = form.officeId.data
		user.name = form.name.data
		user.email = form.email.data
		user.isAdmin = form.isAdmin.data

		if len(form.password.data) > 0:
			user.password = generate_password_hash(form.password.data)

		user.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating user id=%d, officeId=%d, name=%s, email=%s, isAdmin=%d", user.id, user.officeId, user.name, user.email, user.is_admin())

		return user

	def updateProfile(self, id, form):
		user = self.selectById(id)
		user.name = form.name.data
		user.email = form.email.data

		if len(form.password.data) > 0:
			user.password = generate_password_hash(form.password.data)

		user.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating user profile id=%d, name=%s, email=%s", user.id, user.name, user.email)

		return user

	def delete(self, user):
		app.logger.info("Deleting user id=%d", user.id)
		db.session.delete(user)
		db.session.commit()

	def authenticate(self, form):
		email = form.email.data
		password = form.password.data

		app.logger.info("Authenticating user email=%s", email)

		users = db.session.query(UserModel).filter(UserModel.email == email)

		if users.count() == 1:
			user = users.one()

			if user.password != None and check_password_hash(user.password, password):
				return user

		app.logger.info("Authentication failed for user email=%s", email)

		return None

	def passwordResetToken(self, user):
		app.logger.info("Generating reset token for userId=%d", user.id)

		user.token = util.generateUUID()
		user.modifiedAt = datetime.now()
		db.session.commit()

		return user.token

	def updatePassword(self, user, password):
		app.logger.info("Updating password for userId=%d", user.id)

		user.token = None
		user.password = generate_password_hash(password)
		user.modifiedAt = datetime.now()
		db.session.commit()

		return user.token
