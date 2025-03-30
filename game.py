# game.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from utils import get_user_data, set_user_data

# Текст главного меню, отформатированный с переносами строк
MAIN_MENU_TEXT = (
    "Привет! Я Академия ПК – ваш надёжный помощник в мире компьютерных технологий.\n\n"
    "Я могу помочь вам пошагово собрать персональный компьютер, учитывая особенности ваших комплектующих.\n"
    "Также я предлагаю два обучающих режима и интерактивное тестирование:\n\n"
    "• Ассистент сборки ПК – подробная инструкция по сборке компьютера.\n"
    "• Обучающий режим – выбор обучающих курсов (Базовый, Продвинутый, Профессиональный) для получения полной информации.\n"
    "• Интерактивный режим – сборка ПК по выбранному бюджету с интерактивными выборами комплектующих.\n\n"
    "Выберите режим работы:"
)

# Определяем этапы сборки (5 этапов)
STEPS = [
    {
        "component": "Процессор",
        "options": [
            {"name": "Intel Core i7-10700K (новый)", "price": 20000},
            {"name": "Intel Core i5-9400F (б/у)", "price": 12000}
        ],
        "optimal": 0
    },
    {
        "component": "Видеокарта",
        "options": [
            {"name": "NVIDIA GeForce RTX 3060 (новый)", "price": 25000},
            {"name": "NVIDIA GeForce GTX 1660 (б/у)", "price": 15000}
        ],
        "optimal": 0
    },
    {
        "component": "Оперативная память",
        "options": [
            {"name": "16GB DDR4 (новый)", "price": 8000},
            {"name": "8GB DDR4 (б/у)", "price": 4000}
        ],
        "optimal": 0
    },
    {
        "component": "Накопитель",
        "options": [
            {"name": "512GB NVMe SSD (новый)", "price": 6000},
            {"name": "1TB HDD (б/у)", "price": 3000}
        ],
        "optimal": 0
    },
    {
        "component": "Блок питания",
        "options": [
            {"name": "650W Gold PSU (новый)", "price": 5000},
            {"name": "500W PSU (б/у)", "price": 3000}
        ],
        "optimal": 0
    }
]
TOTAL_STEPS = len(STEPS)

# --- Функция отправки сообщений ---
async def send_stage_message(update: Update, text: str, header: str = "", reply_markup=None):
    if header:
        styled_header = f"<b>{header}</b>"
    else:
        styled_header = ""
    final_text = f"{styled_header}\n{text}"
    await update.effective_message.reply_text(final_text, reply_markup=reply_markup, parse_mode='HTML')

# --- Клавиатуры ---
def build_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Ассистент сборки ПК", callback_data="assistant_pc"),
         InlineKeyboardButton("Обучающий режим", callback_data="educational_mode"),
         InlineKeyboardButton("Интерактивный режим", callback_data="game_mode")]
    ])

def build_budget_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("50.000 рублей", callback_data="budget_50000")],
        [InlineKeyboardButton("75.000 рублей", callback_data="budget_75000")],
        [InlineKeyboardButton("100.000 рублей", callback_data="budget_100000")]
    ])

def build_choice_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1", callback_data="game_choice_0"),
         InlineKeyboardButton("2", callback_data="game_choice_1")]
    ])

def build_restart_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Пройти заново", callback_data="game_restart"),
         InlineKeyboardButton("Домой", callback_data="game_home")]
    ])

# --- Логика игры ---
async def start_game_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Ты попал в интерактивный режим.\n"
        "Твоя задача выбрать бюджет сборки ПК и собрать максимально производительную систему под различные задачи.\n"
        "Помни, что нужно грамотно распределять бюджет и тратить основную часть денег на видеокарту и процессор.\n\n"
        "Выбери режим сборки ПК:"
    )
    keyboard = build_budget_keyboard()
    await update.effective_message.reply_text(text, reply_markup=keyboard)

async def handle_budget_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data  # Например, "budget_50000"
    budget = int(data.split("_")[1])
    chat_id = query.message.chat_id
    init_game_state(chat_id, budget)
    await show_game_step(update, context)

def init_game_state(chat_id: int, budget: int):
    state = {
        "game_budget": budget,
        "game_remaining": budget,
        "game_step": 0,
        "game_selections": []
    }
    set_user_data(chat_id, state)

