from todo_app.data.trello_repository import TrelloCard, TrelloList


class Item:
    def __init__(self, id, title, status = 'ToDo'):
        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def from_trello_card(cls, card: TrelloCard, list: TrelloList):
        return cls(card.id, card.name, list.name)