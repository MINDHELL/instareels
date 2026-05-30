from flask import Flask, jsonify, render_template
from pyrogram import Client
import os
import json
import threading

app = Flask(__name__)

API_ID = 31663048
API_HASH = "bcfb546e78c22c0e141bdd694282e9bc"
SESSION_STRING = "BQHjI8gAiWc44QuMTl7v3OUkY2n6gXzLl6OadGmfPBXG_z5WNfOj8YK6LXja45FqjWp1WNccAAIN_DsE-LxfjgEcufLRFjtTjPEjYjrcEIh3KfzIp8UxtYBoVz6oT_EqBMBe6gWNYe4yHCFudGIZ2D1OX3X07dl4LWAJvw643f2m1zknJrwNGCtJBFTr3Y-foPeoE3rnHEFnZvkHzCP9d9VRyezTS4Zc5TBS18ZwrrbMmAf_EIicUTIyWRm2ZZMhjA14X2-1K7L2m-C_-EMtj33QzxEk6x274S6Jno5KiFD4vL_pY45utc3oeP20WMQXdYtXD3jJV2VB731uZKWR_ZdKFZzCFQAAAAGkK6mgAA"
CHANNEL = "Reelsx60"

tg = Client(
    "reels",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

CACHE_FILE = "cache.json"
CACHE = []


# =========================
# LOAD FROM DISK CACHE
# =========================
def load_cache():
    global CACHE
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            CACHE = json.load(f)


# =========================
# SAVE CACHE
# =========================
def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(CACHE, f)


# =========================
# FETCH FROM TELEGRAM ONLY ONCE
# =========================
def fetch_once():
    global CACHE

    if CACHE:
        return

    os.makedirs("static/videos", exist_ok=True)

    videos = []

    with tg:
        count = 0

        for msg in tg.get_chat_history(CHANNEL, limit=50):

            if msg.video:

                file_path = f"static/videos/{count}.mp4"

                if not os.path.exists(file_path):
                    msg.download(file_path)

                videos.append({
                    "url": "/" + file_path,
                    "caption": msg.caption or "Reel"
                })

                count += 1

            if count >= 10:
                break

    CACHE = videos
    save_cache()


# =========================
# BACKGROUND LOADER (IMPORTANT)
# =========================
threading.Thread(target=fetch_once).start()


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("reels.html")


@app.route("/api/videos")
def api_videos():
    load_cache()
    return jsonify(CACHE)


# =========================
# START
# =========================
if __name__ == "__main__":
    load_cache()
    app.run(host="0.0.0.0", port=5000)
