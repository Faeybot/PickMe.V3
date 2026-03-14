from telegram import Update
from telegram.ext import ContextTypes
from services import admin_service, match_service

async def handle_report_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    current_member = context.user_data.get('current_swipe')
    if not current_member:
        await update.message.reply_text("Tidak ada member untuk dilaporkan")
        return

    reporter = current_member[0]  # swiper_id
    reported = current_member[0]  # member_id

    # Simpan report
    admin_service.create_report(reporter, reported, reason="Block oleh user")

    await update.message.reply_text("⚠️ Member ini telah diblokir dan dilaporkan ke admin.")
    # Logika tambahan admin bisa meninjau dan ban otomatis
