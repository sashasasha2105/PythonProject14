# game.py
# -*- coding: utf-8 -*-

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from utils import get_user_data, set_user_data

# ======================================
#          Настройки интерактивного режима
# ======================================

# Бюджеты на выбор (₽)
BUDGETS = [50_000, 100_000, 200_000]

# Этапы сборки, ценовая политика и пояснения
STEPS = [
    {
        "component": "Процессор",
        "options": [
            {"name": "Intel Core i3‑12100F", "price": 8_000},
            {"name": "AMD Ryzen 5 5600X",  "price": 14_000},
            {"name": "Intel Core i7‑12700K","price": 28_000},
        ],
        "optimal_game": 1,
        "optimal_work": 2,
        "analysis": {
            "game": (
                "Для современных игр важна высокая тактовая частота и хорошая производительность на одно ядро. "
                "Ryzen 5 5600X предлагает 6 ядер с басом до 4.6 ГГц, что делает его отличным выбором для большинства игр."
            ),
            "work": (
                "В рабочих приложениях (рендер, компиляция, многозадачность) ценятся максимальное число ядер и потоков. "
                "Core i7‑12700K с 12 реальными ядрами и 20 потоками позволит быстрее справляться с тяжёлыми задачами."
            )
        }
    },
    {
        "component": "Видеокарта",
        "options": [
            {"name": "NVIDIA GTX 1650",    "price": 12_000},
            {"name": "AMD Radeon RX 6600", "price": 20_000},
            {"name": "NVIDIA RTX 3060 Ti", "price": 30_000},
        ],
        "optimal_game": 2,
        "optimal_work": 0,
        "analysis": {
            "game": (
                "Для максимальной частоты кадров в играх RTX 3060 Ti обладает достаточным запасом CUDA‑ядер и высокой пропускной способностью памяти. "
                "Это позволит играть на высоких настройках в 1080p–1440p."
            ),
            "work": (
                "Если цель — офисные и профессиональные приложения без 3D‑ускорения, то дискретная видеокарта не критична. "
                "GTX 1650 достаточно для базового вывода изображения и ускорения интерфейсов."
            )
        }
    },
    {
        "component": "Оперативная память (16 ГБ)",
        "options": [
            {"name": "2×8 GB DDR4‑3200", "price": 6_000},
            {"name": "2×8 GB DDR4‑3600", "price": 7_000},
            {"name": "2×8 GB DDR5‑5200", "price": 10_000},
        ],
        "optimal_game": 1,
        "optimal_work": 2,
        "analysis": {
            "game": (
                "DDR4‑3600 обеспечивает сбалансированное соотношение скорости и стоимости для игр — частота выше стандартной, что даёт небольшой прирост FPS."
            ),
            "work": (
                "В рабочих задачах (виртуалки, компиляции) DDR5‑5200 даст лучший пропускной поток данных, ускоряя многопоточные операции."
            )
        }
    },
    {
        "component": "SSD‑накопитель",
        "options": [
            {"name": "512 GB NVMe PCIe 3.0", "price": 5_000},
            {"name": "1 TB NVMe PCIe 3.0",   "price": 8_000},
            {"name": "1 TB NVMe PCIe 4.0",   "price": 12_000},
        ],
        "optimal_game": 1,
        "optimal_work": 1,
        "analysis": {
            "game": (
                "1 TB PCIe 3.0 — достаточный объём и скорость для игр, позволит устанавливать несколько тяжёлых тайтлов без разгонки бюджета."
            ),
            "work": (
                "1 TB PCIe 3.0 обеспечивает баланс между объёмом и скоростью для рабочих проектов, где важен объём хранения."
            )
        }
    },
    {
        "component": "Блок питания",
        "options": [
            {"name": "550 W Bronze", "price": 4_000},
            {"name": "650 W Gold",   "price": 6_000},
            {"name": "750 W Gold",   "price": 8_000},
        ],
        "optimal_game": 1,
        "optimal_work": 1,
        "analysis": {
            "game": (
                "650 W Gold — достаточный запас мощности и высокий КПД для системы с RTX 3060 Ti и Ryzen 5."
            ),
            "work": (
                "650 W Gold подходит и для рабочих станций, обеспечивает стабильность и небольшой запас для апгрейда."
            )
        }
    },
    {
        "component": "Охлаждение",
        "options": [
            {"name": "Стоковый кулер","price": 1_000},
            {"name": "Башенный кулер","price": 3_000},
            {"name": "AIO 240 мм",    "price": 6_000},
        ],
        "optimal_game": 1,
        "optimal_work": 1,
        "analysis": {
            "game": (
                "Башенный кулер обеспечит более низкие температуры и тихую работу, чем стоковый, при умеренной стоимости."
            ),
            "work": (
                "Башенный кулер достаточно для многозадачности и сравнительно тихой работы, а AIO не даст существенного выигрыша за двойную цену."
            )
        }
    },
]

TOTAL_STEPS = len(STEPS)

# ======================================
#        Утилиты для клавиатур
# ======================================
def build_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Главное меню", callback_data="game_home")]
    ])

def build_purpose_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎮 Игры", callback_data="purpose_game"),
            InlineKeyboardButton("💼 Работа", callback_data="purpose_work"),
        ],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="game_home")]
    ])

def build_budget_keyboard():
    buttons = [InlineKeyboardButton(f"{b//1000} 000 ₽", callback_data=f"budget_{b}") for b in BUDGETS]
    return InlineKeyboardMarkup([buttons, [InlineKeyboardButton("🏠 Главное меню", callback_data="game_home")]])

