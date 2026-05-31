from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 31663048
API_HASH = "bcfb546e78c22c0e141bdd694282e9bc"
SESSION_STRING = "BQHjI8gAiWc44QuMTl7v3OUkY2n6gXzLl6OadGmfPBXG_z5WNfOj8YK6LXja45FqjWp1WNccAAIN_DsE-LxfjgEcufLRFjtTjPEjYjrcEIh3KfzIp8UxtYBoVz6oT_EqBMBe6gWNYe4yHCFudGIZ2D1OX3X07dl4LWAJvw643f2m1zknJrwNGCtJBFTr3Y-foPeoE3rnHEFnZvkHzCP9d9VRyezTS4Zc5TBS18ZwrrbMmAf_EIicUTIyWRm2ZZMhjA14X2-1K7L2m-C_-EMtj33QzxEk6x274S6Jno5KiFD4vL_pY45utc3oeP20WMQXdYtXD3jJV2VB731uZKWR_ZdKFZzCFQAAAAGkK6mgAA"
CHANNEL = "Reelsx60"

bot = Client(
    "reels_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
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
            )
        ]
    ])

    await message.reply_photo(
        photo="https://i.ibb.co/ch07bzkf/x.jpg",
        caption="🎬 Welcome to ReelsX\n\nWatch reels directly from Telegram.",
        reply_markup=keyboard
    )

bot.run()
