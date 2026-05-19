from __future__ import annotations

from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .db import Database
from .routes import bp


def create_app(test_config: dict | None = None) -> Flask:
    load_dotenv()

    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    app.db = Database(app.config)  # type: ignore[attr-defined]
    app.register_blueprint(bp)

    return app

