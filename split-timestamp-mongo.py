import sys
import traceback

import pymongo

from determine_datetime import UnixTimestampSplitter

db_name = "flight-tracker"
mongo_url = sys.argv[1]
target_collection_name = sys.argv[2]
timestamp_field = "created_at"


def main():
    try:
        db_client = pymongo.MongoClient(mongo_url)
        db = db_client[db_name]
        target_collection = db[target_collection_name]

        query_all_unprocessed = {"$or": [{"year": {"$exists": False}}, {"year": ""}]}
        cursor = target_collection.find(query_all_unprocessed).limit(1000)

        for row in cursor:
            mongo_id = row["_id"]
            timestamp = row[timestamp_field]
            splitter = UnixTimestampSplitter()

            if timestamp is None:
                print("Could not determine timestamp field, skipping row with ID", mongo_id)
                continue

            else:
                try:
                    year, month, day, hour, minute, seconds = splitter.split_unix_timestamp(timestamp)
                    row["year"] = year
                    row["month"] = month
                    row["day"] = day
                    row["hour"] = hour
                    row["minute"] = minute
                    row["seconds"] = seconds

                    target_collection.update_one(
                        {"_id": row["_id"]},
                        {"$set": {
                            "year": row["year"],
                            "month": row["month"],
                            "day": row["day"],
                            "hour": row["hour"],
                            "minute": row["minute"],
                            "seconds": row["seconds"]
                        }}
                    )

                    print("updated ID", mongo_id)

                except pymongo.errors.PyMongoError as e:
                    traceback.print_exc()
                    print(f"Update failed: {e}")

        db_client.close()
        sys.exit(0)
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
        traceback.print_exc()

        sys.exit(2)


if __name__ == '__main__':
    main()
