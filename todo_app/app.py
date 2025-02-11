from flask import Flask, render_template, request, redirect
from todo_app.data.models.item import Item, Status
from werkzeug.middleware.proxy_fix import ProxyFix

from todo_app.data.services.mongo_items_service import MongoItemsService
from todo_app.flask_config import Config
from todo_app.models.index_model import IndexModel
from todo_app.oauth import blueprint, login_required


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(Config())
    app.logger.setLevel(app.config["LOG_LEVEL"])
    app.wsgi_app = ProxyFix(app.wsgi_app)
    mongoItemsService = MongoItemsService(app)

    app.register_blueprint(blueprint, url_prefix="/login")

    @app.route("/")
    @login_required(app)
    def index():
        items = mongoItemsService.get_items()
        sorted_items = sorted(items, key=lambda item: item.id)
        item_view_model = IndexModel(sorted_items)
        return render_template("/index.html", view_model=item_view_model)

    @app.route("/", methods=["POST"])
    @login_required(app)
    def add_todo_item():
        mongoItemsService.add_item(request.form.get("title"))
        return redirect("/")

    @app.route("/delete", methods=["POST"])
    @login_required(app)
    def remove_todo_item():
        mongoItemsService.remove_item_by_id(request.form.get("item_id"))
        return redirect("/")

    @app.route("/toggle", methods=["POST"])
    @login_required(app)
    def toggle_todo_item_status():
        current_item = Item(
            request.form.get("item_id"),
            request.form.get("item_title"),
            Status[request.form.get("item_status")],
        )

        mongoItemsService.toggle_item_status(current_item)

        return redirect("/")

    return app
