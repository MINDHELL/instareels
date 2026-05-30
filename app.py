from flask import Flask, jsonify, render_template
from pyrogram import Client

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

def get_videos(limit=10):
    videos = []

    with tg:
        for msg in tg.get_chat_history(CHANNEL, limit=50):
            if msg.video:
                file_id = msg.video.file_id
                videos.append({
                    "file_id": file_id,
                    "caption": msg.caption or "Reel"
                })

            if len(videos) >= limit:
                break

    return videos


@app.route("/api/videos")
def videos_api():
    return jsonify(get_videos(10))


@app.route("/")
def home():
    return render_template("reels.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
