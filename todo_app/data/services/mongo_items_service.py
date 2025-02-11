from flask import Flask
from todo_app.data.repositories.mongo_items_repository import MongoRepository
from todo_app.data.services.base_items_service import BaseItemsService


class MongoItemsService(BaseItemsService):
    def __init__(self, app: Flask):
        app.logger.info("Initialising mongo item service...")
        super().__init__(app, MongoRepository())
        app.logger.info("Mongo item service initialisation complete!")
