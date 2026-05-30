from flask import Flask, jsonify, render_template
from pyrogram import Client
import os
import json

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE_DIR, "static", "videos")
CACHE_FILE = os.path.join(BASE_DIR, "cache.json")

CACHE = []


# =========================
# SAFE CACHE LOAD
# =========================
def load_cache():
    global CACHE
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            CACHE = json.load(f)


def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(CACHE, f)


# =========================
# SAFE DOWNLOAD FUNCTION
# =========================
def build_cache():

    global CACHE

    if CACHE:
        return CACHE

    os.makedirs(VIDEO_DIR, exist_ok=True)

    videos = []

    with tg:
        count = 0

        for msg in tg.get_chat_history(CHANNEL, limit=50):

            if msg.video:

                file_path = os.path.join(VIDEO_DIR, f"{count}.mp4")

                # download safely (NO temp issues)
                if not os.path.exists(file_path):
                    try:
                        msg.download(file_path)
                    except Exception as e:
                        print("Download failed:", e)
                        continue

                videos.append({
                    "url": f"/static/videos/{count}.mp4",
                    "caption": msg.caption or "Reel"
                })

                count += 1

            if count >= 10:
                break

    CACHE = videos
    save_cache()

    return CACHE


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("reels.html")


@app.route("/api/videos")
def api_videos():
    return jsonify(build_cache())


# =========================
# STARTUP SAFE LOAD (NO DOWNLOAD)
# =========================
load_cache()


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
