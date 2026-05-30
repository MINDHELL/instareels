from flask import Flask, jsonify, render_template
from pyrogram import Client
import os

app = Flask(__name__)

# ======================
# CONFIG (FILL THESE)
# ======================
API_ID = 31663048
API_HASH = "bcfb546e78c22c0e141bdd694282e9bc"
SESSION_STRING = "BQHjI8gAiWc44QuMTl7v3OUkY2n6gXzLl6OadGmfPBXG_z5WNfOj8YK6LXja45FqjWp1WNccAAIN_DsE-LxfjgEcufLRFjtTjPEjYjrcEIh3KfzIp8UxtYBoVz6oT_EqBMBe6gWNYe4yHCFudGIZ2D1OX3X07dl4LWAJvw643f2m1zknJrwNGCtJBFTr3Y-foPeoE3rnHEFnZvkHzCP9d9VRyezTS4Zc5TBS18ZwrrbMmAf_EIicUTIyWRm2ZZMhjA14X2-1K7L2m-C_-EMtj33QzxEk6x274S6Jno5KiFD4vL_pY45utc3oeP20WMQXdYtXD3jJV2VB731uZKWR_ZdKFZzCFQAAAAGkK6mgAA"
CHANNEL = "Reelsx60"


# ======================
# PYROGRAM CLIENT
# ======================
tg = Client(
    "reels",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# ======================
# SIMPLE CACHE
# ======================
CACHE = []

def load_videos(limit=10):
    """
    Fetch latest videos from Telegram channel
    and download them ONCE to server storage.
    """

    global CACHE
    videos = []

    os.makedirs("static/videos", exist_ok=True)

    with tg:
        count = 0

        for msg in tg.get_chat_history(CHANNEL, limit=50):

            if msg.video:

                file_path = f"static/videos/{count}.mp4"

                # download only if not already present
                if not os.path.exists(file_path):
                    msg.download(file_path)

                videos.append({
                    "url": "/" + file_path,
                    "caption": msg.caption or "Reel"
                })

                count += 1

            if count >= limit:
                break

    CACHE = videos


# ======================
# API ENDPOINT
# ======================
@app.route("/api/videos")
def api_videos():
    load_videos()
    return jsonify(CACHE)


# ======================
# FRONTEND ROUTE
# ======================
@app.route("/")
def home():
    return render_template("reels.html")


# ======================
# RUN SERVER
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
