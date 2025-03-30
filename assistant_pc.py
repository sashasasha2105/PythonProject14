# assistant_pc.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from data import (
    steps,
    cooling_instructions,
    ram_instructions,
    fan_instructions,
    power_supply_instructions,
    gpu_instructions,
    wires_instructions
)
from utils import get_user_data, set_user_data, update_user_step

# Общее количество этапов сборки (для расчёта процента завершения)
TOTAL_STEPS = 8

def get_progress_text(progress, total=TOTAL_STEPS):
    percent = int((progress / total) * 100)
    filled = "🟢" * progress
    unfilled = "⚪" * (total - progress)
    return f"Прогресс сборки: [{filled}{unfilled}] {percent}%"

def increment_progress(chat_id):
    data = get_user_data(chat_id)
    current = data.get("progress", 0)
    data["progress"] = current + 1
    set_user_data(chat_id, data)

def current_progress_text(chat_id):
    data = get_user_data(chat_id)
    progress = data.get("progress", 0)
    return get_progress_text(progress)

async def send_stage_message(update: Update, text: str, header: str = "", reply_markup=None):
    """
    Отправляет сообщение с жирным заголовком и неизменным текстом.
    """
    if header:
        clean_header = header.replace("🤖", "").strip()
        styled_header = f"<b>{clean_header}</b>"
    else:
        styled_header = ""
    final_text = f"{styled_header}\n{text}"
    await update.effective_message.reply_text(final_text, reply_markup=reply_markup, parse_mode='HTML')

