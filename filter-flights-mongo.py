import json
import sys
import traceback

import pymongo

db_name = "flight-tracker"
source_collection_name = "flights-all"
target_collection_name = "flights-filtered"
mongo_url = sys.argv[1]
airport_code = sys.argv[2]


def main():
    try:
        db_client = pymongo.MongoClient(mongo_url)
        db = db_client[db_name]
        source_collection = db[source_collection_name]
        target_collection = db[target_collection_name]

        query_all_unprocessed = {"$or": [{"processed": False}, {"processed": None}, {"processed": ""}]}

        cursor = source_collection.find(query_all_unprocessed).limit(100)

        for flight in cursor:
            mongo_id = flight["_id"]
            icao = flight["icao"]
            callsign = flight["callsign"]
            created_at = flight["created_at"]
            if callsign is not None and len(callsign) > 0:
                callsign = callsign.strip()
                flight["callsign"] = callsign

            if not flight_exists_in_target_collection(icao, callsign, created_at, target_collection):
                if 0 < flight["altitude"] < 5000:
                    try:
                        flight["airport"] = airport_code
                        target_collection.insert_one(flight)
                        print("inserted flight", icao, "callsign", callsign, "altitude", flight["altitude"])
                    except pymongo.errors.PyMongoError as e:
                        traceback.print_exc()
                        print(f"Fehler beim Einfügen der Datensätze in MongoDB: {e}")
                else:
                    print("skipped because not in range: icao =", icao, "callsign =", callsign)
            else:
                print("skipped because known: icao =", icao, "callsign = ", callsign)

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


def flight_exists_in_target_collection(icao, callsign, created_at, target_collection):
    query = {"icao": icao, "callsign": callsign}
    cursor = target_collection.find(query).sort("created_at", -1).limit(1)

    for existing_flight in cursor:
        # print(f"existing_flight: {existing_flight}")

        last_seen_seconds = created_at - existing_flight["created_at"]
        one_day = 60 * 60 * 24 + 1
        print(f"callsign {callsign} was last_seen before {last_seen_seconds} seconds")

        if last_seen_seconds <= one_day:
            return True
        else:
            print("returning False -> flight will be added")
            return False


if __name__ == '__main__':
    main()
