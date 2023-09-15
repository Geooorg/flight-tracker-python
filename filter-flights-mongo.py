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

        query_all_unprocessed = {"$or": [{"processed": False}, {"processed": None}, {"processed": ""}]}

        cursor = source_collection.find(query_all_unprocessed).limit(250)

        for flight in cursor:
            mongo_id = flight["_id"]
            icao = flight["icao"]
            callsign = flight["callsign"]
            if callsign is not None and len(callsign) > 0:
                callsign = callsign.strip()

            if not check_existing_processed_flight(icao, callsign, source_collection):
                if 0 < flight["altitude"] < 5000:
                    try:
                        flight["airport"] = airport_code
                        target_collection.insert_one(flight)
                        print("inserted flight", icao, "callsign", callsign, "altitude", flight["altitude"])
                    except pymongo.errors.PyMongoError as e:
                        traceback.print_exc()
                        print(f"Fehler beim Einfügen der Datensätze in MongoDB: {e}")
                else:
                    print("skipped flight", icao, "with callsign", callsign)

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
        print(f"Unerwarteter Fehler: {e}")
        traceback.print_exc()
        sys.exit(2)


def check_existing_processed_flight(icao, callsign, collection):
    query = {"icao": icao, "callsign": callsign, "processed": True}
    existing_flight = collection.find_one(query)

    if existing_flight:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
