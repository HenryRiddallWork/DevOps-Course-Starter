from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import get_items, add_item, remove_item_by_id

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items=items)

@app.route('/', methods=['POST'])
def addTodoItem():
    add_item(request.form.get('title'))
    return redirect('/')

@app.route('/delete', methods=['POST'])
def removeTodoItem():
    remove_item_by_id(request.form.get('item_id'))
    return redirect('/')
