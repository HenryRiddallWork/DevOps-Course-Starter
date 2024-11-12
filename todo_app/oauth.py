import os
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.github import github


blueprint = make_github_blueprint(
    client_id=os.getenv("OAUTH_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
)

from functools import wraps
from flask import g, request, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not github.authorized:
            return redirect(url_for("github.login"))
        return f(*args, **kwargs)

    return decorated_function
