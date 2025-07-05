from pydantic import BaseModel, Field, EmailStr, AnyUrl, field_validator
from typing import List, Dict, Optional, Annotated

patient_info = {
    "name": "John Doe",
    "age": '30',
    "email": "deyabir30@hdfc.com",
    "weight": 70.5,
    "married": True,
    "allergies": ["penicillin", "nuts"],
    "linked_in": "https://www.linkedin.com/in/prithwish-dey-1a0b2a1b3/",
    "contact_details": {
        "phone": "123-456-7890",
        "address": "123 Main St, Anytown, USA" 
    }
}


class Patient(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50, title="name of the patient", description="The name of the patient, must be between 1 and 100 characters", example="John Doe")]
    age: int = Field(..., ge=0, description="The age of the patient, must be a non-negative integer")
    email: Optional[EmailStr] = Field(None, description="The email address of the patient")
    linked_in: Optional[AnyUrl] = Field(None, description="The LinkedIn profile of the patient")
    weight: float = Annotated[float, Field(gt=0, strict=True, description="The weight of the patient in kilograms, must be greater than 0")]
    married: Annotated[bool, Field(default=False, description="Indicates if the patient is married, default is False")]
    allergies: List[str] = Field(default_factory=list, max_length=5, description="List of allergies the patient has, default is an empty list")
    contact_details: Dict[str, str]
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        valid_domains = ['hdfc.com', 'icici.com', 'axis.com', 'sbi.com']
        domain_name=  v.split('@')[-1] if v else ''
        if domain_name not in valid_domains:
            raise ValueError('Email must end with @example.com')
        return v
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, v):
        return v.upper()
    
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError('Age must be between 0 and 120')
        return v
    
patient_1 = Patient(**patient_info)

def insert_patient(patient: Patient):
    # Simulate inserting patient into a database
    print(f"Inserting patient: {patient}, Age: {patient.age}")  
    
insert_patient(patient_1)