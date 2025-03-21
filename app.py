from fastapi import FastAPI, Query
from typing import List
from geopy.distance import geodesic

app = FastAPI()

# Sample donor data (usually fetched from a database)
donors = [
    {"donor_id": 1, "name": "John Doe", "blood_type": "O+", "location": (40.7128, -74.0060), "availability": "Available"},
    {"donor_id": 2, "name": "Jane Smith", "blood_type": "A-", "location": (34.0522, -118.2437), "availability": "Unavailable"},
    {"donor_id": 3, "name": "Mike Ross", "blood_type": "B+", "location": (51.5074, -0.1278), "availability": "Available"},
]

@app.get("/find_donors/")
async def find_donors(blood_type: str, lat: float, lon: float, max_distance_km: float = 50):
    available_donors = []

    for donor in donors:
        if donor["blood_type"] == blood_type and donor["availability"] == "Available":
            distance = geodesic((lat, lon), donor["location"]).km
            if distance <= max_distance_km:
                available_donors.append({**donor, "distance_km": round(distance, 2)})

    return {"matched_donors": sorted(available_donors, key=lambda x: x["distance_km"])}

