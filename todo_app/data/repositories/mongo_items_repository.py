import pymongo
import os

from todo_app.data.models.item import Item, Status
from todo_app.data.repositories.base_items_repository import BaseItemsRepository


class MongoRepository(BaseItemsRepository):
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
        self.database = self.client[os.getenv("MONGO_DB_NAME")]
        self.collection = self.database[os.getenv("MONGO_DB_COLLECTION")]

    def get_all_items(self) -> list[Item]:
        return [
            Item(
                mongo_item["_id"],
                mongo_item["title"],
                Status[mongo_item["status"]],
            )
            for mongo_item in self.collection.find({})
        ]

    def add_item(self, title):
        self.collection.insert_one({"title": title, "status": Status.ToDo.value})

    def update_item(self, item: Item):
        self.collection.update_one(
            {"_id": item.id},
            {"$set": {"title": item.title, "status": item.status.value}},
        )

    def remove_item(self, itemId: str):
        self.collection.delete_one({"_id": itemId})
