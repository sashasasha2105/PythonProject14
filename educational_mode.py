# educational_mode.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes
from utils import get_user_data, set_user_data

# --- Тексты курсов в повествовательном стиле ---

# Базовый курс: Комплектующие ПК и их предназначение (5 блоков)
BASIC_COURSE_BLOCKS = [
    (
        "Блок 1. Процессор (CPU)\n"
        "Процессор – это «мозг» компьютера, отвечающий за выполнение инструкций и управление работой всех компонентов системы. "
        "Он обрабатывает данные, выполняет вычисления и координирует работу периферийных устройств. "
        "Различные модели процессоров отличаются производительностью и энергоэффективностью."
    ),
    (
        "Блок 2. Оперативная память (RAM)\n"
        "Оперативная память временно хранит данные и программы, с которыми работает компьютер в данный момент. "
        "Её объём и скорость определяют, сколько информации может обрабатываться одновременно, что напрямую влияет на быстродействие системы."
    ),
    (
        "Блок 3. Материнская плата\n"
        "Материнская плата объединяет все комплектующие, обеспечивая их взаимодействие. "
        "Она содержит слоты для процессора, оперативной памяти, видеокарты, накопителей и другие разъёмы, позволяющие создать гармоничную систему."
    ),
    (
        "Блок 4. Накопители данных\n"
        "Накопители, такие как SSD и HDD, отвечают за долговременное хранение информации. "
        "SSD отличаются высокой скоростью доступа к данным, что ускоряет загрузку системы и приложений, а HDD – большей ёмкостью. "
        "Правильное сочетание этих устройств позволяет оптимизировать производительность и стоимость системы."
    ),
    (
        "Блок 5. Блок питания и система охлаждения\n"
        "Блок питания преобразует сетевое напряжение в необходимые для работы компонентов значения, обеспечивая стабильное энергоснабжение. "
        "Система охлаждения, включающая кулеры и радиаторы, предотвращает перегрев, что критично для долговечности и стабильной работы ПК."
    )
]

# Продвинутый курс: Основы сборки ПК (6 блоков)
ADVANCED_COURSE_BLOCKS = [
    (
        "Блок 1. Подготовка рабочего места и инструментов\n"
        "Перед началом сборки необходимо организовать чистое, хорошо освещённое рабочее пространство и подготовить все необходимые инструменты: отвертки, антистатический браслет, пинцеты и пр. "
        "Это помогает избежать ошибок и повреждений компонентов."
    ),
    (
        "Блок 2. Установка процессора и системы охлаждения\n"
        "Процессор устанавливается с особой осторожностью, чтобы не повредить контакты. "
        "Далее устанавливается система охлаждения – кулер или водяное охлаждение, при этом важно правильно нанести термопасту для эффективного рассеивания тепла."
    ),
    (
        "Блок 3. Монтаж оперативной памяти и видеокарты\n"
        "Установка оперативной памяти требует аккуратного совмещения ключевых выемок на модулях с соответствующими слотами на материнской плате. "
        "Видеокарта устанавливается в слот PCI-Express и закрепляется для обеспечения стабильной работы графической подсистемы."
    ),
    (
        "Блок 4. Установка накопителей и подключение кабелей\n"
        "Монтаж накопителей включает их фиксацию в корпусе и подключение к материнской плате через SATA или NVMe интерфейсы. "
        "Важна аккуратность при подключении кабелей для обеспечения надежной передачи данных и питания."
    ),
    (
        "Блок 5. Проверка подключения и первичный запуск системы\n"
        "После установки всех компонентов проводится проверка: убедитесь, что все кабели и устройства надежно закреплены. "
        "Выполните тестовый запуск системы, чтобы проверить, что BIOS распознает все компоненты и отсутствуют аппаратные сбои."
    ),
    (
        "Блок 6. Установка операционной системы и драйверов\n"
        "После успешного тестового запуска устанавливается операционная система, которая управляет работой ПК. "
        "Далее устанавливаются актуальные драйверы для всех комплектующих, что обеспечивает максимальную производительность и стабильность работы системы."
    )
]

