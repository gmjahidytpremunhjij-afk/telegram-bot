import os
import yt_dlp
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# ðŸ”‘ ENV à¦¥à§‡à¦•à§‡ token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ðŸ'' à¦¤à§‹à¦®à¦¾à¦° Admin ID
ADMIN_ID = 7454180235

# ðŸ“ user file
USERS_FILE = "users.txt"

# ðŸ‘‰ user save function
def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()

    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")


# âœ… Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # user save
    save_user(user.id)

    username = user.username if user.username else user.first_name

    text = f"""
ðŸ‘‹ à¦†à¦¸à¦¸à¦¾à¦²à¦¾à¦®à§ à¦†à¦²à¦¾à¦‡à¦•à§à¦® {username} à¦¸à§à¦¯à¦¾à¦°!

ðŸ“¥ à¦†à¦ªà¦¨à¦¿ à¦ à¦–à¦¾à¦¨ à¦¥à§‡à¦•à§‡ à¦¡à¦¾à¦‰à¦¨à¦²à§‹à¦¡ à¦•à¦°à¦¤à§‡ à¦ªà¦¾à¦°à¦¬à§‡à¦¨:
âœ” TikTok
âœ” Facebook Short Video

ðŸ”— à¦¶à§ à¦§à§ à¦à¦¿à¦¡à¦¿à¦“ à¦²à¦¿à¦‚à¦• à¦ªà¦¾à¦ à¦¾à¦¨

ðŸ'¨â€ ðŸ'» à¦†à¦®à¦¾à¦•à§‡ à¦¤à§ˆà¦°à¦¿ à¦•à¦°à§‡à¦›à§‡: @JAHIDVAI12
"""
    await update.message.reply_text(text)


# ðŸ‘¥ Users count (admin only)
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not os.path.exists(USERS_FILE):
        count = 0
    else:
        with open(USERS_FILE, "r") as f:
            count = len(f.readlines())

    await update.message.reply_text(f"ðŸ‘¥ Total Users: {count}")


# ðŸŽ¬ Video Download
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    msg = await update.message.reply_text("â³ à¦¡à¦¾à¦‰à¦¨à¦²à§‹à¦¡ à¦¹à¦šà§à¦›à§‡...")

    unique_id = str(uuid.uuid4())
    filename = f"video_{unique_id}.mp4"

    ydl_opts = {
        'outtmpl': filename,
        'format': 'best',
        'quiet': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(filename, 'rb') as f:
            await update.message.reply_video(f)

        os.remove(filename)

    except Exception:
        await msg.edit_text("âŒ à¦­à¦¿à¦¡à¦¿à¦“ à¦¡à¦¾à¦‰à¦¨à¦²à§‹à¦¡ à¦•à¦°à¦¾ à¦¯à¦¾à§Ÿà¦¨à¦¿!")


# ðŸš€ App Setup
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

print("âœ… Bot Running...")
app.run_polling()
