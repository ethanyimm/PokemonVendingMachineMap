import json
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load JSON file
with open("data/complete_locations.json", "r") as f:
    locations = json.load(f)

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),  # Default to 3306 if not set
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    
    cursor = conn.cursor()
    
    # Insert/Update query
    insert_query = """
    INSERT INTO vending_locations (
        id, retailer, machine_id, name, address, city, state, zip_code,
        latitude, longitude, type, last_verified, is_active
    ) VALUES (
        %(id)s, %(retailer)s, %(machine_id)s, %(name)s, %(address)s, %(city)s,
        %(state)s, %(zip_code)s, %(latitude)s, %(longitude)s, %(type)s,
        %(last_verified)s, %(is_active)s
    ) ON DUPLICATE KEY UPDATE
        retailer = VALUES(retailer),
        machine_id = VALUES(machine_id),
        name = VALUES(name),
        address = VALUES(address),
        city = VALUES(city),
        state = VALUES(state),
        zip_code = VALUES(zip_code),
        latitude = VALUES(latitude),
        longitude = VALUES(longitude),
        type = VALUES(type),
        last_verified = VALUES(last_verified),
        is_active = VALUES(is_active);
    """
    
    inserted = 0
    updated = 0
    errors = 0
    
    for loc in locations:
        try:
            cursor.execute(insert_query, loc)
            if cursor.rowcount == 1:
                inserted += 1
                print(f"✅ Inserted: {loc['id']}")
            elif cursor.rowcount == 2:
                updated += 1
                print(f"🔄 Updated: {loc['id']}")
        except Exception as e:
            errors += 1
            print(f"⚠️ Error with {loc.get('id')}: {e}")
    
    # Commit all changes
    conn.commit()
    
    print("\n=== Import Summary ===")
    print(f"✅ Inserted: {inserted}")
    print(f"🔄 Updated:  {updated}")
    print(f"⚠️ Errors:   {errors}")
    print("======================")
    
except mysql.connector.Error as db_error:
    print(f"❌ Database connection error: {db_error}")
except FileNotFoundError:
    print("❌ Could not find data/complete_locations.json file")
except json.JSONDecodeError as json_error:
    print(f"❌ JSON parsing error: {json_error}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
finally:
    # Clean up connections
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Database connection closed.")