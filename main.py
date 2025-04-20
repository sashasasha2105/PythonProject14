# main.py
import asyncio
import nest_asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN
from assistant_pc import setup_handlers as setup_assistant_handlers, assistant_pc
from educational_mode import setup_handlers as setup_educational_handlers, start_educational_mode
from game import setup_handlers as setup_game_handlers, start_game_mode

# Применяем nest_asyncio для сред, где цикл уже запущен
nest_asyncio.apply()

# ——————————————————————————————————————————————————————————————————————
# Текст приветствия и клавиатура главного меню
# ——————————————————————————————————————————————————————————————————————
MAIN_MENU_TEXT = (
    "<b>Я Академия ПК – ваш надёжный помощник в мире компьютерных технологий. 🤖</b>\n\n"
    "Я помогу вам <i>шаг за шагом собрать персональный компьютер</i>, учитывая особенности ваших комплектующих.\n"
    "Также предлагаю два обучающих режима и интерактивное тестирование:\n\n"
    "• <b>Ассистент сборки ПК</b> – подробная инструкция по сборке компьютера.\n"
    "• <b>Обучающий режим</b> – выбор одного из курсов (Базовый, Продвинутый, Профессиональный).\n"
    "• <b>Интерактивный режим</b> – сборка ПК по выбранному бюджету и задаче.\n\n"
    "Выберите режим работы:"
)

def build_main_menu_keyboard() -> InlineKeyboardMarkup:
    # По одной кнопке на строку, чтобы текст полностью виден
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Ассистент сборки ПК",   callback_data="assistant_pc")],
        [InlineKeyboardButton("Обучающий режим",       callback_data="educational_mode")],
        [InlineKeyboardButton("Интерактивный режим",   callback_data="game_mode")],
    ])

def get_moscow_greeting(name: str) -> str:
    """Доброе утро/день/вечер по московскому времени."""
    now = datetime.now(ZoneInfo("Europe/Moscow"))
    h = now.hour
    if 5 <= h < 12:
        return f"Доброе утро, {name}!"
    if 12 <= h < 18:
        return f"Добрый день, {name}!"
    return f"Добрый вечер, {name}!"

async def start_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляем основное приветствие с картинкой или без."""
    chat_id = update.effective_chat.id
    user = update.effective_user
    name = user.first_name or "друг"
    greeting = get_moscow_greeting(name)
    full_text = f"{greeting}\n\n{MAIN_MENU_TEXT}"
    try:
        # Попробуем отправить фото с подписью
        with open("Снимок экрана 2025-04-08 в 21.55.12.png", "rb") as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=full_text,
                parse_mode="HTML",
                reply_markup=build_main_menu_keyboard()
            )
    except:
        # Если файл не найден, просто текстом
        await update.effective_message.reply_text(
            full_text,
            parse_mode="HTML",
            reply_markup=build_main_menu_keyboard()
        )

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Роутер для трёх основных режимов + возвращение в меню."""
    query = update.callback_query
    await query.answer()
    cmd = query.data

    if cmd == "assistant_pc":
        await assistant_pc(update, context)
    elif cmd == "educational_mode":
        await start_educational_mode(update, context)
    elif cmd == "game_mode":
        await start_game_mode(update, context)
    elif cmd == "game_home":
        # возврат в главное меню из интерактивного режима
        await start_main_menu(update, context)

# ——————————————————————————————————————————————————————————————————————
# Дополнительные команды
# ——————————————————————————————————————————————————————————————————————
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /support — контакт автора."""
    await update.message.reply_text("Alexandr_TSYP — создатель бота, помощь в сборке ПК")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /info — общая информация и контакты."""
    await update.message.reply_text(
        "Привет! Я Академия ПК — ваш надёжный помощник.\nПоддержка: @Alexandr_TSYP"
    )

# ——————————————————————————————————————————————————————————————————————
# Основная функция запуска бота
# ——————————————————————————————————————————————————————————————————————
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем все режимы
    setup_assistant_handlers(app)
    setup_educational_handlers(app)
    setup_game_handlers(app)

    # Старт и кнопки основного меню
    app.add_handler(CommandHandler("start", start_main_menu))
    app.add_handler(CallbackQueryHandler(main_menu_handler,
                                        pattern="^(assistant_pc|educational_mode|game_mode|game_home)$"))

    # Поддержка и инфо
    app.add_handler(CommandHandler("support", support))
    app.add_handler(CommandHandler("info", info))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())