from datetime import datetime
from flask import current_app as app
from xudos.models.XudoModel import XudoModel
from xudos.models.OfficeModel import OfficeModel
from xudos.services.OfficeService import OfficeService
from xudos.services.PagedService import PagedService
from xudos.utils import database as db
from xudos.utils import util
import os
import random

officeService = OfficeService()

class XudoService(PagedService):

	def select(self):
		app.logger.info("Selecting xudos")
		return db.session.query(XudoModel).order_by(XudoModel.createdAt.desc())

	def selectByOffice(self, office):
		app.logger.info("Selecting xudos by officeId=%d", office.id)
		return db.session.query(XudoModel).join(XudoModel.offices).filter(OfficeModel.id == office.id).order_by(XudoModel.createdAt)

	def selectAccepted(self):
		app.logger.info("Selecting approved xudos")
		return db.session.query(XudoModel).filter(XudoModel.accepted == True).order_by(XudoModel.createdAt)

	def selectAcceptedByOffice(self, office):
		app.logger.info("Selecting approved xudos by officeId=%d", office.id)
		return db.session.query(XudoModel).filter(XudoModel.accepted == True).join(XudoModel.offices).filter(OfficeModel.id == office.id).order_by(XudoModel.createdAt)

	def selectById(self, id):
		app.logger.info("Selecting xudo by id=%d", id)
		offices = db.session.query(XudoModel).filter(XudoModel.id == id)

		if offices.count() == 0:
			return None

		return offices.one()

	def create(self, form):
		xudo = XudoModel(form.offices.data, form.text.data, form.image.data, form.submittedBy.data)
		db.session.add(xudo)
		db.session.commit()

		app.logger.info("Creating xudo submittedBy=%s", xudo.submittedBy)

		return xudo

	def update(self, id, form):
		xudo = self.selectById(id)
		xudo.offices = form.offices.data
		xudo.text = form.text.data
		xudo.submittedBy = form.submittedBy.data

		if form.image.data != None:
			xudo.image = form.image.data

		xudo.modifiedAt = datetime.now()
		db.session.commit()

		app.logger.info("Updating xudo id=%d, submittedBy=%s", xudo.id, xudo.submittedBy)

		return xudo

	def accept(self, xudo):
		app.logger.info("Accepting xudo id=%d", xudo.id)

		xudo.accepted = True
		xudo.modifiedAt = datetime.now()
		db.session.commit()

		return xudo

	def reject(self, xudo):
		app.logger.info("Rejecting xudo id=%d", xudo.id)

		xudo.accepted = False
		xudo.modifiedAt = datetime.now()
		db.session.commit()

		return xudo

	def delete(self, xudo):
		app.logger.info("Deleting xudo id=%d", xudo.id)

		util.deleteFile(xudo.image)
		db.session.delete(xudo)
		db.session.commit()
