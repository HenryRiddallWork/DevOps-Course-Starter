from flask import Flask
from todo_app import app
from todo_app.data.models.item import Item, Status
from todo_app.data.repositories.base_items_repository import BaseItemsRepository


class BaseItemsService:
    def __init__(self, app: Flask, repository: BaseItemsRepository):
        self.app = app
        self.repository = repository

    def get_items(self) -> list[Item]:
        """
        Fetches all saved items.

        Returns:
            list: The list of saved items.
        """
        self.app.logger.info("Getting items")
        return self.repository.get_all_items()

    def add_item(self, title):
        """
        Adds a new item with the specified title.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """
        self.app.logger.info("Adding: " + title)
        return self.repository.add_item(title)

    def toggle_item_status(self, item: Item):
        """
        Toggles an existing item between the two possible statuses.

        Args:
            item: The item to toggle.
        """
        self.app.logger.info("Toggling status for: " + item.id)
        item.status = (
            Status.ToDo if item.status == Status.Completed else Status.Completed
        )

        return self.repository.update_item(item)

    def remove_item_by_id(self, item_id):
        """
        Remove an existing item. If no existing item matches the ID of the specified item, nothing is removed.

        Args:
            item: The item to remove.
        """
        self.app.logger.info("Removing item: " + item_id)
        return self.repository.remove_item(item_id)
