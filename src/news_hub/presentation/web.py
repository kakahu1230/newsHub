"""Flask application serving the NewsHub dashboard."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List

from flask import Flask, jsonify, render_template

from ..config import PROCESSED_DIR

BASE_PATH = Path(__file__).resolve().parents[2]
TEMPLATE_FOLDER = BASE_PATH / "templates"
STATIC_FOLDER = BASE_PATH / "static"


def load_stories() -> List[dict]:
    path = PROCESSED_DIR / "stories.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    for item in data:
        if item.get("published_at"):
            item["published_at"] = datetime.fromisoformat(item["published_at"]).strftime("%Y-%m-%d %H:%M")
    return data


def create_app() -> Flask:
    app = Flask(__name__, template_folder=str(TEMPLATE_FOLDER), static_folder=str(STATIC_FOLDER))

    @app.route("/")
    def index() -> str:
        stories = load_stories()
        categories = sorted({category for story in stories for category in story.get("categories", [])})
        return render_template("index.html", stories=stories, categories=categories)

    @app.route("/api/stories")
    def api_stories():
        return jsonify(load_stories())

    return app


app = create_app()


__all__ = ["app", "create_app", "load_stories"]
