from pydantic import BaseModel, Field
from typing import Optional, List

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: str
    email: Optional[str] = None
    age: int
    address: Address
    
    
patient1 = Patient(
    name="John Doe",
    email="dey@gmail.com",
    age=30, address=Address(
        street="123 Main St",
        city="Anytown",
        state="CA",
        zip_code="12345"
    ))

def insert_patient(patient: Patient):
    # Simulate inserting patient into a database
    print(f"Inserting patient: {patient.name}, Age: {patient.age}, Address: {patient.address.city}") 
    
insert_patient(patient1)