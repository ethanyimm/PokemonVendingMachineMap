# manual_geocode_updater.py
import json
import webbrowser
import urllib.parse
from pathlib import Path

# Configuration - Update these paths to match your files
COMPLETE_LOCATIONS_FILE = "data/complete_locations.json"
FAILED_LOCATIONS_FILE = "data/new_failed_geocodes.txt"
MANUAL_UPDATES_FILE = "data/manual_updates.json"

def load_locations():
    """Load all locations from the complete file"""
    try:
        with open(COMPLETE_LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {COMPLETE_LOCATIONS_FILE} not found")
        return []

def find_failed_locations(all_locations):
    """Find locations with 0.0 coordinates"""
    failed = []
    for location in all_locations:
        # Check if both coordinates are 0.0 (or very close to it)
        if (abs(location.get('latitude', 1)) < 0.001 and 
            abs(location.get('longitude', 1)) < 0.001):
            failed.append(location)
    return failed

def open_in_maps(address):
    """Open a location in Google Maps for easy geocoding"""
    query = urllib.parse.quote_plus(address)
    url = f"https://www.google.com/maps/search/?api=1&query={query}"
    webbrowser.open(url)
    print(f"🌍 Opening Google Maps for: {address}")

def save_manual_updates(updates):
    """Save manual updates to a file"""
    with open(MANUAL_UPDATES_FILE, 'w', encoding='utf-8') as f:
        json.dump(updates, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved manual updates to {MANUAL_UPDATES_FILE}")

def update_locations(all_locations, updates):
    """Update locations with new coordinates"""
    updated_count = 0
    for update in updates:
        for location in all_locations:
            # Match by a unique identifier - adjust this based on your data structure
            if (location.get('name') == update['name'] and 
                location.get('address') == update.get('address')):
                location['latitude'] = update['lat']
                location['longitude'] = update['lng']
                updated_count += 1
                break
    return updated_count

def main():
    print("🔍 Loading locations...")
    all_locations = load_locations()
    
    if not all_locations:
        return
    
    print(f"📊 Total locations: {len(all_locations)}")
    
    # Find failed locations
    failed_locations = find_failed_locations(all_locations)
    print(f"❌ Failed geocodes: {len(failed_locations)}")
    
    if not failed_locations:
        print("🎉 All locations have proper coordinates!")
        return
    
    # Manual update process
    manual_updates = []
    
    print("\n" + "="*50)
    print("MANUAL GEOCODING PROCESS")
    print("="*50)
    
    for i, location in enumerate(failed_locations, 1):
        name = location.get('name', 'Unknown')
        address = location.get('address', '')
        city = location.get('city', '')
        state = location.get('state', '')
        
        full_address = f"{address}, {city}, {state}".strip(", ")
        
        print(f"\n📍 {i}/{len(failed_locations)}: {name}")
        print(f"   Address: {full_address}")
        
        # Open in Google Maps
        open_in_maps(full_address)
        
        # Get coordinates from user
        while True:
            coords = input("Enter coordinates as 'lat, lng' (or 'skip' to move on): ").strip()
            
            if coords.lower() == 'skip':
                print("⏭️  Skipping this location...")
                break
            
            try:
                lat, lng = map(float, coords.split(','))
                
                # Add to manual updates
                manual_updates.append({
                    'name': name,
                    'address': address,
                    'city': city,
                    'state': state,
                    'lat': lat,
                    'lng': lng
                })
                
                print(f"✅ Added coordinates: {lat}, {lng}")
                break
                
            except ValueError:
                print("❌ Invalid format. Please use: 40.7128, -74.0060")
    
    # Save manual updates
    if manual_updates:
        save_manual_updates(manual_updates)
        
        # Apply updates to the main data
        updated_count = update_locations(all_locations, manual_updates)
        
        # Save the complete file with updates
        with open(COMPLETE_LOCATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_locations, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 Successfully updated {updated_count} locations!")
        print(f"📁 Updated file: {COMPLETE_LOCATIONS_FILE}")
    else:
        print("\nℹ️  No manual updates were made.")

if __name__ == "__main__":
    main()