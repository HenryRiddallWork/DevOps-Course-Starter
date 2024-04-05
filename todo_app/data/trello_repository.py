import requests
import os

from todo_app.data.models.item import Item, Status
from todo_app.data.models.trello_objects import TrelloList


class TrelloRepository:
    def __init__(self):
        self.headers = {"Accept": "application/json"}
        self.base_query_params = {
            "key": os.getenv("TRELLO_API_KEY"),
            "token": os.getenv("TRELLO_API_TOKEN"),
            "fields": "id,name,idList,",
        }
        self.board_id = os.getenv("TRELLO_BOARD_ID")
        self.board_url = f"https://api.trello.com/1/boards/{self.board_id}"
        self.lists_cache = {}

        self.default_list = self.get_or_create_list_by_name(Status.ToDo.value)

    def refresh_lists_cache(self):
        response = requests.get(
            f"{self.board_url}/lists", params=self.base_query_params
        )
        api_lists = response.json()

        self.lists_cache = dict(
            zip(
                [api_list["id"] for api_list in api_lists],
                [
                    TrelloList(api_list["id"], api_list["name"])
                    for api_list in api_lists
                ],
            )
        )

    def get_list_by_id(self, id) -> TrelloList:
        if id not in self.lists_cache.keys():
            self.refresh_lists_cache()

        return self.lists_cache.get(id)

    def get_or_create_list_by_name(self, name: str) -> TrelloList:
        if not any(list.name == name for list in self.lists_cache.values()):
            self.refresh_lists_cache()

        if not any(list.name == name for list in self.lists_cache.values()):
            requests.post(
                "https://api.trello.com/1/lists",
                params={
                    **self.base_query_params,
                    "name": name,
                    "idBoard": self.board_id,
                },
            )

            self.refresh_lists_cache()

        return next((list for list in self.lists_cache.values() if list.name == name))

    def get_board_items(self) -> list[Item]:
        response = requests.get(
            f"{self.board_url}/cards", params=self.base_query_params
        )
        return [
            Item(
                api_card["id"],
                api_card["name"],
                Status(self.get_list_by_id(api_card["idList"]).name),
            )
            for api_card in response.json()
        ]

    def add_item(self, title):
        response = requests.post(
            "https://api.trello.com/1/cards",
            headers=self.headers,
            params={
                **self.base_query_params,
                "idList": self.default_list.id,
                "name": title,
            },
        )

        return response

    def update_item(self, item: Item):
        response = requests.put(
            f"https://api.trello.com/1/cards/{item.id}",
            headers=self.headers,
            params={
                **self.base_query_params,
                "idList": self.get_or_create_list_by_name(item.status.value).id,
                "name": item.title,
            },
        )
        return response

    def remove_item(self, itemId):
        response = requests.delete(
            f"https://api.trello.com/1/cards/{itemId}",
            headers=self.headers,
            params=self.base_query_params,
        )

        return response

    def get_item(self, itemId) -> Item:
        response = requests.get(
            f"https://api.trello.com/1/cards/{itemId}",
            headers=self.headers,
            params=self.base_query_params,
        )
        api_card = response.json()
        return Item(
            api_card["id"],
            api_card["name"],
            Status(self.get_list_by_id(api_card["idList"]).name),
        )
