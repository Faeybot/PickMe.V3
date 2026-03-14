import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
from config import TOKEN, FEED_LIMIT_TEXT, FEED_LIMIT_PHOTO, SWIPE_LIMIT, FEED_CHANNEL, ADMIN_CHANNEL
from database import init_db
from handlers import onboarding, feed, dating, report_block
from services import user_service, feed_service, match_service, admin_service
from utils import limiter

ASSETS_PATH = "assets/"

# ==============================
# Bot State (in-memory)
# ==============================
user_state = {}

# ==============================
# Command /start
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    member = user_service.get_member_by_telegram(telegram_id)

    logo_file = os.path.join(ASSETS_PATH, "logo_pickme.png")

    if member:
        # Welcome back dengan logo
        if os.path.exists(logo_file):
            await update.message.reply_photo(
                photo=open(logo_file, "rb"),
                caption=(
                    f"👋 Selamat datang kembali, {member['username']}!\n\n"
                    "/feed - Posting feed\n"
                    "/swipe - Mulai dating\n"
                    "/report - Block/report member"
                )
            )
        else:
            await update.message.reply_text(
                f"👋 Selamat datang kembali, {member['username']}!\n\n"
                "/feed - Posting feed\n"
                "/swipe - Mulai dating\n"
                "/report - Block/report member"
            )
    else:
        # Mulai registrasi
        user_state[telegram_id] = "register_username"
        await update.message.reply_text(
            "Selamat datang di PickMe! Silakan masukkan username Anda:"
        )

# ==============================
# Handle messages
# ==============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    text = update.message.text

    # Registrasi
    if telegram_id in user_state:
        await onboarding.handle_registration(update, context)
        return

    # Command Feed
    if text.lower() == "/feed":
        feed_icon = os.path.join(ASSETS_PATH, "icon_feed.png")
        if os.path.exists(feed_icon):
            await update.message.reply_photo(
                photo=open(feed_icon, "rb"),
                caption="📢 Silakan posting feed Anda"
            )
        else:
            await update.message.reply_text("📢 Silakan posting feed Anda")
        await feed.handle_feed(update, context)
        return

    # Command Swipe/Dating
    if text.lower() == "/swipe":
        dating_icon = os.path.join(ASSETS_PATH, "icon_dating.png")
        if os.path.exists(dating_icon):
            await update.message.reply_photo(
                photo=open(dating_icon, "rb"),
                caption="❤️ Mulai swipe member lain"
            )
        else:
            await update.message.reply_text("❤️ Mulai swipe member lain")
        await dating.handle_swipe(update, context)
        return

    # Report/Block
    if text.lower().startswith("/report"):
        await report_block.handle_report_block(update, context)
        return

    # Default
    await update.message.reply_text("Gunakan command /feed, /swipe, atau /report")

# ==============================
# Callback query (like/comment/block)
# ==============================
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = query.from_user.id
    data = query.data

    current_member = context.user_data.get('current_swipe')
    if not current_member:
        await query.answer("Tidak ada member untuk aksi ini")
        return

    member_id = current_member[0]
    swiper = user_service.get_member_by_telegram(telegram_id)
    if not swiper:
        await query.answer("Silakan registrasi terlebih dahulu")
        return

    # Action
    if data == "like":
        match_service.record_swipe(swiper['id'], member_id, "like")
        await query.answer("❤️ Anda menyukai member ini")
    elif data == "comment":
        match_service.record_swipe(swiper['id'], member_id, "comment")
        await query.answer("💬 Komentar dikirim (placeholder)")
    elif data == "block":
        match_service.record_swipe(swiper['id'], member_id, "block")
        await query.answer("⛔ Member diblokir dan dilaporkan ke admin")
        await report_block.handle_report_block(update, context)

    # Tampilkan member berikutnya
    await dating.handle_swipe(update, context)

# ==============================
# Main
# ==============================
def main():
    # Init DB
    init_db()

    # Init bot
    app = ApplicationBuilder().token(TOKEN).build()

    # Command handler
    app.add_handler(CommandHandler("start", start))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Callback query handler
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("PickMe V3 FINAL running with assets...")
    app.run_polling()

if __name__ == "__main__":
    main()
