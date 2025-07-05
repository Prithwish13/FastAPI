from pydantic import BaseModel, Field, EmailStr, AnyUrl, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str] 
    contact_details: Dict[str, str]
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age and 'emergency_contact' not in model.contact_details:
            raise ValueError("Emergency contact is required for patients under 18")
        return model    
    
    
patient_1 = Patient(
    name="John Doe",
    email="abc@gamil.com",
    age=30,
    weight=70.5,
    married=True,
    allergies=["penicillin", "nuts"],
    contact_details={
        "phone": "123-456-7890",
        "address": "123 Main St, Anytown, USA",
        "emergency_contact": "8546778513"
    }
    
)

def insert_patient(patient: Patient):
    # Simulate inserting patient into a database
    print(f"Inserting patient: {patient}, Age: {patient.age}")  
    
insert_patient(patient_1)