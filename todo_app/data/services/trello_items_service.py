from todo_app.data.repositories.trello_repository import TrelloRepository
from todo_app.data.services.base_items_service import BaseItemsService


class TrelloItemsService(BaseItemsService):
    def __init__(self):
        self.repository = TrelloRepository()
