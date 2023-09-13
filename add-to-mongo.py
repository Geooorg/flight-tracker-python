import os
import json
import sys
import traceback

import pymongo

db_name = "flight-tracker"
collection_name = "flights-all"
mongo_url = sys.argv[1]

# JSON-Daten von der Standardeingabe lesen
json_data = input()

try:
    # JSON-Array in Python-Liste umwandeln
    flights = json.loads(json_data.replace('\n', '').replace('\r', ''))

    print(flights)

    if len(flights) > 0:
        db_client = pymongo.MongoClient(mongo_url)
        db = db_client[db_name]
        collection = db[collection_name]

        result = collection.insert_many(flights)
        db_client.close()

        print(f"Anzahl der eingefügten Datensätze: {len(result.inserted_ids)}")
        sys.exit(0)
    else:
        print("Keine Daten zum Einfügen gefunden.")
        sys.exit(0)
except json.JSONDecodeError as e:
    print(f"Fehler beim Decodieren des JSON: {e}")
    traceback.print_exc()
    sys.exit(1)
except pymongo.errors.PyMongoError as e:
    traceback.print_exc()
    print(f"Fehler beim Einfügen der Datensätze in MongoDB: {e}")
    sys.exit(2)
except Exception as e:
    traceback.print_exc()
    print(f"Unerwarteter Fehler: {e}")
    sys.exit(3)
