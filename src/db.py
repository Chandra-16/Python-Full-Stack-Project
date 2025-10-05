import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

# --- Supabase Connection ---
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase URL and Key must be set in the .env file.")

supabase: Client = create_client(url, key)

# --- GET (Read) Functions ---

def get_homes(user_id: str):
    """Retrieves all homes associated with a user."""
    response = supabase.table('homes').select('*').eq('user_id', user_id).execute()
    return response.data

def get_home_by_id(home_id: str):
    """Retrieves a single home by its ID."""
    response = supabase.table('homes').select('*').eq('id', home_id).single().execute()
    return response.data

def get_appliances(home_id: str):
    """Retrieves all appliances in a specific home."""
    response = supabase.table('appliances').select('*').eq('home_id', home_id).execute()
    return response.data

def get_appliance_by_id(appliance_id: str):
    """Retrieves a single appliance by its ID."""
    response = supabase.table('appliances').select('*').eq('id', appliance_id).single().execute()
    return response.data

def get_energy_readings(appliance_id: str, start_date: str = None, end_date: str = None):
    """Retrieves energy readings for an appliance, with optional date filtering."""
    query = supabase.table('energy_readings').select('*').eq('appliance_id', appliance_id)
    
    if start_date:
        query = query.gte('timestamp', start_date)
    if end_date:
        query = query.lte('timestamp', end_date)
        
    response = query.order('timestamp', desc=True).execute() # Show newest first
    return response.data

# --- POST (Create) Functions ---

def add_home(user_id: str, address: str, utility_provider: str = None):
    """Adds a new home for a user."""
    response = supabase.table('homes').insert({
        "user_id": user_id,
        "address": address,
        "utility_provider": utility_provider
    }).execute()
    return response.data

def add_appliance(home_id: str, name: str, appliance_type: str, model: str = None, wattage: int = None):
    """Adds a new appliance to a specific home."""
    response = supabase.table('appliances').insert({
        "home_id": home_id,
        "name": name,
        "type": appliance_type,
        "model": model,
        "wattage": wattage
    }).execute()
    return response.data

def add_energy_reading(appliance_id: str, consumption_kwh: float, duration_minutes: int):
    """Adds a new energy reading for an appliance."""
    response = supabase.table('energy_readings').insert({
        "appliance_id": appliance_id,
        "timestamp": datetime.now().isoformat(),
        "consumption_kwh": consumption_kwh,
        "duration_minutes": duration_minutes
    }).execute()
    return response.data

# --- PUT (Update) Functions ---

def update_home(home_id: str, data: dict):
    """Updates a home's details."""
    response = supabase.table('homes').update(data).eq('id', home_id).execute()
    return response.data

def update_appliance(appliance_id: str, data: dict):
    """Updates an appliance's details."""
    response = supabase.table('appliances').update(data).eq('id', appliance_id).execute()
    return response.data

# --- DELETE Functions ---

def delete_home(home_id: str):
    """Deletes a home."""
    response = supabase.table('homes').delete().eq('id', home_id).execute()
    return response.data

def delete_appliance(appliance_id: str):
    """Deletes an appliance."""
    response = supabase.table('appliances').delete().eq('id', appliance_id).execute()
    return response.data

def delete_reading(reading_id: str):
    """Deletes a single energy reading."""
    response = supabase.table('energy_readings').delete().eq('id', reading_id).execute()
    return response.data