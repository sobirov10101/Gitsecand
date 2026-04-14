import telebot
from telebot import types
from deep_translator import GoogleTranslator

# 1. Initialize the bot with your token
TOKEN = '8446669118:AAFhjXooYEnykm0Uqy4wwZXi2osjGYeSJoo'
bot = telebot.TeleBot(TOKEN)

# Dictionary to store the user's selected language mode
user_modes = {}

# 2. Command /start - Show the buttons
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_en_uz = types.KeyboardButton("🇬🇧 English -> 🇺🇿 Uzbek")
    btn_uz_en = types.KeyboardButton("🇺🇿 Uzbek -> 🇬🇧 English")
    markup.add(btn_en_uz, btn_uz_en)
    
    bot.reply_to(message, "Welcome! Please choose a translation direction using the buttons below:", reply_markup=markup)

# 3. Handle button clicks to set the translation mode
@bot.message_handler(func=lambda message: message.text in ["🇬🇧 English -> 🇺🇿 Uzbek", "🇺🇿 Uzbek -> 🇬🇧 English"])
def set_mode(message):
    if "English -> Uzbek" in message.text:
        user_modes[message.chat.id] = 'en-uz'
        bot.send_message(message.chat.id, "Mode set: **English to Uzbek**. Send me English text!")
    else:
        user_modes[message.chat.id] = 'uz-en'
        bot.send_message(message.chat.id, "Mode set: **Uzbek to English**. Send me Uzbek text!")

# 4. Handle text translation
@bot.message_handler(func=lambda message: True)
def translate_text(message):
    chat_id = message.chat.id
    mode = user_modes.get(chat_id)

    if not mode:
        bot.reply_to(message, "Please select a translation direction first using the buttons!")
        return

    try:
        # Determine source and target languages
        src, dest = ('en', 'uz') if mode == 'en-uz' else ('uz', 'en')
        
        # Translate the text
        translated = GoogleTranslator(source=src, target=dest).translate(message.text)
        
        bot.reply_to(message, f"✅ **Translation:**\n\n{translated}", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, "❌ Sorry, an error occurred during translation. Please try again later.")

# 5. Start the bot
print("Bot is running...")
bot.infinity_polling()