def update_game_state(chat_id: int, state: dict):
    set_user_data(chat_id, state)

def get_game_state(chat_id: int) -> dict:
    return get_user_data(chat_id)

async def show_game_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    state = get_game_state(chat_id)
    step_index = state.get("game_step", 0)
    if step_index < TOTAL_STEPS:
        step = STEPS[step_index]
        component = step["component"]
        options = step["options"]
        remaining = state.get("game_remaining", 0)
        text = f"Шаг {step_index + 1} из {TOTAL_STEPS}.\nВыберите {component}:\n\n"
        text += f"1) {options[0]['name']} – {options[0]['price']} руб.\n"
        text += f"2) {options[1]['name']} – {options[1]['price']} руб.\n\n"
        text += f"Остаток бюджета: {remaining} руб."
        await send_stage_message(update, text, header="Интерактивный режим", reply_markup=build_choice_keyboard())
    else:
        await show_game_result(update, context)

async def handle_game_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    state = get_game_state(chat_id)
    step_index = state.get("game_step", 0)
    current_step = STEPS[step_index]
    selected_option = int(query.data.split("_")[-1])  # 0 или 1
    price = current_step["options"][selected_option]["price"]
    remaining = state.get("game_remaining", 0) - price
    state["game_remaining"] = remaining
    state.setdefault("game_selections", []).append(selected_option)
    if remaining < 0:
        text = "Бюджет исчерпан! Вы не смогли завершить сборку."
        await send_stage_message(update, text, header="Интерактивный режим", reply_markup=build_restart_keyboard())
        update_game_state(chat_id, state)
        return
    state["game_step"] = step_index + 1
    update_game_state(chat_id, state)
    if state["game_step"] < TOTAL_STEPS:
        await show_game_step(update, context)
    else:
        await show_game_result(update, context)

async def show_game_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    state = get_game_state(chat_id)
    selections = state.get("game_selections", [])
    total_spent = state.get("game_budget", 0) - state.get("game_remaining", 0)
    optimal_count = 0
    result_text = "Итоговая сборка:\n"
    for i, step in enumerate(STEPS):
        component = step["component"]
        chosen = selections[i] if i < len(selections) else None
        option = step["options"][chosen] if chosen is not None else {}
        result_text += f"{i+1}. {component}: {option.get('name', 'Не выбрано')} – {option.get('price', 0)} руб.\n"
        if chosen == step["optimal"]:
            optimal_count += 1
    result_text += f"\nОбщая стоимость: {total_spent} руб.\n"
    result_text += f"Оптимальных выборов: {optimal_count} из {TOTAL_STEPS}.\n"
    if optimal_count == TOTAL_STEPS:
        result_text += "Отличная сборка! Вы собрали оптимальную систему."
    elif optimal_count >= TOTAL_STEPS - 1:
        result_text += "Очень хорошая сборка, почти идеальная!"
    else:
        result_text += "Сборка оставляет простор для улучшения. Рекомендуется перераспределить бюджет."
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Пройти заново", callback_data="game_restart"),
         InlineKeyboardButton("Домой", callback_data="game_home")]
    ])
    await send_stage_message(update, result_text, header="Результаты сборки", reply_markup=keyboard)

async def restart_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await start_game_mode(update, context)

async def game_go_home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=MAIN_MENU_TEXT,
        reply_markup=build_main_menu_keyboard(),
        parse_mode='HTML'
    )

# --- Функции обновления состояния игры ---
def update_game_state(chat_id: int, state: dict):
    set_user_data(chat_id, state)

def get_game_state(chat_id: int) -> dict:
    return get_user_data(chat_id)

# --------------------------------------------------
# Регистрация обработчиков для интерактивного режима (game mode)
# --------------------------------------------------
def setup_handlers(app):
    app.add_handler(CommandHandler("game", start_game_mode))
    app.add_handler(CallbackQueryHandler(start_game_mode, pattern="^game_mode$"))
    app.add_handler(CallbackQueryHandler(handle_budget_selection, pattern="^budget_"))
    app.add_handler(CallbackQueryHandler(handle_game_choice, pattern="^game_choice_"))
    app.add_handler(CallbackQueryHandler(restart_game, pattern="^game_restart$"))
    app.add_handler(CallbackQueryHandler(game_go_home, pattern="^game_home$"))