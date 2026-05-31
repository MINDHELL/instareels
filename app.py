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


from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

@bot.on_message(filters.command("start"))
async def start_command(client, message):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎬 Open Reels",
                url="https://distant-sadye-aarshbots01-761e9600.koyeb.app/"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Channel",
                url="https://t.me/Reelsx60"
            ),
            InlineKeyboardButton(
                "ℹ️ About",
                callback_data="about"
            )
        ]
    ])

    await message.reply_photo(
        photo="https://i.ibb.co/ch07bzkf/x.jpg",  # replace with your image URL
        caption="""
🎬 **Welcome to ReelsX**

Watch reels directly from Telegram in a smooth vertical feed.

✨ Features:
• Infinite reels scrolling
• Sound toggle
• Auto-refresh for new uploads
• Fast loading experience

👇 Tap below to start watching.
""",
        reply_markup=keyboard
    )


@bot.on_callback_query(filters.regex("about"))
async def about_callback(client, query):

    await query.answer()

    await query.message.edit_text(
        """
🎬 **ReelsX**

A Telegram-powered reels platform.

🚀 Built with:
• Pyrogram
• Flask
• Swiper.js

Enjoy short videos directly from Telegram channels.
"""
    )




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

            if not os.path.exists(file_path):

                try:

                    print(
                        f"Downloading video {msg.id}"
                    )

                    msg.download(file_path)

                except Exception as e:

                    print(
                        f"Download failed {msg.id}:",
                        e
                    )

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

    try:
        return jsonify(build_cache())

    except Exception as e:

        print("API Error:", e)

        return jsonify(CACHE)


# =========================
# STARTUP
# =========================
load_cache()


# =========================
# RUN
# =========================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
                     )
