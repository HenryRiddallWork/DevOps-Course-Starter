import os
from flask import Flask, render_template, request, redirect
from todo_app.data.models.item import Status
from todo_app.data.trello_items_service import TrelloItemsService

from todo_app.flask_config import Config
from todo_app.models.index_model import IndexModel


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(Config())
    trelloItemsService = TrelloItemsService()

    @app.route("/")
    def index():
        items = trelloItemsService.get_items()
        sorted_items = sorted(items, key=lambda item: item.id)
        item_view_model = IndexModel(sorted_items)
        return render_template("/index.html", view_model=item_view_model)

    @app.route("/", methods=["POST"])
    def add_todo_item():
        trelloItemsService.add_item(request.form.get("title"))
        return redirect("/")

    @app.route("/delete", methods=["POST"])
    def remove_todo_item():
        trelloItemsService.remove_item_by_id(request.form.get("item_id"))
        return redirect("/")

    @app.route("/complete", methods=["POST"])
    def comeplete_todo_item():
        current_item = trelloItemsService.get_item_by_id(request.form.get("item_id"))
        current_item.status = (
            Status.ToDo if current_item.status == Status.Completed else Status.Completed
        )
        trelloItemsService.save_item(current_item)
        return redirect("/")

    return app
