# scripts/merge_geocoded_data.py
import json
from pathlib import Path

def merge_geocoded_data():
    """Merge the two files to get complete coordinates"""
    
    # Load both files
    auto_file = Path("data/autofilledgeolocations.txt")
    manual_file = Path("data/manuallyaddedgeolocations.txt")
    
    with open(auto_file, 'r', encoding='utf-8') as f:
        auto_data = json.load(f)
    
    with open(manual_file, 'r', encoding='utf-8') as f:
        manual_data = json.load(f)
    
    # Verify both have the same number of locations
    if len(auto_data) != len(manual_data):
        print("❌ Files have different numbers of locations!")
        return
    
    # Create the complete dataset
    complete_data = []
    

    for i in range(len(auto_data)):
        auto_loc = auto_data[i]
        manual_loc = manual_data[i]
        
        # They should have the same ID
        if auto_loc['id'] != manual_loc['id']:
            print(f"❌ ID mismatch at index {i}: {auto_loc['id']} vs {manual_loc['id']}")
            continue
        
        # Create merged location - start with auto data
        merged_loc = auto_loc.copy()
        
        # If auto has coordinates, use them
        if auto_loc['latitude'] != 0.0 and auto_loc['longitude'] != 0.0:
            # Already has coordinates from auto-geocoding
            pass
        # Else if manual has coordinates, use them
        elif manual_loc['latitude'] != 0.0 and manual_loc['longitude'] != 0.0:
            merged_loc['latitude'] = manual_loc['latitude']
            merged_loc['longitude'] = manual_loc['longitude']
        else:
            # Both have 0.0 - this shouldn't happen!
            print(f"❌ Both files have 0.0 for {auto_loc['id']}")
        
        complete_data.append(merged_loc)
    
    # Save the complete dataset
    output_file = Path("data/complete_locations.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, indent=2, ensure_ascii=False)
    
    # Count results
    complete_count = sum(1 for loc in complete_data if loc['latitude'] != 0.0)
    total_count = len(complete_data)
    
    print(f"✅ Merge complete!")
    print(f"   Total locations: {total_count}")
    print(f"   With coordinates: {complete_count}")
    print(f"   Missing coordinates: {total_count - complete_count}")
    print(f"   Saved to: {output_file}")
    
    # Verify we got all 1,632 with coordinates
    if complete_count == 1632:
        print("🎉 ALL 1,632 LOCATIONS HAVE COORDINATES!")
    else:
        print(f"❌ Still missing {1632 - complete_count} coordinates")

if __name__ == "__main__":
    merge_geocoded_data()