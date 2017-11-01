from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from xudos.utils.database import Base

class OfficeModel(Base):

	__tablename__ = "offices"

	id = Column(Integer, primary_key = True)
	city = Column(String)
	state = Column(String)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	users = relationship("UserModel")

	def __init__(self, city, state):
		self.city = city
		self.state = state
		self.createdAt = datetime.now()
		self.modifiedAt = datetime.now()

	def name(self):
		return "{}, {}".format(self.city, self.state)
