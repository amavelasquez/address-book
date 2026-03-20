from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List

from db.db_connection import engine, Base, get_db, Session
from models.addressModel import Address, AddressCreate, AddressResponse
from utils.validateCoords import validate_x_coord, validate_y_coord

app = FastAPI()

Base.metadata.create_all(engine)

get_db()

@app.get("/")
def root():
    return{"messge" : "Hello World!"}

#Get address given coordinates
@app.get("/address/", response_model=AddressResponse)
def get_address(x_coord: float = Query(...), y_coord: float = Query(...), db: Session = Depends(get_db)):
    queried_address = db.query(Address).filter(Address.x_coordinate == x_coord, Address.y_coordinate == y_coord).first()
    if not queried_address:
        raise HTTPException(status_code=404, detail="Address does not exist!")
    return queried_address

#Create address
@app.post("/address/", response_model=AddressResponse)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    if db.query(Address).filter(Address.x_coordinate == address.x_coordinate, Address.y_coordinate == address.y_coordinate).first():
        raise HTTPException(status_code=400, detail="Address already exists!")
    
    if validate_x_coord(address.x_coordinate) and validate_y_coord(address.y_coordinate):
        raise HTTPException(status_code=400, detail="Invalid input, X coordinate should be between -180 and 180, and Y coordinate should be between -90 and 90")
    
    new_address = Address(**address.model_dump())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

#Update address
@app.put("/address/{address_id}", response_model=AddressResponse)
def update_address(address_id:int, address:AddressCreate, db: Session = Depends(get_db)):
    queried_address = db.query(Address).filter(Address.id == address_id).first()
    if not queried_address:
        raise HTTPException(status_code=404, detail="Address does not exist!")
    
    for field, value in address.model_dump().items():
        setattr(queried_address, field, value)

    db.add(queried_address)
    db.commit()
    db.refresh(queried_address)
    return queried_address

#Delete address
@app.delete("/address/{address_id}")
def delete_user(address_id:int, db: Session = Depends(get_db)):
    queried_address = db.query(Address).filter(Address.id == address_id).first()
    if not queried_address:
        raise HTTPException(status_code=404, detail="Address does not exist!")
    
    db.delete(queried_address)
    db.commit()
    return {"message":"Address Deleted"}