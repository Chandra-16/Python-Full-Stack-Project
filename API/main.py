from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
from typing import List, Optional

# --- Path Setup ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import db
from src.logic import TaskManager

# ----------------- APP SETUP --------------------- #
app = FastAPI(title="EnergyFlo API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# --- Pydantic Models ---
class HomeCreate(BaseModel):
    user_id: str
    address: str
    utility_provider: Optional[str] = None

class HomeUpdate(BaseModel):
    address: Optional[str] = None
    utility_provider: Optional[str] = None

class ApplianceCreate(BaseModel):
    home_id: str
    name: str
    type: str
    model: Optional[str] = None
    wattage: Optional[int] = None

class ApplianceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    model: Optional[str] = None
    wattage: Optional[int] = None

class EnergyReadingCreate(BaseModel):
    appliance_id: str
    consumption_kwh: float
    duration_minutes: int

# --- API Endpoints ---

@app.get("/")
def home():
    """A simple endpoint to check if the API is running."""
    return {"message": "Welcome to the EnergyFlo API"}

# --- Home Endpoints ---
@app.post("/homes/", status_code=201)
def create_home(home: HomeCreate):
    return db.add_home(user_id=home.user_id, address=home.address, utility_provider=home.utility_provider)

@app.get("/users/{user_id}/homes/")
def get_user_homes(user_id: str):
    return db.get_homes(user_id=user_id)

@app.get("/homes/{home_id}")
def get_home(home_id: str):
    home = db.get_home_by_id(home_id)
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")
    return home

@app.put("/homes/{home_id}")
def update_home(home_id: str, home: HomeUpdate):
    updated = db.update_home(home_id, home.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Home not found")
    return updated

@app.delete("/homes/{home_id}", status_code=200)
def delete_home(home_id: str):
    deleted = db.delete_home(home_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Home not found")
    return {"message": "Home deleted successfully", "deleted_record": deleted}

# --- Appliance Endpoints ---
@app.post("/appliances/", status_code=201)
def create_appliance(appliance: ApplianceCreate):
    return db.add_appliance(**appliance.model_dump())

@app.get("/homes/{home_id}/appliances/")
def get_home_appliances(home_id: str):
    return db.get_appliances(home_id=home_id)

@app.get("/appliances/{appliance_id}")
def get_appliance(appliance_id: str):
    appliance = db.get_appliance_by_id(appliance_id)
    if not appliance:
        raise HTTPException(status_code=404, detail="Appliance not found")
    return appliance

@app.put("/appliances/{appliance_id}")
def update_appliance(appliance_id: str, appliance: ApplianceUpdate):
    updated = db.update_appliance(appliance_id, appliance.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Appliance not found")
    return updated

@app.delete("/appliances/{appliance_id}", status_code=200)
def delete_appliance(appliance_id: str):
    deleted = db.delete_appliance(appliance_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Appliance not found")
    return {"message": "Appliance deleted successfully", "deleted_record": deleted}

# --- Energy Reading Endpoints ---
@app.post("/readings/", status_code=201)
def create_energy_reading(reading: EnergyReadingCreate):
    return db.add_energy_reading(**reading.model_dump())

@app.get("/appliances/{appliance_id}/readings/")
def get_appliance_readings(appliance_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    return db.get_energy_readings(appliance_id, start_date, end_date)

@app.delete("/readings/{reading_id}", status_code=200)
def delete_reading(reading_id: str):
    deleted = db.delete_reading(reading_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reading not found")
    return {"message": "Reading deleted successfully", "deleted_record": deleted}

# --- Logic/Analytics Endpoints ---
@app.get("/homes/{home_id}/summary")
def get_home_energy_summary(home_id: str, cost_per_kwh: float = 0.15):
    try:
        manager = TaskManager(home_id=home_id)
        return manager.get_home_summary(cost_per_kwh=cost_per_kwh)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/appliances/{appliance_id}/chart_data")
def get_appliance_chart_data(appliance_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    # For chart data, we need a home_id to initialize the manager, but the function
    # inside only needs appliance_id. This is a small quirk of the current class design.
    # We first fetch the appliance to get its home_id.
    appliance = db.get_appliance_by_id(appliance_id)
    if not appliance:
        raise HTTPException(status_code=404, detail="Appliance not found")
    
    manager = TaskManager(home_id=appliance['home_id'])
    return manager.prepare_chart_data(appliance_id, start_date, end_date)