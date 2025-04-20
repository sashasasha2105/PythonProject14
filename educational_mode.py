# educational_mode.py
# -*- coding: utf-8 -*-

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes
from utils import get_user_data, set_user_data

# ─── СОДЕРЖАНИЕ КУРСОВ ─────────────────────────────────────────────

# Базовый курс: «Основные компоненты ПК» (5 блоков)
BASIC_COURSE_BLOCKS = [
    (
        "Блок 1. Процессор (CPU) — мозг компьютера 🧠\n\n"
        "Процессор отвечает за выполнение всех вычислений и управление остальными частями ПК:\n"
        "• Ядра и потоки: каждое ядро обрабатывает задачи, потоки позволяют одному ядру решать несколько задач одновременно.\n"
        "• Тактовая частота (ГГц): показывает, сколько операций может выполнить ядро за секунду.\n"
        "• Кэш‑память (L1, L2, L3): сверхбыстрое хранилище для часто используемых данных.\n"
        "• Интегрированная графика: встроенный видеочип для простых игр и воспроизведения видео."
    ),
    (
        "Блок 2. Оперативная память (RAM) — рабочая зона 🗂️\n\n"
        "ОЗУ хранит данные и программы, с которыми сейчас работает процессор:\n"
        "• Тип DDR3/DDR4/DDR5: влияет на скорость и энергопотребление.\n"
        "• Форм‑фактор UDIMM (десктоп) и SO‑DIMM (ноутбук).\n"
        "• Ёмкость (4–32 ГБ): чем больше, тем больше одновременно открытых программ.\n"
        "• Частота (MT/s) и задержки (CL): чем выше — тем быстрее отклик.\n"
        "• Двух‑ и четырёхканальный режим: повышает пропускную способность."
    ),
    (
        "Блок 3. Материнская плата — центр соединений 🏛️\n\n"
        "Материнка объединяет все компоненты и распределяет питание:\n"
        "• Форм‑фактор ATX/microATX/Mini‑ITX определяет размер и число слотов.\n"
        "• Чипсет задаёт функции (разгон, интерфейсы, количество портов).\n"
        "• VRM (модули питания) обеспечивает стабильное напряжение CPU.\n"
        "• Слоты PCIe, M.2, SATA; порты USB, аудио, Ethernet — для подключаемых устройств."
    ),
    (
        "Блок 4. Накопители — долгосрочное хранение 📚\n\n"
        "Накопители хранят операционную систему и файлы:\n"
        "• HDD: дешёвый, большой объём (1–10 ТБ), вращение 5400–7200 об/мин.\n"
        "• SATA SSD: до 550 МБ/с, гораздо быстрее HDD, компактный.\n"
        "• NVMe SSD: подключение к PCIe, скорость 1,5–7 ГБ/с.\n"
        "• Рекомендация: ОС и программы на SSD, большие архивы — на HDD."
    ),
    (
        "Блок 5. Блок питания и охлаждение ❤️❄️\n\n"
        "PSU питает все компоненты, охлаждение предотвращает перегрев:\n"
        "• 80 PLUS Bronze/Gold/Platinum: эффективность от 82% до 94%+.\n"
        "• Модульные кабели: подключайте только необходимые для аккуратной укладки.\n"
        "• Воздушные кулеры: радиатор + вентилятор — простой монтаж и обслуживание.\n"
        "• AIO‑системы: водоблок, трубки, радиатор — высокая эффективность при аккуратной установке."
    ),
]

