from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, CommandHandler, ConversationHandler, filters
from utils.logger import logger
from locales.locales import LOCALES
from utils.storage import save_user_record
from config import settings

# States
LANG, COUNTRY, NICK, LEVEL = range(4)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = LOCALES["EN"]["greeting"]
    keyboard = [
        [
            InlineKeyboardButton(LOCALES["RU"]["btn_ru"], callback_data="lang_RU"),
            InlineKeyboardButton(LOCALES["EN"]["btn_en"], callback_data="lang_EN"),
        ]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    logger.info(f"User {user.id} started conversation")
    return LANG

async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    data = query.data 
    lang = data.split("_", 1)[1] if "_" in data else "EN"
    context.user_data["lang"] = lang
    context.user_data["answers"] = {}
    logger.info(f"User {user.id} selected language {lang}")

    ask = LOCALES[lang]["ask_country"]
    await query.message.reply_text(ask)
    return COUNTRY

async def country_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.user_data.get("lang", "EN")
    text = update.message.text.strip()
    context.user_data["answers"]["country"] = text
    logger.info(f"User {user.id} country: {text}")

    await update.message.reply_text(LOCALES[lang]["ask_nick"])
    return NICK

async def nick_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.user_data.get("lang", "EN")
    text = update.message.text.strip()
    context.user_data["answers"]["nick"] = text
    logger.info(f"User {user.id} nick: {text}")

    await update.message.reply_text(LOCALES[lang]["ask_level"])
    return LEVEL

async def level_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.user_data.get("lang", "EN")
    text = update.message.text.strip()
    context.user_data["answers"]["level"] = text
    logger.info(f"User {user.id} level: {text}")

    record = {
        "user_id": user.id,
        "language": lang,
        "answers": context.user_data["answers"],
    }
    save_user_record(record, settings.RESULTS_FILE)

    verify_label = LOCALES[lang]["verify_label"]
    keyboard = [
        [InlineKeyboardButton(verify_label, url=settings.VERIFY_URL)]
    ]
    await update.message.reply_text(verify_label, reply_markup=InlineKeyboardMarkup(keyboard))

    context.user_data.clear()
    return ConversationHandler.END

async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.user_data.get("lang", "EN")
    await update.message.reply_text(LOCALES[lang]["cancel"])
    context.user_data.clear()
    logger.info(f"User {user.id} cancelled conversation")
    return ConversationHandler.END

def get_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            LANG: [CallbackQueryHandler(language_choice, pattern="^lang_")],
            COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, country_handler)],
            NICK: [MessageHandler(filters.TEXT & ~filters.COMMAND, nick_handler)],
            LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, level_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)],
        allow_reentry=True,
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/cancel - Cancel current flow"
    )
