# scripts/geocoder.py
#94% accuracy rate
import requests  # ← ADD THIS!
import json
import time
from pathlib import Path

class NominatimGeocoder:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.delay = 1
        self.headers = {
            'User-Agent': 'PokemonVendingFinder/1.0 (https://github.com/yourusername/Pokemon-Vending-Machine-Finder)'
        }
    
    def geocode_address(self, address, city, state):
        """Geocode a single address using Nominatim"""
        query = f"{address}, {city}, {state}, USA"
        params = {
            'q': query,
            'format': 'json',
            'limit': 1
        }
        
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
            
        except Exception as e:  # ← FIXED TYPO!
            print(f"Error geocoding {query}: {e}")
            
        return None, None
    
    def geocode_all_locations(self, input_path, output_path):
        """Geocode all locations in the JSON file"""
        with open(input_path, 'r', encoding='utf-8') as f:
            locations = json.load(f)
        
        successful = 0
        failed = 0
        
        print(f"Starting geocoding for {len(locations)} locations...")
        print("This will take about 2-3 minutes due to rate limiting...")
        
        for i, location in enumerate(locations):
            if location['latitude'] == 0.0 and location['longitude'] == 0.0:
                print(f"Geocoding {i+1}/{len(locations)}: {location['name']} in {location['city']}")
                
                lat, lng = self.geocode_address(
                    location['address'],
                    location['city'], 
                    location['state']
                )
                
                if lat and lng:
                    location['latitude'] = lat
                    location['longitude'] = lng
                    successful += 1
                else:
                    print(f"  ❌ Failed to geocode: {location['address']}")
                    failed += 1
                
                time.sleep(self.delay)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(locations, f, indent=2, ensure_ascii=False)
        
        print("\n✅ Geocoding complete!")
        print(f"   Successful: {successful}")
        print(f"   Failed: {failed}")
        print(f"   Saved to: {output_path}")

if __name__ == "__main__":
    geocoder = NominatimGeocoder()
    geocoder.geocode_all_locations('data/locations.json', 'data/locations_geocoded.json')