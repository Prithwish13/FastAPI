from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from patient_model import Patient, PatientUpdate

app = FastAPI()

def load_data():
    with open("patients.json", "r") as file:
        import json
        return json.load(file)
    
def save_data(data):
    with open("patients.json", "w") as file:
        import json
        json.dump(data, file)

@app.get("/")
def hello_world():
    return {"message": "Patient management system api"}

@app.get("/about")
def about():
    return {"message": "A fully functional patient management system API built with FastAPI."}


@app.get("/patients")
def get_patients(sortBy: str  = Query(..., description="sort on the basis of age, bmi, height & weight", example="height"), 
                 sortOrder: str = Query(default='asc', description="sort in ascending or descending order", example="asc")):
    
    valid_sort_fields = ['age', 'bmi', 'height', 'weight']
    
    if sortBy not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_sort_fields)}")
    if sortOrder not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order. Use 'asc' or 'desc'.")
    data = load_data()  
    
    sort_order = True if sortOrder != 'asc' else False
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sortBy, 0), reverse = sort_order)
    
    return sorted_data

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()
    patient_details = data.get(patient_id)
    if not patient_details:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_details


@app.post("/patients")
def create_patient(patient: Patient):
    data = load_data()
    patient_keys = list(data.keys())[-1] if data else None
    if patient_keys:
        next_id = int(patient_keys[1:]) + 1
    else:
        next_id = 1
    patient_id = f"P{next_id:03d}"
    

    bmi = patient.bmi
    
    data[patient_id] = {**patient.model_dump()}
    
    save_data(data)
    
    return JSONResponse(
        status_code=201,
        content={
            "message": "Patient created successfully",
            "patient_id": patient_id,
            "bmi": bmi,
            "verdict": patient.verdict
        }
    )
@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient: PatientUpdate):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_patient = patient.model_dump(exclude_unset=True)
    existing_patient = data[patient_id]
    
    for key, value in update_patient.items():
        existing_patient[key] = value
            
    data[patient_id] = Patient(**existing_patient).model_dump()
    save_data(data)
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient updated successfully",
            **data[patient_id],
        }
    )
    
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    save_data(data)
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient deleted successfully",
            "patient_id": patient_id
        }
    )