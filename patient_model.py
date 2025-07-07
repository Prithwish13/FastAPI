from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

class Patient(BaseModel):
    name: Annotated[ str, Field(..., min_length=2, max_length=50, description="The name of the patient")]
    age: Annotated[int, Field(..., gt=0, description="The age of the patient in years")]
    city: Annotated[str, Field(..., min_length=2, max_length=50, description="The city where the patient resides")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., min_length=1, max_length=10, description="gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient in kilograms")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        
class PatientUpdate(BaseModel):
    name: Annotated[ Optional[str], Field(default=None, min_length=2, max_length=50, description="The name of the patient")]
    age: Annotated[Optional[int], Field(default=None, gt=0, description="The age of the patient in years")]
    city: Annotated[Optional[str], Field(default=None, min_length=2, max_length=50, description="The city where the patient resides")]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None, min_length=1, max_length=10, description="gender of the patient")]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="The height of the patient in meters")]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description="The weight of the patient in kilograms")]
    