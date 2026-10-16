"""
Web Portofolio Personal Dinamis & Interaktif
Entry point Flask application.
"""
import json
from pathlib import Path

from flask import Flask, render_template, jsonify, abort

from config import Config

# ============================================
# KONFIGURASI
# ============================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = Flask(__name__)
app.config.from_object(Config)


# ============================================
# HELPER — Baca JSON
# ============================================
def load_json(filename):
    """Baca file JSON dari folder data/."""
    filepath = DATA_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_profile():
    return load_json("profile.json")


def get_projects():
    return load_json("projects.json")


def get_project_by_id(project_id):
    projects = get_projects()
    for p in projects:
        if p["id"] == project_id:
            return p
    return None


def get_skills():
    return load_json("skills.json")


# ============================================
# ROUTING — Halaman HTML
# ============================================
@app.route("/")
def index():
    return render_template(
        "index.html",
        profile=get_profile(),
        projects=get_projects()[:1],   # preview: 1 proyek saja
        skills=get_skills()[:3],       # preview: 3 skill saja
    )


@app.route("/about")
def about():
    return render_template("about.html", profile=get_profile())


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=get_projects())


@app.route("/projects/<int:project_id>")
def project_detail(project_id):
    project = get_project_by_id(project_id)
    if project is None:
        abort(404)
    return render_template("project_detail.html", project=project)


@app.route("/skills")
def skills():
    return render_template("skills.html", skills=get_skills())


@app.route("/contact")
def contact():
    return render_template("contact.html", profile=get_profile())


# ============================================
# ROUTING — API JSON
# ============================================
@app.route("/api/profile")
def api_profile():
    return jsonify(get_profile())


@app.route("/api/projects")
def api_projects():
    return jsonify(get_projects())


@app.route("/api/projects/<int:project_id>")
def api_project_detail(project_id):
    project = get_project_by_id(project_id)
    if project is None:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project)


@app.route("/api/skills")
def api_skills():
    return jsonify(get_skills())


# ============================================
# ENTRY POINT
# ============================================
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)