import os
from telegram import Update
from telegram.ext import ContextTypes
from services import feed_service
from config import FEED_CHANNEL, FEED_LIMIT_TEXT, FEED_LIMIT_PHOTO

ASSETS_PATH = "assets/"

async def handle_feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    member = feed_service.get_member_by_telegram(telegram_id)
    if not member:
        await update.message.reply_text("Silakan registrasi dulu dengan /start")
        return

    # Cek limit
    if feed_service.check_text_feed_limit(member['id']) >= FEED_LIMIT_TEXT:
        await update.message.reply_text("⚠️ Limit posting teks harian tercapai")
        return
    if update.message.photo and feed_service.check_photo_feed_limit(member['id']) >= FEED_LIMIT_PHOTO:
        await update.message.reply_text("⚠️ Limit posting foto harian tercapai")
        return

    # Posting feed teks
    if update.message.text:
        feed_service.create_feed(member['id'], update.message.text)
        await update.message.reply_text("✅ Feed berhasil diposting!")

    # Posting feed foto
    elif update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        file_path = f"{ASSETS_PATH}/feed_{member['id']}_{photo_file.file_id}.jpg"
        await photo_file.download_to_drive(file_path)
        feed_service.create_feed(member['id'], content=None, photo_path=file_path)
        await update.message.reply_text("✅ Feed foto berhasil diposting!")

    else:
        await update.message.reply_text("Silakan kirim teks atau foto untuk feed.")
