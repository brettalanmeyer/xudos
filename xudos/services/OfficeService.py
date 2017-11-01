from datetime import datetime
from flask import current_app as app
from xudos.models.OfficeModel import OfficeModel
from xudos.utils import database as db

class OfficeService():

	def select(self):
		return db.session.query(OfficeModel).order_by(OfficeModel.city)

	def selectById(self, id):
		app.logger.info("Selecting office by id=%d", id)
		offices = db.session.query(OfficeModel).filter(OfficeModel.id == id)

		if offices.count() == 0:
			return None

		return offices.one()

	def create(self, form):
		app.logger.info("Creating office city=%s, state=%s", form.city.data, form.state.data)
		office = OfficeModel(form.city.data, form.state.data)
		db.session.add(office)
		db.session.commit()

		return office

	def update(self, id, form):
		app.logger.info("Updating office id=%d, city=%s, state=%s", id, form.city.data, form.state.data)
		office = self.selectById(id)
		office.city = form.city.data
		office.state = form.state.data
		office.modifiedAt = datetime.now()
		db.session.commit()

		return office

	def delete(self, office):
		app.logger.info("Deleting office id=%d", office.id)
		db.session.delete(office)
		db.session.commit()
