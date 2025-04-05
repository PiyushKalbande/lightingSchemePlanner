import numpy as np
from .constants import COLOR_REFLECTANCE_RANGES, ORIENTATION_FACTORS, FIXTURE_TYPES
from colour import Color

def calculate_room_area(length: float, width: float) -> float:
    """Calculate room area in square meters."""
    return length * width

def calculate_room_volume(length: float, width: float, height: float) -> float:
    """Calculate room volume in cubic meters."""
    return length * width * height

def calculate_window_area(num_windows: int, window_width: float, window_height: float) -> float:
    """Calculate total window area in square meters."""
    return num_windows * window_width * window_height

def calculate_natural_light(window_area: float, room_area: float, orientation: str) -> float:
    """Calculate natural light contribution factor."""
    window_to_floor_ratio = window_area / room_area
    orientation_factor = ORIENTATION_FACTORS[orientation]
    return window_to_floor_ratio * orientation_factor

def calculate_color_reflectance(color_hex: str) -> float:
    """Calculate reflectance based on color brightness."""
    # Ensure color_hex has the '#' prefix for Color class
    if not color_hex.startswith('#'):
        color_hex = '#' + color_hex

    color = Color(color_hex)
    brightness = sum(color.rgb) / 3

    if brightness > 0.7:
        return np.interp(brightness, [0.7, 1], COLOR_REFLECTANCE_RANGES["light"])
    elif brightness > 0.3:
        return np.interp(brightness, [0.3, 0.7], COLOR_REFLECTANCE_RANGES["medium"])
    else:
        return np.interp(brightness, [0, 0.3], COLOR_REFLECTANCE_RANGES["dark"])

def calculate_average_reflectance(wall_color: str, ceiling_color: str) -> float:
    """Calculate average reflectance of room surfaces."""
    wall_reflectance = calculate_color_reflectance(wall_color)
    ceiling_reflectance = calculate_color_reflectance(ceiling_color)
    floor_reflectance = 0.3  # Assuming medium gray floor

    return (4 * wall_reflectance + ceiling_reflectance + floor_reflectance) / 6

def calculate_fixture_positions(length: float, width: float, height: float, 
                             fixture_type: str, required_lumens: float, mounting_type: str = "Ceiling Mounted") -> list:
    """Calculate optimal fixture positions."""
    fixture_specs = FIXTURE_TYPES[fixture_type]
    spacing_factor = fixture_specs["spacing_factor"]

    # Calculate number of fixtures needed based on lumens per fixture
    lumens_per_fixture = fixture_specs["efficacy"] * np.mean(fixture_specs["wattage_range"])
    num_fixtures = max(1, int(np.ceil(required_lumens / lumens_per_fixture)))

    # Calculate optimal spacing
    spacing = height * spacing_factor

    # Calculate grid dimensions
    rows = max(1, int(np.sqrt(num_fixtures * width / length)))
    cols = max(1, int(np.ceil(num_fixtures / rows)))

    positions = []
    for row in range(rows):
        for col in range(cols):
            if len(positions) < num_fixtures:
                x = length * (col + 1) / (cols + 1)
                y = width * (row + 1) / (rows + 1)
                z = height
                positions.append({"x": x, "y": y, "z": z})

    return positions

def calculate_energy_metrics(fixture_type: str, num_fixtures: int, 
                           daily_hours: float = 5) -> dict:
    """Calculate energy consumption and cost metrics."""
    fixture_specs = FIXTURE_TYPES[fixture_type]
    avg_wattage = np.mean(fixture_specs["wattage_range"])

    # Daily energy consumption in kWh
    daily_energy = (avg_wattage * num_fixtures * daily_hours) / 1000

    # Annual metrics
    annual_energy = daily_energy * 365
    annual_cost = annual_energy * 0.15  # Assuming $0.15 per kWh

    # Lifetime metrics
    lifetime_hours = fixture_specs["lifetime_hours"]
    lifetime_years = lifetime_hours / (daily_hours * 365)
    lifetime_energy_cost = annual_cost * lifetime_years

    # Initial cost
    initial_cost = num_fixtures * fixture_specs["cost_per_unit"]

    # Total cost of ownership
    total_cost = initial_cost + lifetime_energy_cost

    return {
        "daily_energy_kwh": daily_energy,
        "annual_energy_kwh": annual_energy,
        "annual_cost": annual_cost,
        "lifetime_years": lifetime_years,
        "initial_cost": initial_cost,
        "total_cost": total_cost,
        "energy_efficiency": fixture_specs["efficacy"]
    }

def get_fixture_recommendations(required_lumens: float) -> dict:
    """Get recommended light fixture combinations with energy metrics."""
    recommendations = {}

    for fixture_type, specs in FIXTURE_TYPES.items():
        lumens_per_fixture = specs["efficacy"] * np.mean(specs["wattage_range"])
        num_fixtures = max(1, int(np.ceil(required_lumens / lumens_per_fixture)))

        if num_fixtures <= 8:  # Reasonable number of fixtures
            energy_metrics = calculate_energy_metrics(fixture_type, num_fixtures)
            recommendations[fixture_type] = {
                "count": num_fixtures,
                "description": f"{num_fixtures} x {fixture_type}s",
                "specs": specs,
                "energy_metrics": energy_metrics
            }

    return recommendations

def calculate_required_lumens(
    room_area: float,
    required_lux: float,
    reflectance: float,
    natural_light_factor: float
) -> float:
    """Calculate required artificial light lumens."""
    # Basic lumen calculation
    base_lumens = room_area * required_lux

    # Adjust for surface reflectance
    reflectance_factor = 1 / (0.8 + reflectance)

    # Reduce required lumens based on natural light
    artificial_lumens = base_lumens * reflectance_factor * (1 - natural_light_factor)

    return max(0, artificial_lumens)