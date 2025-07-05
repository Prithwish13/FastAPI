from pydantic import BaseModel, Field, EmailStr, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    married: bool
    allergies: List[str] 
    contact_details: Dict[str, str]
    
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        if self.height <= 0:
            raise ValueError("Height must be greater than zero to calculate BMI")
        return round(self.weight / (self.height ** 2), 2)
    
patient_1 = Patient(
        name="John Doe",
        email="addd@gmail.com",
        age=30,
        weight=70.5,
        height=1.75,
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
    print(f"Inserting patient: {patient}, Age: {patient.age}, BMI: {patient.calculate_bmi}")    
    
    
insert_patient(patient_1)