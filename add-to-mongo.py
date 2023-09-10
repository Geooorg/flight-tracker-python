import os
import json
import sys
import pymongo

connection_url = os.environ.get("mongoDbConnectionUrl")
db_name = "flight-tracker"
collection_name = "flights-HAM"

# JSON-Daten von der Standardeingabe lesen
json_data = input()
print(json_data)

try:
    # JSON-Array in Python-Liste umwandeln
    flights = json.loads(json_data.replace('\n', '').replace('\r', ''))

    if len(flights) > 0:
        db_client = pymongo.MongoClient(connection_url)
        db = db_client[db_name]
        collection = db[collection_name]

        # Versuche, die Datensätze in MongoDB einzufügen
        result = collection.insert_many(flights)
        db_client.close()

        print(f"Anzahl der eingefügten Datensätze: {len(result.inserted_ids)}")
    else:
        print("Keine Daten zum Einfügen gefunden.")
except json.JSONDecodeError as e:
    print(f"Fehler beim Decodieren des JSON: {e}")
    sys.exit(1)  # Beendet das Skript mit dem Fehlercode 1
except pymongo.errors.PyMongoError as e:
    print(f"Fehler beim Einfügen der Datensätze in MongoDB: {e}")
    sys.exit(2)
except Exception as e:
    print(f"Unerwarteter Fehler: {e}")
    sys.exit(3)
