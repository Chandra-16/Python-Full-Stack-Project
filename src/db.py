import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase URL and Key must be set in the .env file.")

sb: Client = create_client(url, key)

def add_home(user_id: str, address: str, utility_provider: str = None):
    """Adds a new home for a user."""
    response = sb.table('homes').insert({
        "user_id": user_id,
        "address": address,
        "utility_provider": utility_provider
    }).execute()
    return response.data

def get_homes(user_id: str):
    """Retrieves all homes associated with a user."""
    response = sb.table('homes').select('*').eq('user_id', user_id).execute()
    return response.data


def add_appliance(home_id: str, name: str, appliance_type: str, model: str = None, wattage: int = None):
    """Adds a new appliance to a specific home."""
    response = sb.table('appliances').insert({
        "home_id": home_id,
        "name": name,
        "type": appliance_type,
        "model": model,
        "wattage": wattage
    }).execute()
    return response.data

def get_appliances(home_id: str):
    """Retrieves all appliances in a specific home."""
    response = sb.table('appliances').select('*').eq('home_id', home_id).execute()
    return response.data

def add_energy_reading(appliance_id: str, consumption_kwh: float, duration_minutes: int):
    """Adds a new energy reading for an appliance."""
    response = sb.table('energy_readings').insert({
        "appliance_id": appliance_id,
        "timestamp": datetime.now().isoformat(),
        "consumption_kwh": consumption_kwh,
        "duration_minutes": duration_minutes
    }).execute()
    return response.data

def get_energy_readings(appliance_id: str, start_date: str = None, end_date: str = None):
    """Retrieves energy readings for an appliance, with optional date filtering."""
    query = sb.table('energy_readings').select('*').eq('appliance_id', appliance_id)
    
    if start_date:
        query = query.gte('timestamp', start_date)
    if end_date:
        query = query.lte('timestamp', end_date)
        
    response = query.order('timestamp', desc=True).execute()
    return response.data

# --- UPDATE Functions ---

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
    """Deletes a home and all its associated data (cascade)."""
    response = supabase.table('homes').delete().eq('id', home_id).execute()
    return response.data

def delete_appliance(appliance_id: str):
    """Deletes an appliance and its readings (cascade)."""
    response = supabase.table('appliances').delete().eq('id', appliance_id).execute()
    return response.data

def delete_reading(reading_id: str):
    """Deletes a single energy reading."""
    response = supabase.table('energy_readings').delete().eq('id', reading_id).execute()
    return response.data