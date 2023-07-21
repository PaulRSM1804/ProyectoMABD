import csv
import uuid
from pymongo import MongoClient
from bson import ObjectId

class User:
    def __init__(self, supplier_id, value, wm_yr_wk, wday, month, year, snap_CA, snap_TX, sell_price, dept_id, week, day):
        self.Id = ObjectId()
        self.supplierId = supplier_id
        self.value = value
        self.wm_yr_wk = wm_yr_wk
        self.wday = wday
        self.month = month
        self.year = year
        self.snap_CA = snap_CA
        self.snap_TX = snap_TX
        self.sell_price = sell_price
        self.dept_id = dept_id
        self.week = week
        self.day = day

def main():
    db_name = "MyDatabase"
    client = MongoClient("mongodb://127.0.0.1:27117")
    # client = MongoClient("mongodb://127.0.0.1:27050")

    database = client[db_name]
    collection = database["MyCollection"]

    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            supplier_id = str(uuid.uuid4())
            user = User(
                supplier_id,
                int(row['value']),
                int(row['wm_yr_wk']),
                int(row['wday']),
                int(row['month']),
                int(row['year']),
                int(row['snap_CA']),
                int(row['snap_TX']),
                float(row['sell_price']),
                int(row['dept_id']),
                int(row['week']),
                int(row['day'])
            )
            collection.insert_one(user.__dict__)

    print("All records inserted.")

if __name__ == "__main__":
    main()
