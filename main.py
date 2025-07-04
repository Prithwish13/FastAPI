from fastapi import FastAPI, Path, HTTPException, Query

app = FastAPI()

def load_data():
    with open("patients.json", "r") as file:
        import json
        return json.load(file)

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