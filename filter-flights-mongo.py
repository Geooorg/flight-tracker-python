import json
import sys
import traceback

import pymongo

db_name = "flight-tracker"
collection_name_source = "flights-all"
collection_name_target = "flights-filtered"
mongo_url = sys.argv[1]
airport_code = sys.argv[2]


def main():
    try:
        db_client = pymongo.MongoClient(mongo_url)
        db = db_client[db_name]
        source_collection = db[collection_name_source]
        target_collection = db[collection_name_target]

        query_all_unprocessed = {"$or": [{"processed": False}, {"processed": None}]}

        cursor = source_collection.find(query_all_unprocessed).limit(50)

        for flight in cursor:
            mongo_id = flight["_id"]
            icao = flight["icao"]

            if not check_existing_processed_flight(icao, source_collection):
                if 0 < flight["altitude"] < 5000:
                    print("inserted flight ", icao)
                    try:
                        flight["airport"] = airport_code
                        target_collection.insert_one(flight)
                    except pymongo.errors.PyMongoError as e:
                        traceback.print_exc()
                        print(f"Fehler beim Einfügen der Datensätze in MongoDB: {e}")

            try:
                flight["processed"] = True
                source_collection.update_one({"_id": mongo_id}, {"$set": {"processed": True}})
                print("updated ID", mongo_id)
            except pymongo.errors.PyMongoError as e:
                traceback.print_exc()
                print(f"Fehler beim Update des Datensatzes in der MongoDB: {e}")

        db_client.close()
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"Fehler beim Decodieren des JSON: {e}")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        traceback.print_exc()
        print(f"Unerwarteter Fehler: {e}")
        sys.exit(3)


def check_existing_processed_flight(icao, collection):
    # Kriterium für die Abfrage
    query = {"icao": icao, "processed": True}

    # Suche nach einem Dokument, das dem Kriterium entspricht
    existing_flight = collection.find_one(query)

    # Überprüfe, ob ein passendes Dokument gefunden wurde
    if existing_flight:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