# Профессиональный курс: Нюансы и тонкие моменты сборки ПК (7 блоков)
PROFESSIONAL_COURSE_BLOCKS = [
    (
        "Блок 1. Оптимизация воздушного потока и охлаждения\n"
        "Тщательное планирование воздушного потока внутри корпуса позволяет эффективно рассеивать тепло. "
        "Правильное расположение вентиляторов и радиаторов обеспечивает оптимальное охлаждение, что критично для стабильной работы высокопроизводительных систем."
    ),
    (
        "Блок 2. Электростатическая защита и меры предосторожности\n"
        "Сборка ПК требует соблюдения мер предосторожности для защиты компонентов от статического электричества. "
        "Использование антистатического браслета и соблюдение правил работы с чувствительными элементами предотвращают повреждения."
    ),
    (
        "Блок 3. Управление кабелями и эстетика сборки\n"
        "Чистота внутри корпуса улучшает не только внешний вид, но и функциональность системы за счёт оптимального воздушного потока. "
        "Организованное управление кабелями с помощью стяжек и специальных каналов повышает как эффективность, так и эстетику сборки."
    ),
    (
        "Блок 4. Разгон и тонкая настройка BIOS/UEFI\n"
        "Для достижения максимальной производительности системы часто проводят разгон компонентов. "
        "Тщательная настройка BIOS/UEFI, грамотное распределение напряжения и частот позволяют добиться высоких результатов без потери стабильности."
    ),
    (
        "Блок 5. Обеспечение стабильности работы при высоких нагрузках\n"
        "Системы, рассчитанные на длительную интенсивную работу, требуют качественных комплектующих и резервирования по питанию. "
        "Мониторинг и оптимизация работы системы помогают обеспечить её стабильность даже при экстремальных нагрузках."
    ),
    (
        "Блок 6. Использование специализированного ПО для мониторинга системы\n"
        "Для контроля за параметрами компонентов используются специальные программы и утилиты, позволяющие в реальном времени следить за температурой, напряжением и производительностью. "
        "Это позволяет своевременно выявлять и устранять возможные проблемы."
    ),
    (
        "Блок 7. Анализ и устранение ошибок при сборке\n"
        "После сборки системы проводится детальный анализ работы всех компонентов. "
        "Последовательная проверка каждого узла и использование диагностического ПО помогают выявить и устранить возможные проблемы, обеспечивая оптимальную производительность."
    )
]

# Краткие описания курсов для страницы выбора
BASIC_SUMMARY = "Базовый курс состоит из 5 блоков. Он рассказывает о ключевых компонентах ПК и их базовых функциях."
ADVANCED_SUMMARY = "Продвинутый курс состоит из 6 блоков. Он объясняет последовательность сборки и основные этапы установки компонентов."
PROFESSIONAL_SUMMARY = "Профессиональный курс состоит из 7 блоков. Он посвящён глубокому анализу, оптимизации и тестированию системы."

# Текст главного меню (тот же, что и в main.py)
MAIN_MENU_TEXT = (
    "Привет! Я Академия ПК – ваш надёжный помощник в мире компьютерных технологий.\n\n"
    "Я могу помочь вам пошагово собрать персональный компьютер, учитывая особенности ваших комплектующих. "
    "Также я предлагаю два обучающих режима и интерактивное тестирование:\n\n"
    "• Ассистент сборки ПК – подробная инструкция по сборке компьютера.\n"
    "• Обучающий режим – выберите один из обучающих курсов (Базовый, Продвинутый, Профессиональный) для получения полной обучающей информации и прохождения теста соответствующей сложности.\n"
    "• Интерактивный режим – общий тест по знаниям о ПК.\n\n"
    "Выберите режим работы:"
)

