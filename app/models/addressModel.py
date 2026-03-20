from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from db.db_connection import Base

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    address_name = Column(String(999), nullable=False)
    x_coordinate = Column(Float, nullable=False, unique=True)
    y_coordinate = Column(Float, nullable=False, unique=True)

class AddressCreate(BaseModel):
    address_name: str
    x_coordinate: float
    y_coordinate: float

class AddressResponse(BaseModel):
    id: int
    address_name: str
    x_coordinate: float
    y_coordinate: float

    class Config:
        from_attributes = True