from enum import Enum


class Status(Enum):
    ToDo = "ToDo"
    Completed = "Completed"


class Item:
    status: Status

    def __init__(self, id, title, status: Status = Status.ToDo):
        self.id = id
        self.title = title
        self.status = status

    def get_status_value(self):
        return self.status.value

    status_value = property(get_status_value)

    @property
    def is_complete(self):
        return self.status == Status.Completed