# Продвинутый курс: «Практическая сборка и проверка» (6 блоков)
ADVANCED_COURSE_BLOCKS = [
    (
        "Блок 1. Подготовка рабочего места и инструментов 🛠️\n\n"
        "1) Выберите ровный, чистый стол без ковров — это снижает статический заряд.\n"
        "2) Наденьте антистатический браслет или постелите антистатический коврик.\n"
        "3) Разложите всё так:\n"
        "   – Материнская плата на картоне или коврике.\n"
        "   – CPU, кулер, ОЗУ, накопители, БП и видеокарта по отдельным зонам.\n"
        "4) Приготовьте инструменты:\n"
        "   – Отвёртки PH1 и PH2.\n"
        "   – Пинцет для мелких деталей.\n"
        "   – Бокорезы и стяжки для кабелей.\n"
        "   – Контейнер или магнитная подставка для винтов."
    ),
    (
        "Блок 2. Установка процессора и термопасты ⛏️🔥\n\n"
        "1) Аккуратно откройте рычаг сокета и поднимите рамку.\n"
        "2) Совместите треугольники на CPU и на сокете.\n"
        "3) Опустите процессор ровно, защёлкните рамку и зафиксируйте рычаг.\n"
        "4) Нанесите термопасту:\n"
        "   – Капля размером с горошину в центр крышки CPU.\n"
        "   – При установке кулера паста распределится равномерно по поверхности."
    ),
    (
        "Блок 3. Монтаж системы охлаждения и подключение вентиляторов ❄️🔌\n\n"
        "Воздушный кулер:\n"
        "• Установите back‑plate за платой, прикрутите стойки крест‑накрест «от руки».\n"
        "• Наденьте радиатор, затем вентилятор, направив стрелку воздуха к задней панели корпуса.\n"
        "• Подключите кабель 4‑pin к разъёму CPU_FAN.\n\n"
        "AIO‑система:\n"
        "• Снимите защитную плёнку с водоблока.\n"
        "• Закрепите водоблок на CPU барашковыми гайками крест‑накрест.\n"
        "• Прикрепите радиатор к корпусу, подключите вентиляторы и помпу к PSU."
    ),
    (
        "Блок 4. Установка памяти и видеокарты 🧩🎮\n\n"
        "Оперативная память:\n"
        "• Откройте защёлки слотов A2 и B2 для двухканального режима.\n"
        "• Совместите вырезы модуля с ключом слота, нажмите до щелчка.\n"
        "• Убедитесь, что модули стоят ровно и защёлки закрыты.\n\n"
        "Видеокарта:\n"
        "• Снимите заглушки PCIe на задней панели корпуса.\n"
        "• Вставьте карту в слот PCIe x16 до щелчка защёлки.\n"
        "• Закрепите винтом, подключите питание (6/8‑pin или 12VHPWR).\n"
        "• При тяжёлых картах используйте дополнительную опору снизу."
    ),
    (
        "Блок 5. Накопители и кабель‑менеджмент 💾🪢\n\n"
        "Накопители:\n"
        "• Закрепите 2.5″ SSD/HDD винтами в монтажных отсеках.\n"
        "• Вставьте M.2 SSD под углом ~30° и закрепите винтом‑фиксатор.\n\n"
        "Кабели:\n"
        "• SATA‑кабель к плате и к накопителю.\n"
        "• Питание от БП (SATA Power) к накопителю.\n"
        "• Кабели фронт‑панели (Power, Reset, LED) строго по маркировке на PCB.\n\n"
        "Менеджмент:\n"
        "• Прячьте жгуты за поддоном корпуса.\n"
        "• Фиксируйте стяжками каждые 10–15 см для свободного воздушного потока."
    ),
    (
        "Блок 6. Первичный запуск, BIOS и установка ОС 🚦💻\n\n"
        "1) Подключите монитор, клавиатуру, мышь и сетевой кабель.\n"
        "2) Включите ПК и нажмите Delete/F2 для входа в BIOS.\n"
        "3) Проверьте:\n"
        "   – CPU и его температуру в простое.\n"
        "   – Объём и расположение модулей ОЗУ.\n"
        "   – Накопители в списке устройств.\n"
        "4) Сохраните настройки и перезагрузитесь с загрузочного носителя.\n"
        "5) Установите ОС:\n"
        "   – Создайте разделы: EFI (~100 МБ), MSR (~16 МБ для Windows), основной раздел.\n"
        "   – Следуйте подсказкам установщика.\n"
        "6) После установки ОС:\n"
        "   – Установите драйверы чипсета, GPU, аудио, сети.\n"
        "   – Выполните полное обновление системы."
    ),
]

