from pymongo import MongoClient
from bson import ObjectId
import uuid

class User:
    def __init__(self, supplier_id, age, name, blog):
        self.Id = ObjectId()
        self.supplierId = supplier_id
        self.Age = age
        self.Name = name
        self.Blog = blog

def main():
    db_name = "MyDatabase"
    client = MongoClient("mongodb://127.0.0.1:27117")
    # client = MongoClient("mongodb://127.0.0.1:27050")

    database = client[db_name]
    collection = database["MyCollection"]

    id = 0
    num_records_in_batch = 10_000
    for times in range(10):
        requests = []
        print(f"{times} - start building records...")
        for j in range(num_records_in_batch):
            supplier_id = str(uuid.uuid4())
            age = 30 + id
            name = "Jin Auto " + str(id)
            blog = f"{id} - The company needed that grimoire because it was going to try to cast a spell in the real world—to transform a popular albeit niche game, \
                     complicated and nerdy, into a cross-media franchise. That has happened for comic books, for literature, even for toys, heaven help us. \
                     Lots of people would agree that existing franchises can turn into games. \
                     But can a famously intricate game turn into a story? That was Kelman’s task. Make it reasonable to produce Magic novels, \
                     Magic comic books, even—you saw this coming—an animated series on Netflix, produced by the people who wrote and directed the last two Avengers movies, to debut next year. \
                     And then maybe live action. Movies. Turn the universe of Magic: The Gathering into a story universe."

            user = User(supplier_id, age, name, blog)
            requests.append(user.__dict__)
            id += 1

        print(f"{times} - start inserting...")
        collection.insert_many(requests)

        print(f"{times} - {num_records_in_batch} records inserted.")

if __name__ == "__main__":
    main()