def build_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Ассистент сборки ПК", callback_data="assistant_pc"),
         InlineKeyboardButton("Обучающий режим", callback_data="educational_mode")]
    ])

# --------------------------------------------------
# Функция отправки сообщений
# --------------------------------------------------
async def send_stage_message(update: Update, text: str, header: str = "", reply_markup=None):
    if header:
        styled_header = f"<b>{header}</b>"
    else:
        styled_header = ""
    final_text = f"{styled_header}\n{text}"
    await update.effective_message.reply_text(final_text, reply_markup=reply_markup, parse_mode='HTML')

# --------------------------------------------------
# Функция возврата в главное меню (из обучающего режима)
# --------------------------------------------------
async def edu_go_home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=MAIN_MENU_TEXT,
        reply_markup=build_main_menu_keyboard(),
        parse_mode='HTML'
    )

# --------------------------------------------------
# Запуск обучающего режима – выбор курса
# --------------------------------------------------
async def start_educational_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Добро пожаловать в режим Обучения!\n\nВыберите курс для изучения:"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 Базовый курс", callback_data="basic_course")],
        [InlineKeyboardButton("📗 Продвинутый курс", callback_data="advanced_course")],
        [InlineKeyboardButton("📙 Профессиональный курс", callback_data="professional_course")]
    ])
    await update.effective_message.reply_text(text, reply_markup=keyboard)

# --------------------------------------------------
# Страница описания курса
# --------------------------------------------------
async def basic_course_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"{BASIC_SUMMARY}\n\nНажмите 'Начать', чтобы приступить к обучению."
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Назад", callback_data="edu_back")],
        [InlineKeyboardButton("Начать", callback_data="basic_start")],
        [InlineKeyboardButton("Домой", callback_data="edu_home")]
    ])
    await update.effective_message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')

async def advanced_course_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"{ADVANCED_SUMMARY}\n\nНажмите 'Начать', чтобы приступить к обучению."
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Назад", callback_data="edu_back")],
        [InlineKeyboardButton("Начать", callback_data="advanced_start")],
        [InlineKeyboardButton("Домой", callback_data="edu_home")]
    ])
    await update.effective_message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')

async def professional_course_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"{PROFESSIONAL_SUMMARY}\n\nНажмите 'Начать', чтобы приступить к обучению."
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Назад", callback_data="edu_back")],
        [InlineKeyboardButton("Начать", callback_data="professional_start")],
        [InlineKeyboardButton("Домой", callback_data="edu_home")]
    ])
    await update.effective_message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')

# --------------------------------------------------
# Функции запуска курсов
# --------------------------------------------------
def get_course_blocks(course: str):
    if course == "basic":
        return BASIC_COURSE_BLOCKS
    elif course == "advanced":
        return ADVANCED_COURSE_BLOCKS
    elif course == "professional":
        return PROFESSIONAL_COURSE_BLOCKS
    else:
        return []

async def start_course(update: Update, context: ContextTypes.DEFAULT_TYPE, course: str) -> None:
    chat_id = update.effective_chat.id
    data = {"edu_course": course, "block_index": 0}
    set_user_data(chat_id, data)
    await show_course_block(update, context)

async def basic_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_course(update, context, "basic")

async def advanced_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_course(update, context, "advanced")

async def professional_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_course(update, context, "professional")

