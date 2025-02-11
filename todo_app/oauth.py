import os
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.github import github


blueprint = make_github_blueprint(
    client_id=os.getenv("OAUTH_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
)

from functools import wraps
from flask import Flask, g, request, redirect, url_for


def login_required(app: Flask):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not github.authorized:
                app.logger.info("Redirecting user to login")
                return redirect(url_for("github.login"))
            return f(*args, **kwargs)

        return decorated_function

    return decorator