# Профессиональный курс: «Оптимизация и диагностика» (7 блоков)
PROFESSIONAL_COURSE_BLOCKS = [
    (
        "Блок 1. Проектирование воздушного потока и критичные детали 🌬️🧰\n\n"
        "Правильный airflow — залог низких температур и тихой работы:\n"
        "1) Intake‑вентиляторы спереди и/или снизу корпуса:\n"
        "   • Подбирайте скорость так, чтобы входящего воздуха было чуть больше, чем выходящего (положительное давление).\n"
        "   • Устанавливайте пылевые фильтры и чистите их регулярно.\n\n"
        "2) Exhaust‑вентиляторы сверху и сзади:\n"
        "   • Удаляют горячий воздух из корпуса.\n"
        "   • Высота установки влияет на эффективность удаления нагретого воздуха.\n\n"
        "3) Внутреннее пространство:\n"
        "   • Кабели не должны препятствовать потоку воздуха — прячьте их за поддоном и фиксируйте стяжками.\n"
        "   • Расположение накопителей не должно блокировать intake-вентиляторы.\n\n"
        "4) Мониторинг:\n"
        "   • Сравнивайте температуры GPU/CPU в простое и под нагрузкой, корректируйте конфигурацию при необходимости."
    ),
    (
        "Блок 2. Электростатическая защита и профилактика ⚡🛡️\n\n"
        "Защита от ESD — обязательный этап сборки:\n"
        "1) Антистатический браслет:\n"
        "   • Надевайте на запястье и заземляйте на корпус БП.\n"
        "   • Проверяйте контакт каждые 10–15 минут во время работы.\n\n"
        "2) Антистатический коврик:\n"
        "   • Подложите под материнскую плату и мелкие детали.\n"
        "   • Работайте босиком или в обуви на нескользящей подошве.\n\n"
        "3) Окружение:\n"
        "   • Снимайте синтетическую одежду — она генерирует статику.\n"
        "   • Поддерживайте влажность 40–60 % для снижения риска ESD."
    ),
    (
        "Блок 3. Кабель‑менеджмент и эстетика сборки 🎨🔗\n\n"
        "Упорядоченная проводка улучшает airflow и внешний вид:\n"
        "1) Группировка:\n"
        "   • Питание (24‑pin, EPS, PCIe) по одной стороне корпуса.\n"
        "   • Данные (SATA, USB) параллельными жгутами.\n\n"
        "2) Фиксация:\n"
        "   • Стяжки или липучки каждые 10–15 см.\n"
        "   • Используйте кабельные каналы и отверстия корпуса.\n\n"
        "3) Маркировка:\n"
        "   • Цветные кабели или метки помогают при обслуживании.\n"
        "   • Отмечайте основные разъёмы (USB, SATA, ARGB)."
    ),
    (
        "Блок 4. Разгон (OC) и стресс‑тестирование 💪📈\n\n"
        "Повышение производительности без потери стабильности:\n"
        "1) Настройки BIOS:\n"
        "   • Включите XMP/DOCP профиль памяти для автоматической настройки частоты.\n"
        "   • Повышайте множитель CPU и Vcore малыми шагами (по 100 МГц и +0.01 В).\n\n"
        "2) Стресс‑тесты:\n"
        "   • Prime95/Blend для CPU — следите за температурами и стабильностью.\n"
        "   • MemTest86 для RAM — минимум 4 прохода.\n\n"
        "3) Мониторинг:\n"
        "   • Используйте HWiNFO или AIDA64 для графиков температуры и напряжений.\n"
        "   • Ведите логи, чтобы видеть динамику изменений."
    ),
    (
        "Блок 5. Стабильность при высоких нагрузках 🏋️‍♂️🔋\n\n"
        "Надёжное питание и защита:\n"
        "1) PSU с запасом мощности 20–30 % от потребления системы и сертификатом 80 PLUS Gold/Platinum.\n"
        "2) ИБП (UPS) для защиты от отключений и просадок напряжения.\n"
        "3) Сетевой фильтр с AV‑защитой от импульсных помех.\n"
        "4) Мониторинг потребления через BIOS/OS — корректируйте частоты при перегрузках."
    ),
    (
        "Блок 6. Системный мониторинг и логирование 📊📝\n\n"
        "Непрерывный контроль параметров продлевает сроки службы компонентов:\n"
        "1) ПО для мониторинга:\n"
        "   • HWiNFO, MSI Afterburner, AIDA64 — в реальном времени показывают температуру, обороты вентиляторов и напряжения.\n"
        "   • Включите запись логов или OSD‑отображение на экране.\n\n"
        "2) Оповещения:\n"
        "   • Установите пороги (например, CPU > 80 °C) — получите предупреждение или автоматическое понижение частот.\n\n"
        "3) Анализ трендов:\n"
        "   • Сравнивайте графики за месяцы/годы для прогнозирования износа термопасты и вентиляторов."
    ),
    (
        "Блок 7. Диагностика и устранение неисправностей 🕵️‍♂️🔧\n\n"
        "Методичное выявление и решение проблем:\n"
        "1) Сборка минимальной конфигурации (CPU + RAM + GPU) и запуск POST — изоляция неисправностей.\n"
        "2) Поочерёдное подключение накопителей, вентиляторов и дополнительных плат с каждым запуском.\n"
        "3) Использование POST‑кодов и индикаторов на плате для быстрой диагностики.\n"
        "4) Сброс CMOS и обновление BIOS для устранения проблем совместимости."
    ),
]