# --------------------------------------------------
# Отображение текущего блока курса с навигацией
# --------------------------------------------------
async def show_course_block(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    course = data.get("edu_course")
    blocks = get_course_blocks(course)
    index = data.get("block_index", 0)
    if index < len(blocks):
        block_text = blocks[index]
        nav_buttons = []
        if index > 0:
            nav_buttons.append(InlineKeyboardButton("Назад", callback_data="course_prev"))
        else:
            nav_buttons.append(InlineKeyboardButton("Назад", callback_data="edu_back"))
        if index < len(blocks) - 1:
            nav_buttons.append(InlineKeyboardButton("Дальше", callback_data="course_next"))
        else:
            nav_buttons.append(InlineKeyboardButton("Завершить курс", callback_data="course_finish"))
        nav_buttons.append(InlineKeyboardButton("Домой", callback_data="edu_home"))
        keyboard = InlineKeyboardMarkup([nav_buttons])
        await send_stage_message(update, block_text, header="Обучение", reply_markup=keyboard)
    else:
        await send_stage_message(update, "Вы завершили курс!", header="Обучение",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton("Домой", callback_data="edu_home")]
                                   ]))

# --------------------------------------------------
# Навигация по блокам курса
# --------------------------------------------------
async def course_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    course = data.get("edu_course")
    blocks = get_course_blocks(course)
    index = data.get("block_index", 0)
    if index < len(blocks) - 1:
        data["block_index"] = index + 1
        set_user_data(chat_id, data)
        await show_course_block(update, context)
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Пройти тест", callback_data="test_start"),
             InlineKeyboardButton("Домой", callback_data="edu_home")]
        ])
        await send_stage_message(update, "Вы успешно завершили курс!", header="Обучение", reply_markup=keyboard)

async def course_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    index = data.get("block_index", 0)
    if index > 0:
        data["block_index"] = index - 1
        set_user_data(chat_id, data)
        await show_course_block(update, context)
    else:
        course = data.get("edu_course")
        if course == "basic":
            await basic_course_summary(update, context)
        elif course == "advanced":
            await advanced_course_summary(update, context)
        elif course == "professional":
            await professional_course_summary(update, context)

async def course_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Пройти тест", callback_data="test_start"),
         InlineKeyboardButton("Домой", callback_data="edu_home")]
    ])
    await send_stage_message(update, "Вы успешно завершили курс!", header="Обучение", reply_markup=keyboard)

# --------------------------------------------------
# Тестирование курса
# --------------------------------------------------
# Тестовые вопросы для базового курса
BASIC_TEST = [
    {
        "question": "Какую основную функцию выполняет процессор (CPU) в компьютере?",
        "options": [
            "Он хранит данные для долгосрочного использования.",
            "Он выполняет вычисления и управляет работой системы.",
            "Он охлаждает остальные компоненты."
        ],
        "correct": 1
    },
    {
        "question": "Какую задачу выполняет оперативная память (RAM)?",
        "options": [
            "Хранит данные временно для быстрого доступа.",
            "Обеспечивает питание для всех компонентов.",
            "Устанавливает драйверы для видеокарты."
        ],
        "correct": 0
    },
    {
        "question": "Какую роль играет материнская плата?",
        "options": [
            "Соединяет и обеспечивает взаимодействие всех компонентов ПК.",
            "Увеличивает скорость интернет-соединения.",
            "Охлаждает процессор."
        ],
        "correct": 0
    }
]

ADVANCED_TEST = [
    {
        "question": "Что включает в себя подготовка рабочего места для сборки ПК?",
        "options": [
            "Организацию чистого и хорошо освещённого пространства и подготовку инструментов.",
            "Выбор видеокарты и блока питания.",
            "Установку операционной системы."
        ],
        "correct": 0
    },
    {
        "question": "Почему важна правильная установка процессора и системы охлаждения?",
        "options": [
            "Чтобы обеспечить стабильную работу и предотвратить перегрев.",
            "Чтобы улучшить звук в системе.",
            "Чтобы увеличить объём оперативной памяти."
        ],
        "correct": 0
    },
    {
        "question": "Что проверяется при первичном запуске системы?",
        "options": [
            "Правильность подключения всех компонентов и их распознавание BIOS.",
            "Цвет корпуса.",
            "Скорость работы интернета."
        ],
        "correct": 0
    }
]

