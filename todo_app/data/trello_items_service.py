from todo_app.data.models.item import Item

from todo_app.data.trello_repository import TrelloRepository, TrelloCard

trello_repository = TrelloRepository()


def map_card_to_item(card: TrelloCard) -> Item:
    """
    Converts a trello card into an item supported by the ToDo app.

    Args:
        card: A trello card

    Returns:
        item: The trello card as a ToDo item
    """
    trello_list = trello_repository.get_list_by_id(card.idList)
    item = Item.from_trello_card(card, trello_list)
    return item


def map_item_to_card(item: Item) -> TrelloCard:
    """
    Converts a ToDo item to a trello card.

    Args:
        card: A ToDo item
    Returns:
        item: The trello card
    """
    trello_list = trello_repository.get_or_create_list_by_name(item.status.value)
    card = TrelloCard(item.id, item.title, trello_list.id)
    return card


def get_items() -> list[Item]:
    """
    Fetches all saved items.

    Returns:
        list: The list of saved items.
    """
    return [map_card_to_item(card) for card in trello_repository.get_board_cards()]


def get_item_by_id(id) -> Item:
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    return map_card_to_item(trello_repository.get_card(id))


def add_item(title):
    """
    Adds a new item with the specified title.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    # Add the item to the list

    return trello_repository.add_card(title)


def save_item(item: Item):
    """
    Updates an existing item. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    return trello_repository.update_card(map_item_to_card(item))


def remove_item_by_id(item_id):
    """
    Remove an existing item. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        item: The item to remove.
    """
    return trello_repository.remove_card(item_id)
