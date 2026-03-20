from fastapi import FastAPI, HTTPException, Depends
from typing import Optional, List

from db.db_connection import engine, SessionLocal, Base, get_db, Session
from models.addressModel import Address, AddressCreate, AddressResponse

app = FastAPI()

Base.metadata.create_all(engine)

get_db()

@app.get("/")
def root():
    return{"messge" : "Hello World!"}

@app.get("/address/{address_id}", response_model=AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)):
    queried_address = db.query(Address).filter(Address.id == address_id).first()
    if not queried_address:
        raise HTTPException(status_code=404, detail="User not found!")
    return queried_address

@app.post("/address/", response_model=AddressResponse)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    if db.query(Address).filter(Address.x_coordinate == address.x_coordinate).first():
        raise HTTPException(status_code=400, detail="Address already exists!")
    
    new_address = Address(**address.model_dump())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address