PROFESSIONAL_TEST = [
    {
        "question": "Как оптимизация воздушного потока влияет на систему?",
        "options": [
            "Улучшает охлаждение и продлевает срок службы компонентов.",
            "Увеличивает тактовую частоту процессора без охлаждения.",
            "Не оказывает влияния на стабильность работы."
        ],
        "correct": 0
    },
    {
        "question": "Какие меры помогают защитить компоненты от статического электричества?",
        "options": [
            "Использование антистатического браслета и соблюдение правил работы с компонентами.",
            "Установка дополнительного блока питания.",
            "Отключение всех вентиляторов."
        ],
        "correct": 0
    },
    {
        "question": "Что включает в себя финальное тестирование системы?",
        "options": [
            "Проверку подключения кабелей.",
            "Стресс-тестирование, мониторинг температуры и проверку стабильности работы.",
            "Только установку операционной системы."
        ],
        "correct": 1
    }
]

async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    data = get_user_data(chat_id)
    course = data.get("edu_course")
    if course == "basic":
        data["test_questions"] = BASIC_TEST
    elif course == "advanced":
        data["test_questions"] = ADVANCED_TEST
    elif course == "professional":
        data["test_questions"] = PROFESSIONAL_TEST
    else:
        data["test_questions"] = []
    data["test_index"] = 0
    data["test_correct"] = 0
    set_user_data(chat_id, data)
    await show_test_question(update, context)

async def show_test_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    questions = data.get("test_questions", [])
    index = data.get("test_index", 0)
    if index < len(questions):
        qdata = questions[index]
        text = f"Вопрос {index+1}: {qdata['question']}\n\n"
        # Добавляем варианты ответов с нумерацией в текст сообщения
        for i, option in enumerate(qdata['options']):
            text += f"{i+1}) {option}\n"
        # Кнопки: отображается только номер варианта
        buttons = []
        for i in range(len(qdata['options'])):
            buttons.append(InlineKeyboardButton(str(i+1), callback_data=f"test_ans_{i}"))
        keyboard = InlineKeyboardMarkup([buttons])
        await send_stage_message(update, text, header="Тест", reply_markup=keyboard)
    else:
        await show_test_result(update, context)

async def test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    questions = data.get("test_questions", [])
    index = data.get("test_index", 0)
    if index < len(questions):
        selected = int(query.data.split("_")[-1])
        correct = questions[index]['correct']
        if selected == correct:
            data["test_correct"] = data.get("test_correct", 0) + 1
        data["test_index"] = index + 1
        set_user_data(chat_id, data)
        await show_test_question(update, context)
    else:
        await show_test_result(update, context)

async def show_test_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    total = len(data.get("test_questions", []))
    correct = data.get("test_correct", 0)
    text = f"Вы ответили правильно на {correct} из {total} вопросов."
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Пройти тест снова", callback_data="test_start"),
         InlineKeyboardButton("Домой", callback_data="edu_home")]
    ])
    await send_stage_message(update, text, header="Результаты теста", reply_markup=keyboard)

async def test_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_test(update, context)

# --------------------------------------------------
# Навигация по блокам курса
# --------------------------------------------------
async def course_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    course = data.get("edu_course")
    blocks = []
    if course == "basic":
        blocks = BASIC_COURSE_BLOCKS
    elif course == "advanced":
        blocks = ADVANCED_COURSE_BLOCKS
    elif course == "professional":
        blocks = PROFESSIONAL_COURSE_BLOCKS
    index = data.get("block_index", 0)
    if index < len(blocks) - 1:
        data["block_index"] = index + 1
        set_user_data(chat_id, data)
        await show_course_block(update, context)
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Пройти тест", callback_data="test_start"),
             InlineKeyboardButton("Домой", callback_data="edu_home")]
        ])
        await send_stage_message(update, "Вы успешно завершили курс!", header="Обучение", reply_markup=keyboard)

