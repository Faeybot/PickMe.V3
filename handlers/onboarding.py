import os
from telegram import Update
from telegram.ext import ContextTypes
from services import user_service

ASSETS_PATH = "assets/"

async def handle_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    text = update.message.text
    state = context.user_data.get('registration_step', 'username')

    # Kirim logo saat mulai registrasi
    if state == 'username' and 'registration_step' not in context.user_data:
        logo_file = os.path.join(ASSETS_PATH, "logo_pickme.png")
        if os.path.exists(logo_file):
            await update.message.reply_photo(
                photo=open(logo_file, "rb"),
                caption="Selamat datang! Silakan masukkan username Anda:"
            )
        else:
            await update.message.reply_text("Selamat datang! Silakan masukkan username Anda:")
        context.user_data['registration_step'] = 'username'
        return

    # Step registrasi
    if state == 'username':
        context.user_data['username'] = text
        context.user_data['registration_step'] = 'age'
        await update.message.reply_text("Masukkan usia Anda:")
    elif state == 'age':
        if text.isdigit():
            context.user_data['age'] = int(text)
            context.user_data['registration_step'] = 'gender'
            await update.message.reply_text("Masukkan gender (L/P):")
        else:
            await update.message.reply_text("Usia harus berupa angka. Coba lagi:")
    elif state == 'gender':
        if text.upper() in ['L','P']:
            context.user_data['gender'] = text.upper()
            context.user_data['registration_step'] = 'interest'
            await update.message.reply_text("Masukkan minat Anda (misal: musik, olahraga):")
        else:
            await update.message.reply_text("Gender harus L atau P. Coba lagi:")
    elif state == 'interest':
        context.user_data['interest'] = text
        context.user_data['registration_step'] = 'about_me'
        await update.message.reply_text("Tulis About Me singkat Anda:")
    elif state == 'about_me':
        context.user_data['about_me'] = text
        context.user_data['registration_step'] = 'photo'
        await update.message.reply_text("Kirim foto profil Anda:")
    elif state == 'photo' and update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        file_path = f"{ASSETS_PATH}/user_{telegram_id}.jpg"
        await photo_file.download_to_drive(file_path)
        context.user_data['photo'] = file_path

        # Simpan member ke database
        user_service.create_member(
            telegram_id=telegram_id,
            username=context.user_data['username'],
            age=context.user_data['age'],
            gender=context.user_data['gender'],
            interest=context.user_data['interest'],
            about_me=context.user_data['about_me'],
            photo_path=file_path
        )

        await update.message.reply_text("✅ Registrasi selesai! Gunakan /feed atau /swipe untuk mulai.")
        context.user_data.clear()
    else:
        await update.message.reply_text("Silakan kirim foto profil Anda.")
