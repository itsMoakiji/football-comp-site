"""
Football Compilations - a small Flask web app.

Drop video files into static/videos/ (or sub-folders like static/videos/goals/)
and they appear on the site automatically. The sub-folder name becomes the
category. A thumbnail with the same name as the video (e.g. bicycle-kick.jpg
next to bicycle-kick.mp4) is used as the card image if present.
"""

import os
from pathlib import Path

from flask import Flask, jsonify, render_template

app = Flask(__name__)

VIDEO_DIR = Path(app.static_folder) / "videos"
VIDEO_EXTS = {".mp4", ".webm", ".ogg", ".mov"}
THUMB_EXTS = (".jpg", ".jpeg", ".png", ".webp")


def pretty(name: str) -> str:
    """Turn 'best_free-kicks' into 'Best Free Kicks'."""
    return name.replace("_", " ").replace("-", " ").strip().title()


def load_videos() -> list[dict]:
    """Scan the videos folder and build a list of video entries."""
    videos = []
    if not VIDEO_DIR.exists():
        return videos

    for file in sorted(VIDEO_DIR.rglob("*")):
        if not file.is_file() or file.suffix.lower() not in VIDEO_EXTS:
            continue

        category = pretty(file.parent.name) if file.parent != VIDEO_DIR else "Highlights"

        thumbnail = None
        for ext in THUMB_EXTS:
            candidate = file.with_suffix(ext)
            if candidate.exists():
                thumbnail = candidate.relative_to(app.static_folder).as_posix()
                break

        videos.append(
            {
                "id": len(videos),
                "title": pretty(file.stem),
                "category": category,
                "src": file.relative_to(app.static_folder).as_posix(),
                "thumbnail": thumbnail,
                "size_mb": round(file.stat().st_size / (1024 * 1024), 1),
            }
        )
    return videos


@app.route("/")
def index():
    videos = load_videos()
    categories = sorted({v["category"] for v in videos})
    return render_template("index.html", videos=videos, categories=categories)


@app.route("/api/videos")
def api_videos():
    return jsonify(load_videos())


@app.route("/health")
def health():
    # Handy for Docker HEALTHCHECK / Kubernetes probes
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    # 0.0.0.0 so the app is reachable from outside the container
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
