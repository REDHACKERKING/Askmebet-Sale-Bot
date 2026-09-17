import asyncio
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    checking = await message.reply_text(
        "🔍 <b>กำลังตรวจสอบข้อมูล...</b>\n"
        "⏳ กรุณารอสักครู่",
        parse_mode="HTML",
    )

    await asyncio.sleep(2)
    await checking.delete()

    success = await message.reply_text(
        "✅ <b>ตรวจสอบสำเร็จ!</b>\n\n"
        "คุณกำลังถูกดูแลโดย เอเจนซี่ "
        '<a href="https://t.me/closed7777">@closed7777</a>',
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    await asyncio.sleep(2)
    await success.delete()

    sale_text = """👤 <b>Sale On-call ประจำสัปดาห์นี้</b>
──────────────
📅 วันเสาร์ ที่ 12/09/2026
➡️ @closed7777

📅 วันอาทิตย์ ที่ 13/09/2026
➡️ @closed7777

🕛 ให้บริการ เสาร์–อาทิตย์ 12:00–20:00 น. (GMT+7)
👉 แตะปุ่มด้านล่างเพื่อทักแชทได้เลยครับ

━━━━━━━━━━━━━━

👤 <b>This week's Sale On-call</b>
──────────────
📅 Sat 12/09/2026
➡️ @closed7777

📅 Sun 13/09/2026
➡️ @closed7777

🕛 Available Sat–Sun 12:00–20:00 (GMT+7)
👉 Tap a button below to start a chat.

🛡️ <b>ช่องทางทางการ / Official:</b>
@Askmebetsaleofficial"""

    keyboard = [
        [InlineKeyboardButton("💬 ติดต่อ Sale On-call", url="https://t.me/closed7777")],
        [InlineKeyboardButton("🛡️ ช่องทางหลัก / Official", url="https://t.me/Askmebetsaleofficial")],
    ]

    await message.reply_text(
        sale_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True,
    )

    photo_url = "https://s.imgz.io/2026/09/17/1000354828d4067fc0751190c4.jpg"
    welcome_text = (
        "สวัสดีครับ ยินดีต้อนรับสู่ <b>Askmebet Sale Official</b> ครับ 👋\n\n"
        "ต้องการประสานงานด้านใดครับ"
    )

    await message.reply_photo(
        photo=photo_url,
        caption=welcome_text,
        parse_mode="HTML",
    )


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("🤖 Askmebet Sale Bot is running...")
app.run_polling()
