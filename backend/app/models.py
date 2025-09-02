from sqlalchemy import Column, String, Boolean, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VendingLocation(Base):
    __tablename__ = "vending_locations"

    id = Column(String(50), primary_key=True, index=True)
    retailer = Column(String(100))
    machine_id = Column(String(50))
    name = Column(String(100))
    address = Column(String(200))
    city = Column(String(100))
    state = Column(String(10))
    zip_code = Column(String(20))
    latitude = Column(Numeric(10, 8))    
    longitude = Column(Numeric(11, 8)) 
    type = Column(String(50))
    last_verified = Column(Date)
    is_active = Column(Boolean)
