from abc import ABC, abstractmethod

from todo_app.data.models.item import Item


class BaseItemsRepository(ABC):

    @abstractmethod
    def get_all_items(self) -> list[Item]:
        pass

    @abstractmethod
    def add_item(self, title: str):
        pass

    @abstractmethod
    def update_item(self, item: Item):
        pass

    @abstractmethod
    def remove_item(self, item_id: str):
        pass
