# scripts/find_failed_geocodes.py
import json
from pathlib import Path

def find_failed_geocodes():
    """Find all locations that failed geocoding (still have 0.0 coordinates)"""
    
    # Load the geocoded data
    input_path = Path(__file__).parent.parent / 'data' / 'complete_locations.json'
    
    with open(input_path, 'r', encoding='utf-8') as f:
        locations = json.load(f)
    
    # Find failed locations (where both lat and lng are 0.0)
    failed_locations = [
        loc for loc in locations 
        if loc['latitude'] == 0.0 and loc['longitude'] == 0.0
    ]
    
    # Save failed locations to a separate file
    failed_output_path = Path(__file__).parent.parent / 'data' / 'new_failed_geocodes.json'
    with open(failed_output_path, 'w', encoding='utf-8') as f:
        json.dump(failed_locations, f, indent=2, ensure_ascii=False)
    
    # Also create a text file for easy manual lookup
    text_output_path = Path(__file__).parent.parent / 'data' / 'new_failed_geocodes.txt'
    with open(text_output_path, 'w', encoding='utf-8') as f:
        f.write("FAILED GEOCODING - NEED MANUAL COORDINATES\n")
        f.write("=" * 50 + "\n\n")
        
        for i, loc in enumerate(failed_locations, 1):
            f.write(f"{i}. {loc['name']}\n")
            f.write(f"   Address: {loc['address']}, {loc['city']}, {loc['state']}\n")
            f.write(f"   ID: {loc['id']}\n")
            f.write(f"   Machine ID: {loc['machine_id']}\n")
            f.write("-" * 40 + "\n")
    
    print(f"✅ Found {len(failed_locations)} failed geocodes")
    print(f"💾 Saved to: {failed_output_path}")
    print(f"📝 Text list: {text_output_path}")
    
    # Print summary
    if failed_locations:
        print("\n🔍 Sample of failed locations:")
        for i, loc in enumerate(failed_locations[:5], 1):  # Show first 5
            print(f"   {i}. {loc['name']} - {loc['address']}, {loc['city']}")
    else:
        print("🎉 All locations were successfully geocoded!")

if __name__ == "__main__":
    find_failed_geocodes()