import json
import os

# Required fields (no zip_code here since it's not always present)
REQUIRED_FIELDS = [
    "id", "retailer", "machine_id", "name", 
    "address", "city", "state", 
    "latitude", "longitude", 
    "type", "last_verified", "is_active"
]

def validate_entry(entry: dict, index: int) -> list:
    """Check if a single vending machine entry has all required fields and valid values."""
    errors = []
    
    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"Entry {index} missing field: {field}")
        else:
            value = entry[field]
            if value in ("", None):  # catches empty strings and nulls
                errors.append(f"Entry {index} field '{field}' is empty")

    # Type checks
    if "latitude" in entry and not isinstance(entry["latitude"], (int, float)):
        errors.append(f"Entry {index} latitude must be a number")
    if "longitude" in entry and not isinstance(entry["longitude"], (int, float)):
        errors.append(f"Entry {index} longitude must be a number")
    if "is_active" in entry and not isinstance(entry["is_active"], bool):
        errors.append(f"Entry {index} is_active must be true/false")
    
    return errors


def validate_file(filepath: str):
    """Validate all entries in the given JSON file."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in {filepath} — {e}")
            return
    
    all_errors = []
    for idx, entry in enumerate(data):
        entry_errors = validate_entry(entry, idx)
        all_errors.extend(entry_errors)
    
    if all_errors:
        print("Validation completed with errors:")
        for err in all_errors:
            print(" -", err)
    else:
        print("All entries are valid ✅")


if __name__ == "__main__":
    validate_file("data/locations.json")
