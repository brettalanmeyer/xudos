from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from xudos.utils.database import Base

class UserModel(Base):

	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	officeId = Column(Integer, ForeignKey("offices.id"))
	name = Column(String)
	email = Column(String, unique = True)
	password = Column(String)
	token = Column(String)
	isAdmin = Column(String)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	office = relationship("OfficeModel")

	def __init__(self, officeId, name, email, password, isAdmin):
		self.officeId = officeId
		self.name = name
		self.email = email
		self.password = password
		self.token = None
		self.isAdmin = isAdmin
		self.createdAt = datetime.now()
		self.modifiedAt = datetime.now()

	def is_admin(self):
		return self.isAdmin == 1

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id
