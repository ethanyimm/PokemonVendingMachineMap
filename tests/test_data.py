import json

with open('data/complete_locations.json', 'r') as f:
    data = json.load(f)

zeros = [loc for loc in data if loc['latitude'] == 0.0 and loc['longitude'] == 0.0]
print(f"Locations with (0,0) coordinates: {len(zeros)}")
print("✅ All done!" if len(zeros) == 0 else "❌ Still need to fix some locations")

#Locations with (0,0) coordinates: 0
#✅ All done!