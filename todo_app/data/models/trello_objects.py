class TrelloCard:
    def __init__(self, id, name, idList) -> None:
        self.id = id
        self.name = name
        self.idList = idList


class TrelloList:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
