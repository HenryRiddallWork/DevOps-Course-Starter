from todo_app.data.models.item import Item
from todo_app.data.repositories.base_items_repository import BaseItemsRepository


class BaseItemsService:
    def __init__(self, repository: BaseItemsRepository):
        self.repository = repository

    def get_items(self) -> list[Item]:
        """
        Fetches all saved items.

        Returns:
            list: The list of saved items.
        """
        return self.repository.get_all_items()

    def add_item(self, title):
        """
        Adds a new item with the specified title.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """
        return self.repository.add_item(title)

    def save_item(self, item: Item):
        """
        Updates an existing item. If no existing item matches the ID of the specified item, nothing is saved.

        Args:
            item: The item to save.
        """
        return self.repository.update_item(item)

    def remove_item_by_id(self, item_id):
        """
        Remove an existing item. If no existing item matches the ID of the specified item, nothing is removed.

        Args:
            item: The item to remove.
        """
        return self.repository.remove_item(item_id)
