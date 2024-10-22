from flask import Flask, render_template, request, redirect
from todo_app.data.models.item import Item, Status

from todo_app.data.services.mongo_items_service import MongoItemsService
from todo_app.flask_config import Config
from todo_app.models.index_model import IndexModel


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(Config())
    mongoItemsService = MongoItemsService()

    @app.route("/")
    def index():
        items = mongoItemsService.get_items()
        sorted_items = sorted(items, key=lambda item: item.id)
        item_view_model = IndexModel(sorted_items)
        return render_template("/index.html", view_model=item_view_model)

    @app.route("/", methods=["POST"])
    def add_todo_item():
        mongoItemsService.add_item(request.form.get("title"))
        return redirect("/")

    @app.route("/delete", methods=["POST"])
    def remove_todo_item():
        mongoItemsService.remove_item_by_id(request.form.get("item_id"))
        return redirect("/")

    @app.route("/complete", methods=["POST"])
    def comeplete_todo_item():
        current_item = Item(
            request.form.get("item_id"),
            request.form.get("item_title"),
            Status[request.form.get("item_status")],
        )
        print(current_item.status.value)
        current_item.status = (
            Status.ToDo if current_item.status == Status.Completed else Status.Completed
        )
        print(current_item.status.value)
        mongoItemsService.save_item(current_item)
        return redirect("/")

    return app
