import os
import yt_dlp
import uuid
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7454180235


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.username if user.username else user.first_name

    await update.message.reply_text(f"""
👋 আসসালামু আলাইকুম {name}!

✔ TikTok
✔ Facebook
✔ Instagram

🔗 শুধু ভিডিও লিংক দিন
""")


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not any(x in url for x in ["tiktok.com", "facebook.com", "fb.watch", "instagram.com"]):
        return

    msg = await update.message.reply_text("⏳ প্রসেস হচ্ছে...")

    try:
        # 🔥 Instagram = API
        if "instagram.com" in url:
            api = f"https://api.douyin.wtf/api?url={url}"
            res = requests.get(api).json()
            video = res.get("data", {}).get("play")

            if not video:
                raise Exception("IG fail")

            await update.message.reply_video(video)

        else:
            # 🔥 TikTok + Facebook = yt-dlp
            filename = f"video_{uuid.uuid4()}.%(ext)s"

            ydl_opts = {
                'outtmpl': filename,
                'format': 'best',
                'quiet': True,
                'noplaylist': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info)

            if not file_name.endswith(".mp4"):
                file_name = file_name.rsplit(".", 1)[0] + ".mp4"

            with open(file_name, 'rb') as f:
                await update.message.reply_video(f)

            os.remove(file_name)

    except Exception:
        await msg.edit_text("❌ ভিডিও ডাউনলোড করা যায়নি!")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("✅ Bot Running...")
app.run_polling()
