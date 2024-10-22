import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
import mongomock


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with mongomock.patch(servers=(("fakemongo.com", 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client
