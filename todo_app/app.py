from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import get_items, add_item, remove_item_by_id, get_item_by_id, save_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def index():
    items = get_items()
    return render_template("index.html", items=items)

@app.route("/", methods=["POST"])
def add_todo_item():
    add_item(request.form.get("title"))
    return redirect("/")

@app.route("/delete", methods=["POST"])
def remove_todo_item():
    remove_item_by_id(request.form.get("item_id"))
    return redirect("/")

@app.route("/complete", methods=["POST"])
def comeplete_todo_item():
    current_item = get_item_by_id(request.form.get("item_id"))
    current_item["status"] = "Resumed" if current_item["status"] == "Completed" else "Completed"
    save_item(current_item)
    return redirect("/")
