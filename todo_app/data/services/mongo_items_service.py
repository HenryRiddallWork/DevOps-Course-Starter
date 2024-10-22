from todo_app.data.repositories.mongo_items_repository import MongoRepository
from todo_app.data.services.base_items_service import BaseItemsService


class MongoItemsService(BaseItemsService):
    def __init__(self):
        self.repository = MongoRepository()
