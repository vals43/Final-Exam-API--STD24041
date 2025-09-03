from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class Characteristic(BaseModel):
    ram_memory: int
    rom_memory: int

class Phone(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic


phones_db: Dict[str, Phone] = {}


@app.get("/health")
def health():
    return "Ok"


@app.post("/phones", status_code=201)
def create_phone(phone: Phone):
    if phone.identifier in phones_db:
        raise HTTPException(status_code=400, message=f"Un phone avec cette ID :{id} existe deja")
    phones_db[phone.identifier] = phone
    return phone


@app.get("/phones", response_model=List[Phone])
def get_phones():
    return list(phones_db.values())


@app.get("/phones/{id}", response_model=Phone)
def get_phone(id: str):
    if id not in phones_db:
        raise HTTPException(status_code=404, message=f"Le phone  avec l'Id {id} n'existe pas ou n'as pas été trouvé")
    return phones_db[id]


@app.put("/phones/{id}/characteristics", response_model=Phone)
def update_characteristics(id: str, new_characteristics: Characteristic):
    if id not in phones_db:
        raise HTTPException(status_code=404, message=f"Le phone  avec l'Id {id} n'existe pas ou n'as pas été trouvé")

    phone = phones_db[id]
    phone.characteristics = new_characteristics
    phones_db[id] = phone
    return phone
