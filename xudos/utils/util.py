from flask import current_app as app
from flask import request
from flask_mail import Mail
from flask_mail import Message
from xudos.app import app as context
from xudos.decorators.Async import async
import hashlib
import os
import uuid

def param(name, default = None, paramType = None):
	value = request.args.get(name)

	if value == None:
		value = default

	if value != None and paramType != None:
		try:
			if paramType == "int":
				value = int(value)
			elif paramType == "str":
				value = str(value)
		except:
			return None

	return value

def paramForm(name, default = None, paramType = None):
	value = None

	if name in request.form:
		value = request.form[name]

	if value == None:
		value = default

	if value != None and paramType != None:
		if paramType == "int":
			value = int(value)
		elif paramType == "str":
			value = str(value)
		elif paramType == "bool":
			value = value in ("True", "true")

	return value

def hash(string):
	return hashlib.sha224(string).hexdigest()

def generateUUID():
	return str(uuid.uuid4())

def sendMail(to, subject, html):
	sender = (app.config["MAIL_FROM_NAME"], app.config["MAIL_FROM_EMAIL"])

	recipients = [to]

	mail = Mail(app)
	messages = Message(subject, sender = sender, recipients = recipients)
	messages.html = html
	messages.body = html

	if app.config["MAIL_ENABLED"]:
		app.logger.info("Mail Enabled, Sending Mail")
		sendMailAsync(mail, messages)

@async
def sendMailAsync(mail, messages):
	with context.app_context():
		mail.send(messages)

def uploadFile(files, fieldName, existingImage = None):
	uploadDirectory = "{}/static/uploads/{}".format(app.root_path ,"{}")

	if fieldName in files:

		file = files[fieldName]

		if len(file.filename) != 0:
			extension = file.filename.split(".")[-1]
			fileName = "{}.{}".format(str(uuid.uuid4()), extension)
			file.save(uploadDirectory.format(fileName))

			if existingImage != None:
				existingImagePath = uploadDirectory.format(existingImage)
				if os.path.isfile(existingImagePath):
					os.remove(existingImagePath)

			return True, fileName

	return False, None

def deleteFile(fileName):
	path = "{}/static/uploads/{}".format(app.root_path, fileName)

	if os.path.isfile(path):
		os.remove(path)