# ─── КРАТКИЕ ОПИСАНИЯ ─────────────────────────────────────────────

BASIC_SUMMARY        = "📘 Базовый курс (5 блоков). Краткий обзор ключевых компонентов ПК."
ADVANCED_SUMMARY     = "📗 Продвинутый курс (6 блоков). Пошаговая сборка и тестирование."
PROFESSIONAL_SUMMARY = "📙 Профессиональный курс (7 блоков). Глубокая оптимизация и диагностика."

# ─── ГЛАВНОЕ МЕНЮ ────────────────────────────────────────────────

MAIN_MENU_TEXT = (
    "👋 Привет! Я Академия ПК — ваш надёжный помощник.\n\n"
    "• Ассистент сборки ПК — пошаговая инструкция сборки.\n"
    "• Обучающий режим — курсы и тесты для любого уровня.\n"
    "• Интерактивный режим — проверка знаний в игровой форме.\n\n"
    "Выберите режим:"
)

def build_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Ассистент сборки ПК", callback_data="assistant_pc")],
        [InlineKeyboardButton("Обучающий режим", callback_data="educational_mode")],
        [InlineKeyboardButton("Интерактивный режим", callback_data="game_mode")]
    ])

def format_header(header: str) -> str:
    if header == "Обучение":
        return f"🎓 {header} 🎓"
    if header == "Тест":
        return f"📝 {header} 📝"
    return header

def minimal_send_message(text: str, header: str = "") -> str:
    return f"<b>{format_header(header)}</b>\n{text}" if header else text

async def send_stage_message(update: Update, text: str, header: str = "", reply_markup=None):
    await update.effective_message.reply_text(
        minimal_send_message(text, header),
        parse_mode='HTML',
        reply_markup=reply_markup
    )

# ─── ИНТЕГРАЦИЯ КНОПКИ "ГЛАВНОЕ МЕНЮ" ─────────────────────────────

async def edu_go_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # ленивый импорт, чтобы избежать циклического импорта
    from main import start_main_menu
    # очищаем состояние
    set_user_data(update.effective_chat.id, {})
    await start_main_menu(update, context)

# ─── СТАРТ И ВЫБОР КУРСА ────────────────────────────────────────────

async def start_educational_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # сброс предыдущего прогресса
    set_user_data(update.effective_chat.id, {})
    text = "🎓 Режим обучения 🎓\n\nВыберите курс для изучения:"
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 Базовый курс", callback_data="basic_course")],
        [InlineKeyboardButton("📗 Продвинутый курс", callback_data="advanced_course")],
        [InlineKeyboardButton("📙 Профессиональный курс", callback_data="professional_course")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="edu_home")]
    ])
    await update.effective_message.reply_text(text, reply_markup=kb)

async def basic_course_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"{BASIC_SUMMARY}\n\nНажмите «Начать», чтобы приступить к базовому курсу."
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Назад", callback_data="edu_back"),
        InlineKeyboardButton("Начать", callback_data="basic_start"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="edu_home")
    ]])
    await update.effective_message.edit_text(text, reply_markup=kb, parse_mode='HTML')

async def advanced_course_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"{ADVANCED_SUMMARY}\n\nНажмите «Начать», чтобы приступить к продвинутому курсу."
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Назад", callback_data="edu_back"),
        InlineKeyboardButton("Начать", callback_data="advanced_start"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="edu_home")
    ]])
    await update.effective_message.edit_text(text, reply_markup=kb, parse_mode='HTML')

