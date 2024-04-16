import pytest
import requests

from todo_app.tests.conftest import stub


def test_index_page(monkeypatch, client):
    # Replace requests.get(url) with our own function
    monkeypatch.setattr(requests, "get", stub)

    # Make a request to our app's index page
    response = client.get("/")

    assert response.status_code == 200
    assert "Test card" in response.data.decode()
