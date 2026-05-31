from flask import Flask, jsonify, render_template
from pyrogram import Client
import os, json, threading, time

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
DOWNLOADING = set()
LOCK = threading.Lock()


# ---------------- CACHE ----------------
def load_cache():
    global CACHE
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                CACHE = json.load(f)
        except:
            CACHE = []


def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(CACHE, f, indent=2)


# ---------------- TG CONNECT ----------------
def ensure_tg():
    if not tg.is_connected:
        tg.start()


# ---------------- BACKGROUND DOWNLOADER ----------------
def background_loader():
    global CACHE

    ensure_tg()
    os.makedirs(VIDEO_DIR, exist_ok=True)

    while True:
        try:
            for msg in tg.get_chat_history(CHANNEL, limit=100):

                if not msg.video:
                    continue

                file_id = str(msg.id)

                file_path = os.path.join(VIDEO_DIR, f"{file_id}.mp4")

                with LOCK:
                    exists = any(v["id"] == file_id for v in CACHE)

                if exists:
                    continue

                # mark downloading
                if file_id in DOWNLOADING:
                    continue

                DOWNLOADING.add(file_id)

                try:
                    if not os.path.exists(file_path):
                        print("Downloading", file_id)
                        msg.download(file_path)

                    data = {
                        "id": file_id,
                        "url": f"/static/videos/{file_id}.mp4",
                        "caption": msg.caption or "Reel"
                    }

                    with LOCK:
                        CACHE.append(data)
                        save_cache()

                    print("Finished", file_id)

                except Exception as e:
                    print("Download error:", e)

                finally:
                    DOWNLOADING.discard(file_id)

            time.sleep(30)  # refresh loop

        except Exception as e:
            print("Worker error:", e)
            time.sleep(10)


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("reels.html")


@app.route("/api/videos")
def api_videos():
    with LOCK:
        return jsonify(sorted(CACHE, key=lambda x: x["id"], reverse=True))


# ---------------- START ----------------
load_cache()

threading.Thread(target=background_loader, daemon=True).start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
