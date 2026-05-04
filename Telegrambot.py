import os
import logging
import tempfile
import asyncio
from dotenv import load_dotenv
load_dotenv()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)
import httpx
 
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
 
WAITING_VOICE = 1
WAITING_TEXT = 2
 
user_data_store = {}
 
 
async def clone_voice_elevenlabs(audio_bytes: bytes, voice_name: str, api_key: str) -> str:
    url = "https://api.elevenlabs.io/v1/voices/add"
    async with httpx.AsyncClient(timeout=60.0) as client:
        headers = {"xi-api-key": api_key}
        files = [
            ("files", ("voice.mp3", audio_bytes, "audio/mpeg")),
            ("name", (None, voice_name)),
        ]
        response = await client.post(url, headers=headers, files=files)
        if response.status_code != 200:
            logger.error(f"ElevenLabs clone xato: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()["voice_id"]
 
 
async def text_to_speech_elevenlabs(text: str, voice_id: str, api_key: str) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.95,
            "style": 0.3,
            "use_speaker_boost": True,
        },
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.content
 
 
async def delete_voice_elevenlabs(voice_id: str, api_key: str):
    url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
    headers = {"xi-api-key": api_key}
    async with httpx.AsyncClient(timeout=30.0) as client:
        await client.delete(url, headers=headers)
 
 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"👋 Salom, {user.first_name}!\n\n"
        "🎙️ *Ovoz Klonlash Boti*ga xush kelibsiz!\n\n"
        "Bu bot sizning ovozingizni tahlil qilib, "
        "istalgan matnni *sizning ovozingizda* o'qib beradi.\n\n"
        "📋 *Qanday ishlaydi:*\n"
        "1️⃣ Ovoz xabar yuboring (kamida 10 soniya)\n"
        "2️⃣ O'qitilishini kuting\n"
        "3️⃣ Matn yozing\n"
        "4️⃣ Botingiz ovozda eshiting! 🎵\n\n"
        "▶️ Boshlash uchun /clone buyrug'ini yuboring"
    )
    keyboard = [[InlineKeyboardButton("🎙️ Ovoz Klonlashni Boshlash", callback_data="start_clone")]]
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
 
 
async def start_clone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
    else:
        message = update.message
    text = (
        "🎤 *1-QADAM: Ovoz Namunasini Yuboring*\n\n"
        "• Kamida *15-30 soniya* gapiring\n"
        "• Aniq va baland ovozda gapiring\n"
        "• Shovqinsiz joyda yozing\n\n"
        "🔴 Hozir ovoz xabar yuboring..."
    )
    await message.reply_text(text, parse_mode="Markdown")
    return WAITING_VOICE
 
 
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    api_key = os.getenv("ELEVENLABS_API_KEY", "")
 
    if not api_key:
        await update.message.reply_text("❌ ElevenLabs API kaliti topilmadi.")
        return ConversationHandler.END
 
    processing_msg = await update.message.reply_text("⏳ Ovozingiz tahlil qilinmoqda...")
 
    try:
        voice = update.message.voice or update.message.audio
        if not voice:
            await processing_msg.edit_text("❌ Ovoz fayli topilmadi.")
            return WAITING_VOICE
 
        file = await context.bot.get_file(voice.file_id)
        
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
            await file.download_to_drive(tmp.name)
            tmp_path = tmp.name
 
        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()
        os.unlink(tmp_path)
 
        await processing_msg.edit_text("🔄 Ovozingiz klonlanmoqda...")
 
        voice_name = f"user_{user_id}"
        voice_id = await clone_voice_elevenlabs(audio_bytes, voice_name, api_key)
 
        user_data_store[user_id] = {"voice_id": voice_id}
 
        await processing_msg.edit_text(
            "✅ *Ovozingiz muvaffaqiyatli klonlandi!*\n\n"
            "📝 Endi matn yozing — uni sizning ovozingizda o'qib beraman!",
            parse_mode="Markdown"
        )
        return WAITING_TEXT
 
    except httpx.HTTPStatusError as e:
        logger.error(f"ElevenLabs xato: {e.response.status_code} - {e.response.text}")
        if e.response.status_code == 422:
            await processing_msg.edit_text("❌ Ovoz juda qisqa. Kamida 15 soniya gapiring.")
        else:
            await processing_msg.edit_text(f"❌ API xatosi: {e.response.status_code}\n{e.response.text[:200]}")
        return WAITING_VOICE
 
    except Exception as e:
        logger.error(f"Xato: {e}")
        await processing_msg.edit_text(f"❌ Xato: {str(e)[:200]}")
        return WAITING_VOICE
 
 
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    api_key = os.getenv("ELEVENLABS_API_KEY", "")
 
    if user_id not in user_data_store:
        await update.message.reply_text("❌ Avval /clone bilan ovoz yuboring.")
        return ConversationHandler.END
 
    text = update.message.text.strip()
    if len(text) < 2:
        await update.message.reply_text("❌ Matn juda qisqa.")
        return WAITING_TEXT
    if len(text) > 2500:
        await update.message.reply_text(f"❌ Matn juda uzun ({len(text)}/2500).")
        return WAITING_TEXT
 
    processing_msg = await update.message.reply_text("🎵 Audio yaratilmoqda...")
 
    try:
        voice_id = user_data_store[user_id]["voice_id"]
        audio_bytes = await text_to_speech_elevenlabs(text, voice_id, api_key)
 
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
 
        await processing_msg.delete()
 
        with open(tmp_path, "rb") as f:
            await update.message.reply_voice(voice=f, caption="🎙️ Klonlangan ovozingiz")
 
        os.unlink(tmp_path)
 
        keyboard = [
            [InlineKeyboardButton("📝 Yana matn", callback_data="new_text")],
            [InlineKeyboardButton("🎤 Yangi ovoz", callback_data="start_clone")],
        ]
        await update.message.reply_text("✅ Tayyor!", reply_markup=InlineKeyboardMarkup(keyboard))
        return WAITING_TEXT
 
    except Exception as e:
        logger.error(f"TTS xato: {e}")
        await processing_msg.edit_text(f"❌ Xato: {str(e)[:200]}")
        return WAITING_TEXT
 
 
