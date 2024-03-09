from enum import Enum
from todo_app.data.models.trello_objects import TrelloCard, TrelloList


class Status(Enum):
    ToDo = "ToDo"
    Completed = "Completed"


class Item:
    status: Status

    def __init__(self, id, title, status: Status = Status.ToDo):
        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def from_trello_card(cls, card: TrelloCard, list: TrelloList):
        return cls(card.id, card.name, Status[list.name])

    def get_status_value(self):
        return self.status.value

    status_value = property(get_status_value)
