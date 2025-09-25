from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
from typing import List, Optional

# --- Path Setup ---
# This allows the API to import modules from the 'src' directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import db
from src.logic import TaskManager

# ----------------- APP SETUP --------------------- #
app = FastAPI(title="EnergyFlo API", version="1.0")

# CORS (Cross-Origin Resource Sharing) middleware allows your frontend
# to communicate with this backend API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allows all origins
    allow_credentials=True,
    allow_methods=['*'],  # Allows all methods
    allow_headers=['*'],   # Allows all headers
)

# --- Pydantic Models (Data Schemas) ---
# These models define the structure of data for API requests

class HomeCreate(BaseModel):
    user_id: str
    address: str
    utility_provider: Optional[str] = None

class ApplianceCreate(BaseModel):
    home_id: str
    name: str
    type: str # e.g., "Refrigerator", "Television"
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

## Home Endpoints
@app.post("/homes/", status_code=201)
def create_home(home: HomeCreate):
    """Adds a new home to the database."""
    new_home = db.add_home(
        user_id=home.user_id,
        address=home.address,
        utility_provider=home.utility_provider
    )
    if not new_home:
        raise HTTPException(status_code=400, detail="Failed to create home.")
    return {"message": "Home created successfully", "data": new_home}

@app.get("/users/{user_id}/homes/")
def get_user_homes(user_id: str):
    """Retrieves all homes associated with a specific user."""
    homes = db.get_homes(user_id=user_id)
    return {"data": homes}

## Appliance Endpoints
@app.post("/appliances/", status_code=201)
def create_appliance(appliance: ApplianceCreate):
    """Adds a new appliance to a home."""
    new_appliance = db.add_appliance(
        home_id=appliance.home_id,
        name=appliance.name,
        appliance_type=appliance.type,
        model=appliance.model,
        wattage=appliance.wattage
    )
    if not new_appliance:
        raise HTTPException(status_code=400, detail="Failed to create appliance.")
    return {"message": "Appliance created successfully", "data": new_appliance}

@app.get("/homes/{home_id}/appliances/")
def get_home_appliances(home_id: str):
    """Retrieves all appliances in a specific home."""
    appliances = db.get_appliances(home_id=home_id)
    return {"data": appliances}

## Energy Reading Endpoints
@app.post("/readings/", status_code=201)
def create_energy_reading(reading: EnergyReadingCreate):
    """Adds a new energy reading for an appliance."""
    new_reading = db.add_energy_reading(
        appliance_id=reading.appliance_id,
        consumption_kwh=reading.consumption_kwh,
        duration_minutes=reading.duration_minutes
    )
    if not new_reading:
        raise HTTPException(status_code=400, detail="Failed to add reading.")
    return {"message": "Energy reading added successfully", "data": new_reading}

@app.get("/appliances/{appliance_id}/readings/")
def get_appliance_readings(appliance_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Retrieves energy readings for an appliance, with optional date filtering."""
    readings = db.get_energy_readings(appliance_id, start_date, end_date)
    return {"data": readings}

## Logic/Analytics Endpoint
@app.get("/homes/{home_id}/summary")
def get_home_energy_summary(home_id: str, cost_per_kwh: float = 0.15):
    """
    Provides a full energy consumption and cost summary for a specific home.
    Uses a default cost of $0.15/kWh if not provided.
    """
    try:
        manager = TaskManager(home_id=home_id)
        summary = manager.get_home_summary(cost_per_kwh=cost_per_kwh)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")