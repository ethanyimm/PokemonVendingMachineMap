import json
import re
from pathlib import Path

def convert_text_to_json(text_data):
    """Convert your text data to JSON format automatically"""
    
    lines = text_data.strip().split('\n')
    locations = []
    
    for line in lines:
        if line.strip():  # Skip empty lines
            # Split the line by tabs or multiple spaces
            parts = re.split(r'\t|\s{2,}', line.strip())
            parts = [p.strip() for p in parts if p.strip()]
            
            if len(parts) >= 4:
                retailer = parts[0]
                machine_id = parts[1]
                address = parts[2]
                city_state = parts[3]
                
                # Extract city and state from "City, State" format
                if ', ' in city_state:
                    city, state = city_state.split(', ', 1)
                else:
                    city, state = city_state, "Arizona"  # Default to AZ
                
                # Create unique ID
                location_id = f"{retailer.lower()}_{machine_id}"
                
                location = {
                    "id": location_id,
                    "retailer": retailer,
                    "machine_id": machine_id,
                    "name": retailer,
                    "address": address,
                    "city": city,
                    "state": state,
                    "zip_code": "",
                    "latitude": 0.0,  # We'll geocode these later
                    "longitude": 0.0,
                    "type": "grocery" if retailer in ["Frys", "Safeway", "Albertsons", "WinCo Foods"] else "retail",
                    "last_verified": "2024-01-15",
                    "is_active": True
                }
                
                locations.append(location)
    
    return locations

def main():
    # Load text from file instead of hardcoding
    input_path = Path(__file__).parent.parent / 'raw_text' / 'locations.txt'
    text_data = input_path.read_text(encoding='utf-8')
    
    locations = convert_text_to_json(text_data)

    # Save to JSON file
    output_path = Path(__file__).parent.parent / 'data' / 'locations.json'
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(locations, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully converted {len(locations)} locations!")
    print(f"💾 Saved to: {output_path}")

if __name__ == "__main__":
    main()