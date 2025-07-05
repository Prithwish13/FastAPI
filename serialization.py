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
    gender: str = 'Male'
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


temp = patient1.model_dump(exclude_unset=True, exclude={ 'address': ['zip_code']})

json_temp = patient1.model_dump_json()

print(temp)
print(type(temp))
print(json_temp)
print(type(json_temp))