# scripts/manual_geocode_updater.py
import json
import webbrowser
import urllib.parse
from pathlib import Path

# FIXED: Read from the GEOCODED file, not the original
DATA_FILE = Path("data/locations_geocoded.json")  # ← CHANGED THIS LINE

def load_data():
    """Load the geocoded data (with good coordinates)"""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"{DATA_FILE} not found")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """Save updated data back to the same file"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved updates to {DATA_FILE}")

def open_in_maps(address: str):
    """Open a full address in Google Maps"""
    query = urllib.parse.quote_plus(address)
    url = f"https://www.google.com/maps/search/?api=1&query={query}"
    webbrowser.open(url)
    print(f"🌍 Opening Google Maps for: {address}")

def find_location(data, location_id):
    """Find a location entry by ID"""
    for entry in data:
        if entry.get("id") == location_id:
            return entry
    return None

if __name__ == "__main__":
    data = load_data()

    while True:
        location_id = input("\nEnter location ID (or 'quit' to stop): ").strip()
        if location_id.lower() in ["quit", "exit"]:
            break

        location = find_location(data, location_id)
        if not location:
            print(f"❌ No location found for ID: {location_id}")
            continue

        # Build a full address string
        address_parts = [
            location.get("address", ""),
            location.get("city", ""),
            location.get("state", "")
        ]
        full_address = ", ".join([part for part in address_parts if part])  # skip blanks

        if not full_address.strip():
            print("⚠️ No address available for this entry.")
            continue

        # Step 1: Open Google Maps
        open_in_maps(full_address)

        # Step 2: Ask for combined lat/lon input
        coords = input("Paste coordinates (lat, lon) or press Enter to skip: ").strip()
        if coords:
            try:
                lat_str, lon_str = [c.strip() for c in coords.split(",")]
                location["latitude"] = float(lat_str)
                location["longitude"] = float(lon_str)
                save_data(data)
                print(f"✅ Updated {location_id} with coords ({lat_str}, {lon_str})")
            except Exception as e:
                print(f"⚠️ Invalid coordinates format: {e}")
        else:
            print("ℹ️ Skipped updating coordinates.")