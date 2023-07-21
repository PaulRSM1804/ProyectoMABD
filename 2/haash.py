from pymongo import MongoClient
import hashlib

def get_hashed_value(value):
    hashed_value = hashlib.md5(str(value).encode()).hexdigest()
    return hashed_value

def main():
    dbName = "MyDatabase"
    client = MongoClient("mongodb://127.0.0.1:27117,127.0.0.1:27118/")
    database = client[dbName]

    field_name = "supplierId"
    value = "example_value"

    hashed_value = get_hashed_value(value)

    shard_key = {field_name: "hashed"}
    hashed_field_value = {field_name: hashed_value}

    hashed_query = database.command("planCacheSetFilter", "MyCollection", shard_key, hashed_field_value)
    print("Hashed Query:", hashed_query)

if __name__ == "__main__":
    main()