async def course_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    index = data.get("block_index", 0)
    if index > 0:
        data["block_index"] = index - 1
        set_user_data(chat_id, data)
        await show_course_block(update, context)
    else:
        course = data.get("edu_course")
        if course == "basic":
            await basic_course_summary(update, context)
        elif course == "advanced":
            await advanced_course_summary(update, context)
        elif course == "professional":
            await professional_course_summary(update, context)

async def course_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Пройти тест", callback_data="test_start"),
         InlineKeyboardButton("Домой", callback_data="edu_home")]
    ])
    await send_stage_message(update, "Вы успешно завершили курс!", header="Обучение", reply_markup=keyboard)

# --------------------------------------------------
# Отображение текущего блока курса с навигацией
# --------------------------------------------------
async def show_course_block(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    course = data.get("edu_course")
    blocks = []
    if course == "basic":
        blocks = BASIC_COURSE_BLOCKS
    elif course == "advanced":
        blocks = ADVANCED_COURSE_BLOCKS
    elif course == "professional":
        blocks = PROFESSIONAL_COURSE_BLOCKS
    index = data.get("block_index", 0)
    if index < len(blocks):
        block_text = blocks[index]
        nav_buttons = []
        if index > 0:
            nav_buttons.append(InlineKeyboardButton("Назад", callback_data="course_prev"))
        else:
            nav_buttons.append(InlineKeyboardButton("Назад", callback_data="edu_back"))
        if index < len(blocks) - 1:
            nav_buttons.append(InlineKeyboardButton("Дальше", callback_data="course_next"))
        else:
            nav_buttons.append(InlineKeyboardButton("Завершить курс", callback_data="course_finish"))
        nav_buttons.append(InlineKeyboardButton("Домой", callback_data="edu_home"))
        keyboard = InlineKeyboardMarkup([nav_buttons])
        await send_stage_message(update, block_text, header="Обучение", reply_markup=keyboard)
    else:
        await send_stage_message(update, "Вы завершили курс!", header="Обучение",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton("Домой", callback_data="edu_home")]
                                   ]))

# --------------------------------------------------
# Регистрация обработчиков для обучающего режима
# --------------------------------------------------
def setup_handlers(app):
    # Запуск обучающего режима
    app.add_handler(CommandHandler("educational_mode", start_educational_mode))
    app.add_handler(CallbackQueryHandler(start_educational_mode, pattern="^educational_mode$"))
    # Выбор курса
    app.add_handler(CallbackQueryHandler(basic_course_summary, pattern="^basic_course$"))
    app.add_handler(CallbackQueryHandler(advanced_course_summary, pattern="^advanced_course$"))
    app.add_handler(CallbackQueryHandler(professional_course_summary, pattern="^professional_course$"))
    # Запуск курса
    app.add_handler(CallbackQueryHandler(basic_start, pattern="^basic_start$"))
    app.add_handler(CallbackQueryHandler(advanced_start, pattern="^advanced_start$"))
    app.add_handler(CallbackQueryHandler(professional_start, pattern="^professional_start$"))
    # Навигация по блокам курса
    app.add_handler(CallbackQueryHandler(course_next, pattern="^course_next$"))
    app.add_handler(CallbackQueryHandler(course_prev, pattern="^course_prev$"))
    app.add_handler(CallbackQueryHandler(course_finish, pattern="^course_finish$"))
    # Кнопка "Назад" на странице описания курса возвращает к выбору курса
    app.add_handler(CallbackQueryHandler(start_educational_mode, pattern="^edu_back$"))
    # Кнопка "Домой" возвращает в главное меню бота
    app.add_handler(CallbackQueryHandler(edu_go_home, pattern="^edu_home$"))
    # Тестирование: запуск теста
    app.add_handler(CallbackQueryHandler(test_start, pattern="^test_start$"))
    # Тестирование: обработка ответа на вопрос (callback_data вида test_ans_X)
    app.add_handler(CallbackQueryHandler(test_answer, pattern="^test_ans_"))