# --------------------------------------------------
# Исходное приветственное сообщение (главное меню режима ассистента)
# --------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправляет исходное приветственное сообщение режима Ассистента сборки ПК.
    Это сообщение содержит описание режимов, как в оригинале.
    """
    chat_id = update.effective_chat.id
    set_user_data(chat_id, {"progress": 0})
    welcome_text = (
        "Привет! Я Академия ПК – ваш надёжный помощник в мире компьютерных технологий.\n\n"
        "Я могу помочь вам пошагово собрать персональный компьютер, учитывая особенности ваших комплектующих. "
        "Также я предлагаю два обучающих режима и интерактивное тестирование:\n\n"
        "• Ассистент сборки ПК – подробная инструкция по сборке компьютера.\n"
        "• Обучающий режим – выберите один из обучающих курсов (Базовый, Продвинутый, Профессиональный) "
        "для получения полной обучающей информации и прохождения теста соответствующей сложности.\n"
        "• Интерактивный режим – общий тест по знаниям о ПК.\n\n"
        "Выберите режим работы:"
    )
    main_menu_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Ассистент сборки ПК", callback_data="assistant_pc"),
         InlineKeyboardButton("Обучающий режим", callback_data="educational_mode")]
    ])
    await send_stage_message(update, welcome_text, header="🌟 Главное меню", reply_markup=main_menu_keyboard)

# --------------------------------------------------
# Режим "Ассистент сборки ПК"
# --------------------------------------------------
async def assistant_pc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Запуск режима Ассистента сборки ПК.
    Вызывается из главного меню по callback_data "assistant_pc".
    """
    query = update.callback_query
    await query.answer()
    text = (
        "Привет! Я чат-бот по сборке вашего ПК. У вас есть все необходимые компоненты для сборки?\n\n"
        "Проверьте наличие:\n"
        "- Материнская плата\n"
        "- Процессор\n"
        "- Охлаждение процессора\n"
        "- Оперативная память\n"
        "- Накопитель\n"
        "- Блок питания\n"
        "- Корпус\n"
        "- Видеокарта (если нужна)\n"
        "- Отвертки\n"
        "- Термопаста"
    )
    await send_stage_message(update, text, header="Режим ассистента сборки",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Я готов", callback_data="ready"),
                                    InlineKeyboardButton("Еще нужно подготовиться", callback_data="not_ready")],
                                   [InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

# --------------------------------------------------
# Обработчик кнопки "Домой" – возвращает в главное меню
# --------------------------------------------------
async def go_home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    При нажатии кнопки "Домой" возвращает пользователя к исходному приветственному сообщению,
    которое содержит две кнопки и является главным меню (как в main.py).
    """
    query = update.callback_query
    await query.answer()
    # Отправляем главное меню. Здесь дублируется текст и клавиатура из функции start.
    main_menu_text = (
        "Привет! Я Академия ПК – ваш надёжный помощник в мире компьютерных технологий.\n\n"
        "Я могу помочь вам пошагово собрать персональный компьютер, учитывая особенности ваших комплектующих. "
        "Также я предлагаю два обучающих режима и интерактивное тестирование:\n\n"
        "• Ассистент сборки ПК – подробная инструкция по сборке компьютера.\n"
        "• Обучающий режим – выберите один из обучающих курсов (Базовый, Продвинутый, Профессиональный) "
        "для получения полной обучающей информации и прохождения теста соответствующей сложности.\n"
        "• Интерактивный режим – общий тест по знаниям о ПК.\n\n"
        "Выберите режим работы:"
    )
    main_menu_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Ассистент сборки ПК", callback_data="assistant_pc"),
         InlineKeyboardButton("Обучающий режим", callback_data="educational_mode")]
    ])
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=main_menu_text,
        reply_markup=main_menu_keyboard,
        parse_mode='HTML'
    )

# --------------------------------------------------
# Обработка готовности к сборке
# --------------------------------------------------
async def handle_preparation_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "ready":
        text = (
            "Разложите комплектующие на ровной, просторной и непроводящей поверхности. "
            "Убедитесь, что у вас достаточно места для работы.\n\n"
            "Расположите их так, чтобы были легко доступны:\n"
            "- Корпус\n"
            "- Материнская плата\n"
            "- Процессор, кулер и ОЗУ\n"
            "- Видеокарта, SSD/HDD\n"
            "- Блок питания"
        )
        await query.edit_message_text(text)
        increment_progress(query.message.chat_id)
        progress_text = current_progress_text(query.message.chat_id)
        await send_stage_message(update, f"{progress_text}\n\nНажмите 'Дальше⏩', чтобы продолжить.",
                                   header="🛠️ Этап подготовки",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton("Назад⏪", callback_data="back_to_start"),
                                        InlineKeyboardButton("Дальше⏩", callback_data="next_step"),
                                        InlineKeyboardButton("🏠", callback_data="go_home")]
                                   ]))
    else:
        await query.edit_message_text("Пожалуйста, подготовьтесь и запустите сборку позже.")

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await assistant_pc(update, context)

# --------------------------------------------------
# Переход к выбору платформы (Процессора)
# --------------------------------------------------
async def process_next_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update, "Выберите производителя процессора:",
                               header="💻 Выбор платформы",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Intel", callback_data="Intel"),
                                    InlineKeyboardButton("AMD", callback_data="AMD")],
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_preparation"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def back_to_preparation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_preparation_choice(update, context)

# --------------------------------------------------
# Обработка выбора платформы
# --------------------------------------------------
async def process_platform_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    platform = query.data
    data = get_user_data(query.message.chat_id)
    if "progress" not in data:
        data["progress"] = 0
    data["platform"] = platform
    data["step_index"] = 0
    set_user_data(query.message.chat_id, data)
    await show_step(update, context)

# --------------------------------------------------
# Шаг установки процессора
# --------------------------------------------------
async def show_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_info = get_user_data(query.message.chat_id)
    if user_info:
        platform = user_info["platform"]
        step_index = user_info["step_index"]
        instructions_list = steps.get(platform, {}).get("instructions", [])
        if step_index < len(instructions_list):
            step_text = instructions_list[step_index]
            await send_stage_message(update, step_text, header="⚙️ Установка процессора")
            user_info["step_index"] += 1
            update_user_step(query.message.chat_id, "step_index", user_info["step_index"])
            increment_progress(query.message.chat_id)
            progress_text = current_progress_text(query.message.chat_id)
            await send_stage_message(update, f"{progress_text}\n\nНажмите 'Дальше⏩', чтобы перейти к выбору типа охлаждения.",
                                       header="⚙️ Установка процессора",
                                       reply_markup=InlineKeyboardMarkup([
                                           [InlineKeyboardButton("Назад⏪", callback_data="back_to_platform"),
                                            InlineKeyboardButton("Дальше⏩", callback_data="next_step_cooling"),
                                            InlineKeyboardButton("🏠", callback_data="go_home")]
                                       ]))

async def back_to_platform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await process_next_step(update, context)

# --------------------------------------------------
# Выбор типа охлаждения
# --------------------------------------------------
async def handle_cooling_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update, "Установка охлаждения процессора:\nКакой тип охлаждения у вас?",
                               header="❄️ Выбор системы охлаждения",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Воздушное", callback_data="air"),
                                    InlineKeyboardButton("Водяное", callback_data="water")],
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_platform"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def handle_cooling_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_info = get_user_data(query.message.chat_id)
    platform = user_info.get("platform", "Intel")
    cooling_type = query.data
    user_info["cooling"] = cooling_type
    set_user_data(query.message.chat_id, user_info)
    instructions = cooling_instructions.get(platform, {}).get(cooling_type, "Инструкция не найдена.")
    await send_stage_message(update, instructions, header="❄️ Система охлаждения")
    increment_progress(query.message.chat_id)
    progress_text = current_progress_text(query.message.chat_id)
    await send_stage_message(update, f"{progress_text}\n\nНажмите 'Дальше⏩', чтобы продолжить установку оперативной памяти.",
                               header="❄️ Система охлаждения",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_cooling"),
                                    InlineKeyboardButton("Дальше⏩", callback_data="next_step_ram"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def back_to_cooling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_cooling_choice(update, context)

# --------------------------------------------------
# Выбор оперативной памяти
# --------------------------------------------------
async def handle_ram_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update, "Установка оперативной памяти. Сколько планок ОЗУ у вас?",
                               header="💾 Установка оперативной памяти",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("1 планка", callback_data="1"),
                                    InlineKeyboardButton("2 планки", callback_data="2"),
                                    InlineKeyboardButton("4 планки", callback_data="4")],
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_cooling"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def handle_ram_choice_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    ram_choice = query.data
    instruction = ram_instructions.get(ram_choice, "Инструкция не найдена.")
    await query.edit_message_text(instruction)
    increment_progress(query.message.chat_id)
    progress_text = current_progress_text(query.message.chat_id)
    await send_stage_message(update, f"{progress_text}\n\nНажмите 'Дальше⏩', чтобы перейти к установке M.2 накопителя.",
                               header="💾 Установка оперативной памяти",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_ram"),
                                    InlineKeyboardButton("Дальше⏩", callback_data="next_step_m2"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def back_to_ram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_ram_choice(update, context)

# --------------------------------------------------
# Установка M.2 накопителя
# --------------------------------------------------
async def handle_m2_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update,
        "Установка M.2 накопителя:\n"
        "1. Найдите слот M.2.\n"
        "2. Аккуратно вставьте накопитель.\n"
        "3. Зафиксируйте винтом.\n"
        "[Видео](https://rutube.ru/video/fa86b5395ed102e415eb00d8a3b2f9fd/)",
        header="🗜️ Установка M.2"
    )
    increment_progress(query.message.chat_id)
    progress_text = current_progress_text(query.message.chat_id)
    await send_stage_message(update, f"{progress_text}\n\nНажмите 'Дальше⏩', чтобы перейти к установке вентиляторов.",
                               header="🗜️ Установка M.2",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_m2"),
                                    InlineKeyboardButton("Дальше⏩", callback_data="next_step_fans"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def back_to_m2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_m2_choice(update, context)

# --------------------------------------------------
# Выбор типа установки вентиляторов
# --------------------------------------------------
async def handle_fan_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update, "Установка вентиляторов в корпус. Выберите тип корпуса:",
                               header="🌀 Установка вентиляторов",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Аквариумный тип", callback_data="aquarium"),
                                    InlineKeyboardButton("Классический тип (нижнее расположение БП)", callback_data="classic_bottom")],
                                   [InlineKeyboardButton("Классический тип (верхнее расположение БП)", callback_data="classic_top"),
                                    InlineKeyboardButton("У меня уже установлены", callback_data="already_installed")],
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_m2"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def handle_fan_instructions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    instruction = fan_instructions.get(query.data, "Инструкция не найдена.")
    await query.edit_message_text(instruction)
    increment_progress(query.message.chat_id)
    progress_text = current_progress_text(query.message.chat_id)
    await send_stage_message(update, f"{progress_text}\n\nНажмите 'Дальше⏩', чтобы перейти к установке блока питания.",
                               header="🌀 Установка вентиляторов",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_fans"),
                                    InlineKeyboardButton("Дальше⏩", callback_data="next_step_power_supply"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def back_to_fans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_fan_choice(update, context)

# --------------------------------------------------
# Установка блока питания
# --------------------------------------------------
async def handle_power_supply_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update, power_supply_instructions,
                               header="🔌 Установка блока питания")
    increment_progress(query.message.chat_id)
    progress_text = current_progress_text(query.message.chat_id)
    await send_stage_message(update, f"{progress_text}\n\nНажмите 'Дальше⏩', чтобы продолжить.",
                               header="🔌 Установка блока питания",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_fans"),
                                    InlineKeyboardButton("Дальше⏩", callback_data="next_step_gpu_check"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def back_to_power(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_fan_instructions(update, context)

# --------------------------------------------------
# Проверка наличия видеокарты
# --------------------------------------------------
async def ask_gpu_presence(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update, "Есть ли у вас дискретная видеокарта?",
                               header="🎮 Подключение видеокарты",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Да", callback_data="gpu_yes"),
                                    InlineKeyboardButton("Нет", callback_data="gpu_no")],
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_power"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def handle_gpu_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update, gpu_instructions, header="🎮 Видеокарта")
    increment_progress(query.message.chat_id)
    progress_text = current_progress_text(query.message.chat_id)
    await send_stage_message(update, f"{progress_text}\n\nНажмите 'Дальше⏩' для подключения проводов ПК.",
                               header="🎮 Видеокарта",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_gpu"),
                                    InlineKeyboardButton("Дальше⏩", callback_data="next_step_wires"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def handle_gpu_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    increment_progress(query.message.chat_id)
    progress_text = current_progress_text(query.message.chat_id)
    await send_stage_message(update, f"{progress_text}\n\nНажмите 'Дальше⏩' для подключения проводов ПК.",
                               header="🎮 Видеокарта",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_gpu"),
                                    InlineKeyboardButton("Дальше⏩", callback_data="next_step_wires"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def back_to_gpu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_power_supply_choice(update, context)

# --------------------------------------------------
# Подключение проводов ПК
# --------------------------------------------------
async def handle_wires_instruction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update, wires_instructions, header="🔗 Подключение проводов")
    await send_stage_message(update, "Нужна ли вам помощь в установке ОС?",
                               header="🔗 Подключение проводов",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Да", callback_data="os_yes"),
                                    InlineKeyboardButton("Нет", callback_data="os_no")],
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_wires"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def back_to_wires(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_wires_instruction(update, context)

# --------------------------------------------------
# Выбор помощи в установке ОС
# --------------------------------------------------
async def handle_os_help_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update, "Выберите операционную систему:",
                               header="💿 Помощь в установке ОС",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Windows", callback_data="os_windows"),
                                    InlineKeyboardButton("Linux", callback_data="os_linux"),
                                    InlineKeyboardButton("Mac OS", callback_data="os_mac")],
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_wires"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def handle_os_help_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update, "Хорошо, переходим к завершению сборки.",
                               header="💿 Помощь в установке ОС",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_wires"),
                                    InlineKeyboardButton("Завершить сборку", callback_data="finish_assembly"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def back_to_os(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_os_help_yes(update, context)

# --------------------------------------------------
# Подробные инструкции по установке ОС
# --------------------------------------------------
async def handle_os_windows(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update,
        "Подробная инструкция по установке **Windows**:\n\n"
        "1. **Загрузка образа:** перейдите на официальный сайт Microsoft:\n"
        "   https://www.microsoft.com/software-download/windows\n"
        "   и скачайте ISO-образ.\n"
        "2. **Создание загрузочной флешки:** используйте Rufus или Media Creation Tool.\n"
        "3. **Настройка BIOS/UEFI:** при необходимости включите UEFI Boot.\n"
        "4. **Запуск установки:** загрузитесь с флешки и следуйте инструкциям установщика.\n\n"
        "Подробные рекомендации:\n"
        "https://support.microsoft.com/en-us/windows",
        header="🖥️ Установка Windows"
    )
    await send_stage_message(update, "Нажмите 'Завершить сборку', чтобы закончить процесс.",
                               header="🖥️ Установка Windows",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_os"),
                                    InlineKeyboardButton("Завершить сборку", callback_data="finish_assembly"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def handle_os_linux(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update,
        "Подробная инструкция по установке **Linux**:\n\n"
        "1. **Выбор дистрибутива:** например, Ubuntu, Fedora, Debian и т.д.\n"
        "2. **Скачивание ISO:** с официальных сайтов (например, https://ubuntu.com/ для Ubuntu).\n"
        "3. **Создание загрузочной флешки:** используйте balenaEtcher или Rufus.\n"
        "4. **Настройка BIOS/UEFI:** включите UEFI или Legacy Boot (в зависимости от дистрибутива).\n"
        "5. **Запуск установки:** загрузитесь с флешки и следуйте шагам установщика.\n\n"
        "Подробнее:\n"
        "• Ubuntu Docs: https://ubuntu.com/tutorials\n"
        "• Fedora Docs: https://docs.fedoraproject.org/\n"
        "• Debian Handbook: https://www.debian.org/doc/",
        header="🐧 Установка Linux"
    )
    await send_stage_message(update, "Нажмите 'Завершить сборку', чтобы закончить процесс.",
                               header="🐧 Установка Linux",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_os"),
                                    InlineKeyboardButton("Завершить сборку", callback_data="finish_assembly"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

async def handle_os_mac(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update,
        "Подробная инструкция по установке **Mac OS**:\n\n"
        "1. **Проверьте совместимость:** убедитесь, что ваше устройство поддерживает нужную версию.\n"
        "2. **Скачивание:** если это Mac, установщик можно загрузить из App Store. Для Hackintosh – используются специальные сборки.\n"
        "3. **Создание загрузочной флешки (для Hackintosh):** используйте UniBeast или OpenCore.\n"
        "4. **Настройка BIOS/UEFI:** отключите Secure Boot, включите AHCI и т.д.\n"
        "5. **Установка:** загрузитесь с флешки и следуйте инструкциям установщика.\n\n"
        "Подробнее:\n"
        "• Apple Support: https://support.apple.com/boot-camp\n"
        "• Hackintosh Guides: https://dortania.github.io/",
        header="🍎 Установка Mac OS"
    )
    await send_stage_message(update, "Нажмите 'Завершить сборку', чтобы закончить процесс.",
                               header="🍎 Установка Mac OS",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Назад⏪", callback_data="back_to_os"),
                                    InlineKeyboardButton("Завершить сборку", callback_data="finish_assembly"),
                                    InlineKeyboardButton("🏠", callback_data="go_home")]
                               ]))

# --------------------------------------------------
# Завершение сборки
# --------------------------------------------------
async def finish_assembly(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_stage_message(update,
        "Поздравляем! Сборка завершена. Приятного использования вашего нового ПК!",
        header="🎉 Завершение сборки",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Вернуться в главное меню 🏠", callback_data="go_home")]
        ])
    )

# --------------------------------------------------
# Регистрация обработчиков для режима Ассистента сборки ПК
# --------------------------------------------------
def setup_handlers(app):
    app.add_handler(CallbackQueryHandler(assistant_pc, pattern="^assistant_pc$"))
    app.add_handler(CallbackQueryHandler(go_home, pattern="^go_home$"))
    app.add_handler(CallbackQueryHandler(handle_preparation_choice, pattern="^(ready|not_ready)$"))
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="^back_to_start$"))
    app.add_handler(CallbackQueryHandler(process_next_step, pattern="^next_step$"))
    app.add_handler(CallbackQueryHandler(back_to_preparation, pattern="^back_to_preparation$"))
    app.add_handler(CallbackQueryHandler(process_platform_choice, pattern="^(Intel|AMD)$"))
    app.add_handler(CallbackQueryHandler(back_to_platform, pattern="^back_to_platform$"))
    # Переход к выбору типа охлаждения
    app.add_handler(CallbackQueryHandler(handle_cooling_choice, pattern="^next_step_cooling$"))
    app.add_handler(CallbackQueryHandler(back_to_cooling, pattern="^back_to_cooling$"))
    app.add_handler(CallbackQueryHandler(handle_cooling_selection, pattern="^(air|water)$"))
    # Выбор оперативной памяти
    app.add_handler(CallbackQueryHandler(handle_ram_choice, pattern="^next_step_ram$"))
    app.add_handler(CallbackQueryHandler(handle_ram_choice_selection, pattern="^(1|2|4)$"))
    app.add_handler(CallbackQueryHandler(back_to_ram, pattern="^back_to_ram$"))
    # Установка M.2 накопителя
    app.add_handler(CallbackQueryHandler(handle_m2_choice, pattern="^next_step_m2$"))
    app.add_handler(CallbackQueryHandler(back_to_m2, pattern="^back_to_m2$"))
    # Выбор типа установки вентиляторов
    app.add_handler(CallbackQueryHandler(handle_fan_choice, pattern="^next_step_fans$"))
    app.add_handler(CallbackQueryHandler(back_to_fans, pattern="^back_to_fans$"))
    app.add_handler(CallbackQueryHandler(handle_fan_instructions, pattern="^(aquarium|classic_bottom|classic_top|already_installed)$"))
    # Установка блока питания
    app.add_handler(CallbackQueryHandler(handle_power_supply_choice, pattern="^next_step_power_supply$"))
    app.add_handler(CallbackQueryHandler(back_to_power, pattern="^back_to_power$"))
    # Проверка наличия видеокарты
    app.add_handler(CallbackQueryHandler(ask_gpu_presence, pattern="^next_step_gpu_check$"))
    app.add_handler(CallbackQueryHandler(handle_gpu_yes, pattern="^gpu_yes$"))
    app.add_handler(CallbackQueryHandler(handle_gpu_no, pattern="^gpu_no$"))
    app.add_handler(CallbackQueryHandler(back_to_gpu, pattern="^back_to_gpu$"))
    # Подключение проводов ПК
    app.add_handler(CallbackQueryHandler(handle_wires_instruction, pattern="^next_step_wires$"))
    app.add_handler(CallbackQueryHandler(back_to_wires, pattern="^back_to_wires$"))
    # Помощь в установке ОС
    app.add_handler(CallbackQueryHandler(handle_os_help_yes, pattern="^os_yes$"))
    app.add_handler(CallbackQueryHandler(handle_os_help_no, pattern="^os_no$"))
    app.add_handler(CallbackQueryHandler(back_to_os, pattern="^back_to_os$"))
    # Подробные инструкции по установке ОС
    app.add_handler(CallbackQueryHandler(handle_os_windows, pattern="^os_windows$"))
    app.add_handler(CallbackQueryHandler(handle_os_linux, pattern="^os_linux$"))
    app.add_handler(CallbackQueryHandler(handle_os_mac, pattern="^os_mac$"))
    # Завершение сборки
    app.add_handler(CallbackQueryHandler(finish_assembly, pattern="^finish_assembly$"))