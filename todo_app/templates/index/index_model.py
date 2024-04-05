from todo_app.data.models.item import Item, Status


class IndexModel:
    def __init__(self, items: list[Item]):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def completed_items(self):
        return [item for item in self._items if item.status == Status.Completed]

    @property
    def todo_items(self):
        return [item for item in self._items if item.status == Status.ToDo]
