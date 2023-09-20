import sys
import traceback

import pymongo

from airline_mapper import AirlineMapper

db_name = "flight-tracker"
mongo_url = sys.argv[1]
target_collection_name = sys.argv[2]


def main():
    try:
        db_client = pymongo.MongoClient(mongo_url)
        db = db_client[db_name]
        target_collection = db[target_collection_name]

        query_all_unprocessed = {"$or": [{"airline": {"$exists": False}}, {"airline": ""}]}
        cursor = target_collection.find(query_all_unprocessed).limit(1000)

        airline_mapper = AirlineMapper()

        for row in cursor:
            mongo_id = row["_id"]
            callsign = row["callsign"]

            if callsign is not None and len(callsign) > 3:
                try:
                    airline_name = airline_mapper.get_airline_name(callsign.strip())

                    target_collection.update_one(
                        {"_id": row["_id"]}, {"$set": {"airline": airline_name}}
                    )

                    print("determined airline for ID", mongo_id)

                except pymongo.errors.PyMongoError as e:
                    traceback.print_exc()
                    print(f"Update failed: {e}")

        # finally
        db_client.close()
        sys.exit(0)
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
        traceback.print_exc()

        sys.exit(1)


if __name__ == '__main__':
    main()
