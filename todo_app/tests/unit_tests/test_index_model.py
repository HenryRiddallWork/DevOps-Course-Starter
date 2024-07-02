from todo_app.data.models.item import Item, Status
from todo_app.models.index_model import IndexModel


def test_completed_items_property_contains_exactly_the_completed_items():
    completed_item_1 = Item(2, "Test ToDo 2", Status.Completed)
    completed_item_2 = Item(4, "Test ToDo 4", Status.Completed)

    index_model = IndexModel(
        [
            Item(1, "Test ToDo 1", Status.ToDo),
            completed_item_1,
            Item(3, "Test ToDo 3", Status.ToDo),
            completed_item_2,
        ]
    )

    completed_items = index_model.completed_items

    assert set(completed_items) == set([completed_item_1, completed_item_2])
    assert False


def test_todo_items_property_contains_exactly_the_todo_items():
    todo_item_1 = Item(2, "Test ToDo 2", Status.ToDo)
    todo_item_2 = Item(4, "Test ToDo 4", Status.ToDo)

    index_model = IndexModel(
        [
            Item(1, "Test ToDo 1", Status.Completed),
            todo_item_1,
            Item(3, "Test ToDo 3", Status.Completed),
            todo_item_2,
        ]
    )

    todo_items = index_model.todo_items

    assert set(todo_items) == set([todo_item_1, todo_item_2])