def build_choice_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1️⃣", callback_data="choice_0"),
            InlineKeyboardButton("2️⃣", callback_data="choice_1"),
            InlineKeyboardButton("3️⃣", callback_data="choice_2"),
        ],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="game_home")]
    ])

def build_restart_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Пройти заново", callback_data="game_restart")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="game_home")]
    ])

# ======================================
#        Отправка сообщений
# ======================================
async def send_stage_message(update: Update, text: str, header: str = "", reply_markup=None):
    styled_header = f"<b>{header}</b>\n\n" if header else ""
    await update.effective_message.reply_text(
        f"{styled_header}{text}",
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# ======================================
#            Логика игры
# ======================================
async def start_game_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "🕹️ <b>Интерактивная сборка ПК</b>\n\nДля каких задач собираете систему?"
    await send_stage_message(update, text, reply_markup=build_purpose_keyboard())

async def handle_purpose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query; await query.answer()
    purpose = query.data.split("_")[1]  # "game" или "work"
    chat_id = query.message.chat_id
    set_user_data(chat_id, {
        "purpose": purpose,
        "budget": None,
        "remaining": None,
        "step": 0,
        "selections": []
    })
    text = "💰 Выберите бюджет сборки:"
    await send_stage_message(update, text, reply_markup=build_budget_keyboard())

async def handle_budget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query; await query.answer()
    budget = int(query.data.split("_")[1])
    chat_id = query.message.chat_id
    state = get_user_data(chat_id)
    state["budget"] = budget
    state["remaining"] = budget
    set_user_data(chat_id, state)
    await show_next_step(update, context)

async def show_next_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query; await query.answer()
    state = get_user_data(query.message.chat_id)
    idx = state["step"]
    if idx < TOTAL_STEPS:
        step = STEPS[idx]
        text = (
            f"Шаг {idx+1} из {TOTAL_STEPS} — выберите <b>{step['component']}</b>:\n\n"
            f"1) {step['options'][0]['name']} — {step['options'][0]['price']} ₽\n"
            f"2) {step['options'][1]['name']} — {step['options'][1]['price']} ₽\n"
            f"3) {step['options'][2]['name']} — {step['options'][2]['price']} ₽\n\n"
            f"Остаток бюджета: {state['remaining']} ₽"
        )
        await send_stage_message(update, text, header="Сборка ПК", reply_markup=build_choice_keyboard())
    else:
        await show_result(update, context)

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query; await query.answer()
    chat_id = query.message.chat_id
    state = get_user_data(chat_id)
    idx = state["step"]
    choice = int(query.data.split("_")[1])
    price = STEPS[idx]["options"][choice]["price"]
    state["remaining"] -= price
    state["selections"].append(choice)
    state["step"] += 1
    set_user_data(chat_id, state)

    if state["remaining"] < 0:
        await send_stage_message(
            update,
            "❌ Бюджет исчерпан! Сборка прервана.",
            header="Ошибка",
            reply_markup=build_restart_keyboard()
        )
        return

    await show_next_step(update, context)

async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query; await query.answer()
    state = get_user_data(query.message.chat_id)
    total_spent = state["budget"] - state["remaining"]
    optimal = 0
    lines = ["🏁 <b>Результаты сборки</b>\n"]
    purpose = state["purpose"]

    # Отчёт по выбору
    for i, sel in enumerate(state["selections"]):
        comp = STEPS[i]["component"]
        opt = STEPS[i]["options"][sel]
        best = STEPS[i][f"optimal_{purpose}"]
        mark = "✅" if sel == best else "❌"
        if sel == best:
            optimal += 1
        lines.append(f"{mark} {comp}: {opt['name']} — {opt['price']} ₽")

    lines.append(f"\n💰 Потрачено: {total_spent} ₽ из {state['budget']} ₽")
    lines.append(f"🏆 Оптимальных выборов: {optimal} из {TOTAL_STEPS}")

    # Глубокий теханализ
    if optimal == TOTAL_STEPS:
        lines.append("\n🎉 Отличная сборка! Вы идеально уложились в цель.")
    else:
        lines.append("\n🔎 <b>Глубокий теханализ:</b>")
        for i, sel in enumerate(state["selections"]):
            best = STEPS[i][f"optimal_{purpose}"]
            if sel != best:
                wrong_name = STEPS[i]["options"][sel]["name"]
                correct_name = STEPS[i]["options"][best]["name"]
                explanation = STEPS[i]["analysis"][purpose]
                lines.append(f"\n• <b>{STEPS[i]['component']}</b>: вы выбрали «{wrong_name}», а лучше «{correct_name}».\n  {explanation}")

    await send_stage_message(update, "\n".join(lines), reply_markup=build_restart_keyboard())

async def restart_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query; await query.answer()
    await start_game_mode(update, context)

async def game_go_home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query; await query.answer()
    from main import start_main_menu
    await start_main_menu(update, context)

# ======================================
#         Регистрация обработчиков
# ======================================
def setup_handlers(app):
    app.add_handler(CommandHandler("game", start_game_mode))
    app.add_handler(CallbackQueryHandler(start_game_mode,       pattern="^game_mode$"))
    app.add_handler(CallbackQueryHandler(handle_purpose,        pattern="^purpose_"))
    app.add_handler(CallbackQueryHandler(handle_budget,         pattern="^budget_"))
    app.add_handler(CallbackQueryHandler(handle_choice,         pattern="^choice_"))
    app.add_handler(CallbackQueryHandler(restart_game,          pattern="^game_restart$"))
    app.add_handler(CallbackQueryHandler(game_go_home,          pattern="^game_home$"))

# Алиас для main.py
start_game_mode = start_game_mode