async def professional_course_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"{PROFESSIONAL_SUMMARY}\n\nНажмите «Начать», чтобы приступить к профессиональному курсу."
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Назад", callback_data="edu_back"),
        InlineKeyboardButton("Начать", callback_data="professional_start"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="edu_home")
    ]])
    await update.effective_message.edit_text(text, reply_markup=kb, parse_mode='HTML')

def get_course_blocks(course: str):
    return {
        "basic": BASIC_COURSE_BLOCKS,
        "advanced": ADVANCED_COURSE_BLOCKS,
        "professional": PROFESSIONAL_COURSE_BLOCKS
    }.get(course, [])

async def start_course(update: Update, context: ContextTypes.DEFAULT_TYPE, course: str):
    chat_id = update.effective_chat.id
    set_user_data(chat_id, {"edu_course": course, "block_index": 0})
    await show_course_block(update, context)

async def basic_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_course(update, context, "basic")

async def advanced_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_course(update, context, "advanced")

async def professional_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_course(update, context, "professional")

async def show_course_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    blocks = get_course_blocks(data.get("edu_course", ""))
    idx = data.get("block_index", 0)
    if idx < len(blocks):
        text = blocks[idx]
        buttons = []
        if idx > 0:
            buttons.append(InlineKeyboardButton("Назад", callback_data="course_prev"))
        else:
            buttons.append(InlineKeyboardButton("Назад", callback_data="edu_back"))
        if idx < len(blocks) - 1:
            buttons.append(InlineKeyboardButton("Дальше", callback_data="course_next"))
        else:
            buttons.append(InlineKeyboardButton("Завершить курс", callback_data="course_finish"))
        buttons.append(InlineKeyboardButton("🏠 Главное меню", callback_data="edu_home"))
        kb = InlineKeyboardMarkup([buttons])
        await send_stage_message(update, text, header="Обучение", reply_markup=kb)
    else:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Главное меню", callback_data="edu_home")]])
        await send_stage_message(update, "Вы успешно завершили курс!", header="Обучение", reply_markup=kb)

async def course_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    data["block_index"] = data.get("block_index", 0) + 1
    set_user_data(chat_id, data)
    await show_course_block(update, context)

async def course_prev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    idx = data.get("block_index", 0)
    if idx > 0:
        data["block_index"] = idx - 1
        set_user_data(chat_id, data)
        await show_course_block(update, context)
    else:
        course = data.get("edu_course", "")
        if course == "basic":
            await basic_course_summary(update, context)
        elif course == "advanced":
            await advanced_course_summary(update, context)
        else:
            await professional_course_summary(update, context)

async def course_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Пройти тест", callback_data="test_start")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="edu_home")]
    ])
    await send_stage_message(update, "Вы успешно завершили курс!", header="Обучение", reply_markup=kb)

# ─── ТЕСТИРОВАНИЕ С РАЗБОРОМ ОШИБОК ─────────────────────────────

BASIC_TEST = [
    {"question": "Какова основная роль процессора?", "options": ["Хранит файлы", "Выполняет команды", "Охлаждает систему"], "correct": 1},
    {"question": "Для чего нужна оперативная память?", "options": ["Временное хранилище данных", "Питание компонентов", "Охлаждение"], "correct": 0},
    {"question": "Что делает материнская плата?", "options": ["Соединяет компоненты", "Увеличивает скорость интернета", "Запускает приложения"], "correct": 0},
]
ADVANCED_TEST = [
    {"question": "Что нужно подготовить перед сборкой?", "options": ["Чистое место и инструменты", "Только отвертку", "Только винты"], "correct": 0},
    {"question": "Зачем нужна термопаста?", "options": ["Для отвода тепла", "Для питания кулера", "Для звука"], "correct": 0},
    {"question": "Что проверяется в BIOS при первом запуске?", "options": ["Распознавание компонентов", "Цвет подсветки", "Скорость интернета"], "correct": 0},
]
PROFESSIONAL_TEST = [
    {"question": "Почему важно продумывать airflow?", "options": ["Для эффективного охлаждения", "Для повышения FPS без кулеров", "Не важно"], "correct": 0},
    {"question": "Как защититься от статического разряда?", "options": ["Антистатическим браслетом", "Закрыть окна", "Надеть перчатки"], "correct": 0},
    {"question": "Что включает разбор ошибок после теста?", "options": ["Анализ неверных ответов", "Только итоговый балл", "Скорость сети"], "correct": 0},
]

