# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime
import webbrowser
from threading import Timer

from src.classifier import predict_disaster, predict_help
from src.verifier import verify_event
from src.rule_engine import evaluate_credibility
from src.decision_engine import make_final_decision
from src.notifier import notify_authority
from src.tweet_fetcher import get_latest_post
from src.config import HELP_THRESHOLD

app = Flask(__name__)
app.secret_key = "super_secret_key_change_this"

POSTS_FILE = "data/posts.json"


def ensure_posts_file():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_posts():
    ensure_posts_file()

    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_posts(posts):
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)


def run_pipeline(text, source="manual", username=None):
    disaster_prob = predict_disaster(text)

    verification = verify_event(text)

    rule_result = evaluate_credibility(text)

    decision_result = make_final_decision(
        disaster_prob,
        verification,
        rule_result
    )

    help_prob = 0.0
    email_logs = []

    if decision_result["decision"] == "REAL":
        help_prob = predict_help(text)
        email_logs = notify_authority(text)

    post = {
        "id": str(int(datetime.now().timestamp() * 1000)),
        "text": text,
        "source": source,
        "username": username if username else "",
        "created_at": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
        "disaster_probability": round(disaster_prob, 3),
        "help_probability": round(help_prob, 3),
        "verification_status": verification["status"],
        "verification_confidence": verification["confidence"],
        "final_decision": decision_result["decision"],
        "credibility_score": rule_result["score"],
        "email_logs": email_logs
    }

    posts = load_posts()
    posts.insert(0, post)

    save_posts(posts)

    return post


@app.route("/")
def home():
    posts = load_posts()
    return render_template("index.html", posts=posts)


@app.route("/submit_post", methods=["POST"])
def submit_post():
    text = request.form.get("post_text", "").strip()

    if not text:
        flash("Please enter a post before submitting.", "error")
        return redirect(url_for("home"))

    run_pipeline(text, source="manual")

    flash("Post submitted and analyzed successfully.", "success")

    return redirect(url_for("home"))


@app.route("/fetch_twitter", methods=["POST"])
def fetch_twitter():
    username = request.form.get("twitter_username", "").strip()

    if not username:
        flash("Please enter a Twitter/X username.", "error")
        return redirect(url_for("home"))

    text = get_latest_post(username)

    if not text:
        flash("No disaster-related tweet was fetched from this account.", "error")
        return redirect(url_for("home"))

    run_pipeline(text, source="twitter", username=username)

    flash(
        f"Latest disaster-related tweet from @{username} fetched and analyzed.",
        "success"
    )

    return redirect(url_for("home"))


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    ensure_posts_file()

    Timer(1, open_browser).start()

    app.run(debug=True)