async def new_text_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    if user_id not in user_data_store:
        await query.message.reply_text("❌ /clone bilan ovoz yuboring.")
        return ConversationHandler.END
    await query.message.reply_text("📝 Matn yozing:")
    return WAITING_TEXT
 
 
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_data_store:
        api_key = os.getenv("ELEVENLABS_API_KEY", "")
        if api_key:
            try:
                await delete_voice_elevenlabs(user_data_store[user_id]["voice_id"], api_key)
            except Exception:
                pass
        del user_data_store[user_id]
    await update.message.reply_text("❌ Bekor qilindi. /clone bilan qayta boshlang.")
    return ConversationHandler.END
 
 
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Buyruqlar:*\n"
        "/start - Boshlash\n"
        "/clone - Ovoz klonlash\n"
        "/cancel - Bekor qilish\n"
        "/help - Yordam",
        parse_mode="Markdown"
    )
 
 
def main():
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
 
    if not telegram_token:
        raise ValueError("8715420286:AAFuu3AyGp1POXm4vtt-HGeORlr0dEZaua0")
    if not elevenlabs_key:
        raise ValueError("sk_4ce758b6a9dd4097284903cd5a548d42cd5ff174caeb8322")
 
    app = Application.builder().token(telegram_token).build()
 
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("clone", start_clone),
            CallbackQueryHandler(start_clone, pattern="^start_clone$"),
        ],
        states={
            WAITING_VOICE: [
                MessageHandler(filters.VOICE | filters.AUDIO, handle_voice),
            ],
            WAITING_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text),
                CallbackQueryHandler(new_text_callback, pattern="^new_text$"),
                CallbackQueryHandler(start_clone, pattern="^start_clone$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
 
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(conv_handler)
 
    logger.info("🤖 Bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
 
 
if __name__ == "__main__":
    main()