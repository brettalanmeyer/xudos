from datetime import datetime
from sqlalchemy import Table, Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from xudos.utils.database import Base

class XudoModel(Base):

	__tablename__ = "xudos"

	id = Column(Integer, primary_key = True)
	text = Column(String)
	image = Column(String)
	submittedBy = Column(String)
	accepted = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	offices = relationship("OfficeModel", secondary = Table("xudos_offices", Base.metadata,
		Column("xudoId", Integer, ForeignKey("xudos.id"), primary_key = True),
		Column("officeId", Integer, ForeignKey("offices.id"), primary_key = True)
	))

	def __init__(self, offices, text, image, submittedBy):
		self.offices = offices
		self.text = text
		self.image = image
		self.submittedBy = submittedBy
		self.accepted = None
		self.createdAt = datetime.now()
		self.modifiedAt = datetime.now()

	def dateFormatted(self):
		return "{:%b %d, %Y %I:%M%P}".format(self.createdAt)

	def isAccepted(self):
		return self.accepted == 1

	def isRejected(self):
		return self.accepted == 0
