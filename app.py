from flask import Flask, jsonify, render_template
from pyrogram import Client
import os
import json
import threading
import time


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


# new lines
import threading

download_lock = threading.Lock()

def background_download():

    if not download_lock.acquire(blocking=False):
        return

    try:

        ensure_connected()

        for msg in tg.get_chat_history(CHANNEL, limit=50):

            if not msg.video:
                continue

            filename = f"{msg.id}.mp4"

            file_path = os.path.join(
                VIDEO_DIR,
                filename
            )

            if os.path.exists(file_path):
                continue

            print(f"Downloading {msg.id}")

            try:
                msg.download(file_path)
                print(f"Finished {msg.id}")

            except Exception as e:
                print("Download error:", e)

    finally:
        download_lock.release()

#new
def cache_updater():

    while True:

        try:
            build_cache()

        except Exception as e:
            print("Cache updater:", e)

        time.sleep(60)





# =========================
# CACHE LOAD
# =========================
def load_cache():
    global CACHE

    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                CACHE = json.load(f)
        except:
            CACHE = []


def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            CACHE,
            f,
            ensure_ascii=False,
            indent=2
        )


# =========================
# TELEGRAM CONNECT
# =========================
def ensure_connected():

    try:
        if not tg.is_connected:
            tg.start()
    except Exception as e:
        print("Telegram connection error:", e)

def download_video(msg, file_path):

    try:
        print(f"Downloading {msg.id}")
        msg.download(file_path)
        print(f"Finished {msg.id}")

    except Exception as e:
        print("Download error:", e)




# =========================
# BUILD VIDEO CACHE
# =========================

def build_cache():

    global CACHE

    os.makedirs(VIDEO_DIR, exist_ok=True)

    ensure_connected()

    videos = []

    try:

        count = 0

        for msg in tg.get_chat_history(CHANNEL, limit=50):

            if not msg.video:
                continue

            filename = f"{msg.id}.mp4"

            file_path = os.path.join(
                VIDEO_DIR,
                filename
            )

            # Download in background
            if not os.path.exists(file_path):

                threading.Thread(
                    target=download_video,
                    args=(msg, file_path),
                    daemon=True
                ).start()

                continue

            videos.append({
                "url": f"/static/videos/{filename}",
                "caption": msg.caption or "Reel"
            })

            count += 1

            if count >= 20:
                break

        CACHE = videos

        save_cache()

        return videos

    except Exception as e:

        print("Cache build error:", e)

        return CACHE




# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("reels.html")


@app.route("/api/videos")
def api_videos():
    return jsonify(CACHE) 


# =========================
# STARTUP
# =========================
load_cache()

threading.Thread(
    target=cache_updater,
    daemon=True
).start()


# =========================
# RUN
# =========================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
                     )
