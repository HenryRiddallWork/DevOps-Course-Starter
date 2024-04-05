from todo_app.data.models.item import Item

from todo_app.data.trello_repository import TrelloRepository

trello_repository = TrelloRepository()


def get_items() -> list[Item]:
    """
    Fetches all saved items.

    Returns:
        list: The list of saved items.
    """
    return trello_repository.get_board_items()


def get_item_by_id(id) -> Item:
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    return trello_repository.get_item(id)


def add_item(title):
    """
    Adds a new item with the specified title.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    return trello_repository.add_item(title)


def save_item(item: Item):
    """
    Updates an existing item. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    return trello_repository.update_item(item)


def remove_item_by_id(item_id):
    """
    Remove an existing item. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        item: The item to remove.
    """
    return trello_repository.remove_item(item_id)