async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query or update
    chat_id = query.message.chat_id if hasattr(query, 'message') else update.effective_chat.id
    data = get_user_data(chat_id)
    course = data.get("edu_course", "")
    tests = {"basic": BASIC_TEST, "advanced": ADVANCED_TEST, "professional": PROFESSIONAL_TEST}
    data["test_questions"] = tests.get(course, [])
    data["test_index"] = 0
    data["test_correct"] = 0
    data["wrong_answers"] = []
    set_user_data(chat_id, data)
    await show_test_question(update, context)

async def show_test_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    qs = data.get("test_questions", [])
    idx = data.get("test_index", 0)
    if idx < len(qs):
        qd = qs[idx]
        text = f"<b>Вопрос {idx+1}:</b> {qd['question']}\n\n"
        for i, opt in enumerate(qd["options"]):
            text += f"{i+1}) {opt}\n"
        buttons = [InlineKeyboardButton(str(i+1), callback_data=f"test_ans_{i}") for i in range(len(qd["options"]))]
        buttons.append(InlineKeyboardButton("🏠 Главное меню", callback_data="edu_home"))
        kb = InlineKeyboardMarkup([buttons])
        await send_stage_message(update, text, header="Тест", reply_markup=kb)
    else:
        await show_test_result(update, context)

async def test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    idx = data.get("test_index", 0)
    qs = data.get("test_questions", [])
    if idx < len(qs):
        sel = int(query.data.split("_")[-1])
        corr = qs[idx]["correct"]
        if sel == corr:
            data["test_correct"] += 1
        else:
            data["wrong_answers"].append({"index": idx, "selected": sel, "correct": corr})
        data["test_index"] += 1
        set_user_data(chat_id, data)
        await show_test_question(update, context)
    else:
        await show_test_result(update, context)

async def show_test_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = get_user_data(chat_id)
    total = len(data.get("test_questions", []))
    correct = data.get("test_correct", 0)
    text = f"<b>Результаты теста:</b>\nПравильно: {correct} из {total}.\n\n"
    wrongs = data.get("wrong_answers", [])
    if wrongs:
        text += "<b>Разбор ошибок:</b>\n"
        for w in wrongs:
            qd = data["test_questions"][w["index"]]
            sel = qd["options"][w["selected"]]
            corr = qd["options"][w["correct"]]
            text += f"Вопрос {w['index']+1}: вы выбрали «{sel}», правильный ответ — «{corr}».\n"
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Пройти тест снова", callback_data="test_start")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="edu_home")]
    ])
    await send_stage_message(update, text, header="Тест", reply_markup=kb)

async def test_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_test(update, context)

# ─── РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ ─────────────────────────────────────

def setup_handlers(app):
    app.add_handler(CommandHandler("educational_mode", start_educational_mode))
    app.add_handler(CallbackQueryHandler(start_educational_mode,      pattern="^educational_mode$"))
    app.add_handler(CallbackQueryHandler(basic_course_summary,       pattern="^basic_course$"))
    app.add_handler(CallbackQueryHandler(advanced_course_summary,    pattern="^advanced_course$"))
    app.add_handler(CallbackQueryHandler(professional_course_summary,pattern="^professional_course$"))
    app.add_handler(CallbackQueryHandler(basic_start,                pattern="^basic_start$"))
    app.add_handler(CallbackQueryHandler(advanced_start,             pattern="^advanced_start$"))
    app.add_handler(CallbackQueryHandler(professional_start,         pattern="^professional_start$"))
    app.add_handler(CallbackQueryHandler(course_next,                pattern="^course_next$"))
    app.add_handler(CallbackQueryHandler(course_prev,                pattern="^course_prev$"))
    app.add_handler(CallbackQueryHandler(course_finish,              pattern="^course_finish$"))
    app.add_handler(CallbackQueryHandler(start_educational_mode,     pattern="^edu_back$"))
    app.add_handler(CallbackQueryHandler(edu_go_home,                pattern="^edu_home$"))
    app.add_handler(CallbackQueryHandler(test_start,                 pattern="^test_start$"))
    app.add_handler(CallbackQueryHandler(test_answer,                pattern="^test_ans_"))
    # ок