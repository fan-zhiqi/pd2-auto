from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class CPLLocation(Base):
    __tablename__ = 'cpl_location'
    complex_uuid = Column(String, primary_key=True)
    device_uuid = Column(String, primary_key=True)
    cpl_uuid = Column(String, primary_key=True)
    can_delete = Column(Boolean)
    cpl_actual_size = Column(Integer)
    cpl_size = Column(Integer)
    deleting = Column(Boolean)