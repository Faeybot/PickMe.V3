from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services import match_service, user_service
from config import SWIPE_LIMIT

async def handle_swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    swiper = user_service.get_member_by_telegram(telegram_id)
    if not swiper:
        await update.message.reply_text("Silakan registrasi dulu dengan /start")
        return

    if match_service.check_daily_swipe_limit(swiper['id']) >= SWIPE_LIMIT:
        await update.message.reply_text("⚠️ Limit swipe harian tercapai")
        return

    # Ambil member acak
    member = match_service.get_random_member(swiper['id'])
    if not member:
        await update.message.reply_text("😔 Tidak ada member sesuai kriteria")
        return

    # Simpan current swipe
    context.user_data['current_swipe'] = (member['id'], member['username'])

    # Tampilkan profil
    text = f"👤 {member['username']}, {member['age']} tahun\nAbout: {member['about_me']}"
    keyboard = [
        [InlineKeyboardButton("❤️ Like", callback_data="like"),
         InlineKeyboardButton("💬 Comment", callback_data="comment")],
        [InlineKeyboardButton("⛔ Block & Report", callback_data="block")]
    ]

    if member.get('photo_path'):
        await update.message.reply_photo(
            photo=open(member['photo_path'], "rb"),
            caption=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
