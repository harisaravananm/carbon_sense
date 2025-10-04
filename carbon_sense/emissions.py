# emissions.py
def estimate_emissions(kwh, source='grid'):
    emission_factors = {
        'grid': 0.233,    # UK avg: 0.233 kg CO₂ / kWh
        'solar': 0.05,
        'wind': 0.01,
        'coal': 0.94,
    }
    factor = emission_factors.get(source, 0.233)
    return kwh * factor
