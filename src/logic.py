from typing import List, Dict, Any
from . import db

class TaskManager:
    """
    Manages the business logic for processing and analyzing energy data.
    """
    def __init__(self, home_id: str):
        """
        Initializes the manager for a specific home.

        Args:
            home_id (str): The UUID of the home to manage.
        """
        if not home_id:
            raise ValueError("A valid home_id must be provided.")
        self.home_id = home_id

    def calculate_appliance_cost(self, appliance_id: str, cost_per_kwh: float, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Calculates the total consumption and cost for a single appliance.

        Args:
            appliance_id (str): The UUID of the appliance.
            cost_per_kwh (float): The cost rate for one kilowatt-hour.
            start_date (str, optional): The start date for the period.
            end_date (str, optional): The end date for the period.

        Returns:
            A dictionary containing total consumption and cost.
        """
        readings = db.get_energy_readings(appliance_id, start_date, end_date)
        
        total_kwh = sum(reading['consumption_kwh'] for reading in readings)
        total_cost = total_kwh * cost_per_kwh
        
        return {
            "appliance_id": appliance_id,
            "total_kwh": round(total_kwh, 4),
            "total_cost": round(total_cost, 2),
            "reading_count": len(readings)
        }

    def get_home_summary(self, cost_per_kwh: float, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Calculates the total cost and consumption for all appliances in the home.
        Also identifies the appliance with the highest consumption.

        Args:
            cost_per_kwh (float): The cost rate for one kilowatt-hour.
            start_date (str, optional): The start date for the period.
            end_date (str, optional): The end date for the period.

        Returns:
            A dictionary summarizing the home's total energy usage and costs.
        """
        appliances = db.get_appliances(self.home_id)
        if not appliances:
            return {"message": "No appliances found for this home."}

        overall_kwh = 0
        overall_cost = 0
        appliance_breakdown = []
        
        highest_consumption_appliance = {"name": None, "kwh": 0}

        for appliance in appliances:
            appliance_id = appliance['id']
            appliance_summary = self.calculate_appliance_cost(appliance_id, cost_per_kwh, start_date, end_date)
            
            # Add appliance name to the summary for context
            appliance_summary['name'] = appliance['name']
            appliance_breakdown.append(appliance_summary)
            
            overall_kwh += appliance_summary['total_kwh']
            overall_cost += appliance_summary['total_cost']

            # Check for the highest consumer
            if appliance_summary['total_kwh'] > highest_consumption_appliance['kwh']:
                highest_consumption_appliance['name'] = appliance['name']
                highest_consumption_appliance['kwh'] = appliance_summary['total_kwh']

        return {
            "home_id": self.home_id,
            "total_kwh": round(overall_kwh, 4),
            "total_cost": round(overall_cost, 2),
            "highest_consumer": highest_consumption_appliance,
            "appliance_breakdown": appliance_breakdown
        }