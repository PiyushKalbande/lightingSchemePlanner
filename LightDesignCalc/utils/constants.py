# Standard reflectance values for different colors (will be used with color picker)
COLOR_REFLECTANCE_RANGES = {
    "light": (0.6, 0.8),  # Light colors
    "medium": (0.3, 0.6), # Medium colors
    "dark": (0.1, 0.3)    # Dark colors
}

# Recommended illuminance levels (in lux) for different room types
ROOM_ILLUMINANCE = {
    "Living Room": 300,
    "Bedroom": 200,
    "Kitchen": 500,
    "Home Office": 500,
    "Bathroom": 300,
    "Dining Room": 300,
}

# Light reduction factors based on window orientation
ORIENTATION_FACTORS = {
    "North": 0.65,
    "South": 1.0,
    "East": 0.85,
    "West": 0.85,
}

# Mounting options for different fixtures
MOUNTING_OPTIONS = {
    "LED Bulb": ["Ceiling Mounted", "Wall Mounted", "Pendant"],
    "LED Panel": ["Recessed Ceiling", "Surface Mounted"],
    "LED Strip": ["Wall Mounted", "Cove Lighting", "Under Cabinet"],
    "LED Downlight": ["Recessed Ceiling"]
}

# Fixture types with detailed specifications (prices in INR)
FIXTURE_TYPES = {
    "LED Bulb": {
        "efficacy": 100,  # lumens per watt
        "wattage_range": (5, 15),
        "lifetime_hours": 25000,
        "cost_per_unit": 450,  # INR
        "description": "Energy-efficient, omnidirectional light",
        "installation_cost": 200,  # INR per unit
        "spacing_factor": 1.5  # Spacing to mounting height ratio
    },
    "LED Panel": {
        "efficacy": 120,
        "wattage_range": (20, 45),
        "lifetime_hours": 50000,
        "cost_per_unit": 2500,
        "description": "Even light distribution, modern look",
        "installation_cost": 500,
        "spacing_factor": 1.2
    },
    "LED Strip": {
        "efficacy": 80,
        "wattage_range": (10, 20),
        "lifetime_hours": 30000,
        "cost_per_unit": 1200,
        "description": "Flexible installation, ambient lighting",
        "installation_cost": 400,
        "spacing_factor": 1.0
    },
    "LED Downlight": {
        "efficacy": 90,
        "wattage_range": (8, 20),
        "lifetime_hours": 35000,
        "cost_per_unit": 800,
        "description": "Directional lighting, clean appearance",
        "installation_cost": 300,
        "spacing_factor": 1.3
    }
}

# Energy cost calculation constants (Indian standards)
ENERGY_COST_PER_KWH = 8.0  # Average electricity cost per kilowatt-hour in INR
HOURS_PER_DAY = 5  # Average usage hours per day
DAYS_PER_YEAR = 365

# Currency conversion
INR_TO_USD = 0.012  # 1 INR = 0.012 USD (approximate)