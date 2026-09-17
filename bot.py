import asyncio
import os

from aiohttp import web
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# =========================
# CONFIG
# =========================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

DOMAIN, CODE = range(2)

VALID_DOMAIN = "sksj.com"
VALID_CODE = "12037"


# =========================
# RENDER HEALTH CHECK
# =========================

async def health(request):
    return web.Response(
        text="Askmebet Sale Bot is running!"
    )


# =========================
# /START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    # ตรวจสอบข้อมูล
    checking = await message.reply_text(
        "🔍 <b>กำลังตรวจสอบข้อมูล...</b>\n"
        "⏳ กรุณารอสักครู่",
        parse_mode="HTML"
    )

    await asyncio.sleep(4)
    await checking.delete()

    # ตรวจสอบสำเร็จ
    success = await message.reply_text(
        "✅ <b>ตรวจสอบสำเร็จ!</b>\n\n"
        "คุณกำลังถูกดูแลโดย เอเจนซี่ "
        '<a href="https://t.me/closed7777">@closed7777</a>',
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    await asyncio.sleep(6)
    await success.delete()

    # =========================
    # SALE ON-CALL
    # =========================

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
        [
            InlineKeyboardButton(
                "💬 ติดต่อ Sale On-call",
                url="https://t.me/closed7777"
            )
        ],
        [
            InlineKeyboardButton(
                "🛡️ ช่องทางหลัก / Official",
                url="https://t.me/Askmebetsaleofficial"
            )
        ],
        [
            InlineKeyboardButton(
                "🔐 เข้าสู่หน้าซัพพอร์ต",
                callback_data="support_login"
            )
        ],
    ]

    await message.reply_text(
        sale_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True,
    )

    # =========================
    # รูปต้อนรับ
    # =========================

    await message.reply_photo(
        photo=(
            "https://s.imgz.io/2026/09/17/"
            "1000354828d4067fc0751190c4.jpg"
        ),
        caption=(
            "สวัสดีครับ ยินดีต้อนรับสู่ "
            "<b>Askmebet Sale Official</b> ครับ 👋\n\n"
            "ต้องการประสานงานด้านใดครับ"
        ),
        parse_mode="HTML",
    )


# =========================
# SUPPORT LOGIN
# =========================

async def support_login(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "🔐 <b>เข้าสู่หน้าซัพพอร์ต</b>\n\n"
        "🌐 กรุณากรอก Domain Name\n"
        "ตัวอย่าง: <code>sksj.com</code>",
        parse_mode="HTML",
    )

    return DOMAIN


# =========================
# RECEIVE DOMAIN
# =========================

async def receive_domain(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    domain = update.message.text.strip().lower()

    context.user_data["support_domain"] = domain

    await update.message.reply_text(
        "🔑 <b>กรุณากรอกรหัสที่ได้รับจากเอเจนซี่</b>",
        parse_mode="HTML",
    )

    return CODE


# =========================
# RECEIVE CODE
# =========================

async def receive_code(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    domain = context.user_data.get(
        "support_domain",
        ""
    )

    code = update.message.text.strip()

    # ข้อมูลถูกต้อง
    if domain == VALID_DOMAIN and code == VALID_CODE:

        context.user_data[
            "support_authenticated"
        ] = True

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛠 ติดต่อซัพพอร์ต",
                    url="https://t.me/closed7777"
                )
            ],
            [
                InlineKeyboardButton(
                    "👤 ติดต่อเอเจนซี่",
                    url="https://t.me/closed7777"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚪 ออกจากระบบ",
                    callback_data="support_logout"
                )
            ],
        ]

        await update.message.reply_text(
            "✅ <b>ยืนยันสำเร็จ!</b>\n\n"
            "🌐 Domain: <code>sksj.com</code>\n"
            "🟢 สถานะระบบ: <b>เปิดใช้งาน</b>\n\n"
            "ยินดีต้อนรับเข้าสู่หน้าซัพพอร์ตครับ",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # ข้อมูลไม่ถูกต้อง
    else:

        context.user_data.clear()

        await update.message.reply_text(
            "❌ <b>ข้อมูลไม่ถูกต้อง</b>\n\n"
            "Domain หรือรหัสไม่ตรงกับข้อมูลที่ได้รับจากเอเจนซี่\n"
            "กรุณากด /start แล้วลองใหม่อีกครั้งครับ",
            parse_mode="HTML",
        )

    return ConversationHandler.END


# =========================
# CANCEL
# =========================

async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data.clear()

    await update.message.reply_text(
        "❌ ยกเลิกการเข้าสู่ระบบแล้วครับ"
    )

    return ConversationHandler.END


# =========================
# LOGOUT
# =========================

async def logout(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    context.user_data.clear()

    await query.message.reply_text(
        "🚪 ออกจากระบบซัพพอร์ตเรียบร้อยแล้วครับ"
    )


# =========================
# MAIN
# =========================

async def main():

    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # =========================
    # SUPPORT LOGIN HANDLER
    # =========================

    login_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                support_login,
                pattern="^support_login$"
            )
        ],

        states={
            DOMAIN: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receive_domain
                )
            ],

            CODE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receive_code
                )
            ],
        },

        fallbacks=[
            CommandHandler(
                "cancel",
                cancel
            )
        ],
    )

    # =========================
    # BOT HANDLERS
    # =========================

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        login_handler
    )

    app.add_handler(
        CallbackQueryHandler(
            logout,
            pattern="^support_logout$"
        )
    )

    # =========================
    # RENDER WEB SERVER
    # =========================

    web_app = web.Application()

    web_app.router.add_get(
        "/",
        health
    )

    web_app.router.add_get(
        "/health",
        health
    )

    runner = web.AppRunner(web_app)

    await runner.setup()

    port = int(
        os.getenv(
            "PORT",
            "10000"
        )
    )

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    print(
        "🤖 Askmebet Sale Bot is running..."
    )

    print(
        f"🌐 Render server listening on port {port}"
    )

    # =========================
    # START TELEGRAM BOT
    # =========================

    await app.initialize()

    await app.start()

    await app.updater.start_polling()

    try:

        await asyncio.Event().wait()

    finally:

        await app.updater.stop()

        await app.stop()

        await app.shutdown()

        await runner.cleanup()


# =========================
# RUN
# =========================

if __name__ == "__main__":
    asyncio.run(main())
