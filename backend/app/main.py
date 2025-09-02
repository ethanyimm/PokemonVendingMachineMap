# backend/app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from math import cos, radians
from sqlalchemy.orm import Session
from .database import get_db
from .models import VendingLocation  # ← CHANGED THIS LINE

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Pokemon Vending Machine API is running!"}

@app.get("/api/debug-env")
async def debug_env():
    import os
    return {
        "MYSQLUSER": os.getenv("MYSQLUSER"),
        "MYSQLPASSWORD": os.getenv("MYSQLPASSWORD"),
        "MYSQLHOST": os.getenv("MYSQLHOST"),
        "MYSQLPORT": os.getenv("MYSQLPORT"),
        "MYSQLDATABASE": os.getenv("MYSQLDATABASE")
    }


@app.get("/api/locations")
async def get_all_locations(db: Session = Depends(get_db)):
    """Get all vending machine locations"""
    try:
        # Using SQLAlchemy ORM approach
        locations = db.query(VendingLocation).all()  # ← CHANGED HERE
        return locations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/locations/{state}")
async def get_locations_by_state(state: str, db: Session = Depends(get_db)):
    """Get locations for a specific state"""
    try:
        # Query using SQLAlchemy
        locations = db.query(VendingLocation).filter(VendingLocation.state == state.upper()).all()  # ← CHANGED HERE
        return locations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/locations/nearby")
async def get_nearby_locations(
    lat: float, 
    lng: float, 
    radius_km: int = 10,
    db: Session = Depends(get_db)
):
    """Find locations near given coordinates"""
    try:
        # Calculate bounding box
        lat_range = radius_km / 111.0
        lng_range = radius_km / (111.0 * cos(radians(lat)))
        
        # SQLAlchemy query with bounding box
        locations = db.query(VendingLocation).filter(  # ← CHANGED HERE
            VendingLocation.latitude.between(lat - lat_range, lat + lat_range),  # ← CHANGED HERE
            VendingLocation.longitude.between(lng - lng_range, lng + lng_range)  # ← CHANGED HERE
        ).all()
        
        return locations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")