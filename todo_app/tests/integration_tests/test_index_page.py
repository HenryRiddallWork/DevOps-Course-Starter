import os
import pymongo

from todo_app.data.models.item import Status


def test_index_page(client):
    # Insert fake card
    test = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
    test[os.getenv("MONGO_DB_NAME")][os.getenv("MONBGO_DB_COLLECTION")].insert_one(
        {"title": "Test card", "status": Status.ToDo.value}
    )

    # Make a request to our app's index page
    response = client.get("/")

    assert response.status_code == 200
    assert "Test card" in response.data.decode()
