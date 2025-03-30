# main.py
import asyncio
import nest_asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from assistant_pc import setup_handlers as setup_assistant_handlers, assistant_pc
from educational_mode import setup_handlers as setup_educational_handlers, start_educational_mode
from game import setup_handlers as setup_game_handlers, start_game_mode

# Применение nest_asyncio для сред с уже запущенным циклом событий
nest_asyncio.apply()

# Исходное приветственное сообщение (главное меню)
MAIN_MENU_TEXT = (
    "Привет! Я Академия ПК – ваш надёжный помощник в мире компьютерных технологий.\n\n"
    "Я могу помочь вам пошагово собрать персональный компьютер, учитывая особенности ваших комплектующих. "
    "Также я предлагаю два обучающих режима и интерактивное тестирование:\n\n"
    "• Ассистент сборки ПК – подробная инструкция по сборке компьютера.\n"
    "• Обучающий режим – выберите один из обучающих курсов (Базовый, Продвинутый, Профессиональный) для получения полной обучающей информации и прохождения теста.\n"
    "• Интерактивный режим – сборка ПК по выбранному бюджету с интерактивными выборами комплектующих.\n\n"
    "Выберите режим работы:"
)

def build_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Ассистент сборки ПК", callback_data="assistant_pc")],
        [InlineKeyboardButton("Обучающий режим", callback_data="educational_mode")],
        [InlineKeyboardButton("Интерактивный режим", callback_data="game_mode")]
    ])

async def start_main_menu(update, context):
    await update.effective_message.reply_text(MAIN_MENU_TEXT, reply_markup=build_main_menu_keyboard(), parse_mode='HTML')

async def main_menu_handler(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "assistant_pc":
        await assistant_pc(update, context)
    elif data == "educational_mode":
        await start_educational_mode(update, context)
    elif data == "game_mode":
        await start_game_mode(update, context)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем обработчики для всех режимов
    setup_assistant_handlers(app)
    setup_educational_handlers(app)
    setup_game_handlers(app)

    # Главное меню: команда /start и выбор режима
    app.add_handler(CommandHandler("start", start_main_menu))
    app.add_handler(CallbackQueryHandler(main_menu_handler, pattern="^(assistant_pc|educational_mode|game_mode)$"))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())