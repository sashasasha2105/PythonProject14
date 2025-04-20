# -*- coding: utf-8 -*-
"""
assistant_pc.py — Ассистент сборки ПК (расширенная версия).
Дата: 20 апр 2025
"""

from pathlib import Path
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from data import (
    steps, cooling_instructions, ram_instructions,
    fan_instructions, power_supply_instructions,
    gpu_instructions, wires_instructions
)
from utils import get_user_data, set_user_data

# ─────────────────────────────────────────────────────────────
# 1 ▸ Тексты шагов
# ─────────────────────────────────────────────────────────────
PREPARATION_FULL = """
<b>🔧 Подготовка рабочего места</b>

1️⃣ <b>Стол</b> — ровная поверхность минимум 80×60 см.  
2️⃣ <b>Антистатика</b> — браслет + клипса к корпусу БП или касайтесь металла каждые 2 мин.  
3️⃣ <b>Инструменты</b> — PH2, PH1, плоскогубцы, пинцет, бокорезы, стяжки, термопаста, салфетки.  
4️⃣ <b>Раскладка</b> — корпус без панелей, матплата на коробке, комплектующие рядом.  
5️⃣ <b>Освещение</b> — яркая лампа, 20–26 °C, без сквозняков и пыли.
""".strip()

# CPU
steps["Intel"]["instructions"][0] = """
<b>⚙️ Установка процессора Intel (LGA‑сокет)</b>

1️⃣ Откройте рычаг и поднимите рамку сокета.  
2️⃣ Совместите золотой треугольник на CPU с меткой на сокете.  
3️⃣ Опустите процессор строго вертикально, не давите.  
4️⃣ Закройте рамку и опустите рычаг до щелчка.  
5️⃣ Проверьте, что CPU не шатается.

⚠️ Не касайтесь контактных площадек пальцами!  
<a href="https://rutube.ru/video/1c42d5692ee827b3c815e963bc1dcac0/">Видео Intel</a>
""".strip()

steps["AMD"]["instructions"][0] = """
<b>⚙️ Установка процессора AMD (AM4/AM5)</b>

<b>AM4 (PGA)</b>  
1️⃣ Поднимите рычаг на 90°.  
2️⃣ Совместите треугольник CPU с меткой сокета.  
3️⃣ Опустите CPU, затем опустите рычаг.

<b>AM5 (LGA)</b>  
1️⃣ Откройте рамку, приподняв фиксатор.  
2️⃣ Совместите направляющие CPU и сокета.  
3️⃣ Опустите CPU строго вертикально.  
4️⃣ Закройте рамку до щелчка.

⚠️ Не сгибайте ножки и не касайтесь площадок!  
<a href="https://rutube.ru/video/cf6d5d2cfbe19149fde57551e8e53022/">Видео AMD</a>
""".strip()

# RAM
ram_instructions.update({
    "1": """
<b>💾 Установка 1 планки ОЗУ</b>

1️⃣ Откройте защелки слота A2.  
2️⃣ Совместите вырез модуля и паз слота.  
3️⃣ Нажмите до щелчка, защелки закроются.  
4️⃣ Проверьте выравнивание.
""".strip(),
    "2": """
<b>💾 Установка 2 планок (двухканал)</b>

1️⃣ Откройте защелки A2 и B2.  
2️⃣ Вставьте оба модуля, нажмите до щелчков.  
3️⃣ Убедитесь в равном положении.
""".strip(),
    "4": """
<b>💾 Установка 4 планок (четырёхканал)</b>

1️⃣ Откройте все защелки.  
2️⃣ Вставьте A1→B1→A2→B2.  
3️⃣ Нажмите до щелчков, проверьте выравнивание.
""".strip(),
})

# M.2
M2_DETAILED = """
<b>🗜️ Установка M.2 SSD</b>

1️⃣ Отверните винтик‑фиксатор и положите рядом.  
2️⃣ Вставьте SSD под углом ~30° до упора.  
3️⃣ Опустите горизонтально, совместите отверстие.  
4️⃣ Закрутите винт пальцами — не перетягивайте.  
5️⃣ При наличии радиатора установите его поверх SSD.  
<a href="https://rutube.ru/video/fa86b5395ed102e415eb00d8a3b2f9fd/">Видео M.2</a>
""".strip()

# Cooling
cooling_instructions["Intel"]["air"] = """
<b>🌀 Воздушный кулер Intel (башня)</b>

1️⃣ Установите back‑plate за платой.  
2️⃣ Вверните стойки, прикрутите рамку.  
3️⃣ Наденьте радиатор, закрепите крест‑накрест.  
4️⃣ Прикрутите вентилятор стрелой к задней панели.  
5️⃣ Подключите 4‑pin к <code>CPU_FAN</code>.  
<a href="https://yandex.ru/video/preview/15387608359965564597">Видео Intel air</a>
""".strip()

cooling_instructions["Intel"]["water"] = """
<b>💧 AIO Intel</b>

1️⃣ Установите back‑plate и стойки.  
2️⃣ Снимите плёнку с водоблока.  
3️⃣ Надавите, закрутите крест‑накрест.  
4️⃣ Прикрутите вентиляторы стрелками наружу.  
5️⃣ Подключите Pump→<code>PUMP_FAN</code>, Fans→<code>SYS_FAN</code>.  
<a href="https://yandex.ru/video/preview/8565882692027585885">Видео Intel water</a>
""".strip()

cooling_instructions["AMD"]["air"] = """
<b>🌀 Воздушный кулер AMD (AM4/AM5)</b>

1️⃣ Установите лапы кулера на стойки.  
2️⃣ Наденьте радиатор вертикально.  
3️⃣ Закрутите пружинные винты по диагонали.  
4️⃣ Прикрутите вентилятор стрелкой наружу.  
5️⃣ Подключите к <code>CPU_FAN</code>.  
<a href="https://rutube.ru/video/2d0be3979a44d55577b5ec1ac4902b36/">Видео AMD air</a>
""".strip()

cooling_instructions["AMD"]["water"] = """
<b>💧 AIO AMD</b>

1️⃣ Вкрутите стойки в штатный back‑plate.  
2️⃣ Снимите плёнку, установите блок.  
3️⃣ Закрутите крест‑накрест.  
4️⃣ Подключите Fans→<code>SYS_FAN</code>, Pump→<code>PUMP_FAN</code>.  
5️⃣ ARGB/RGB → хедеры.  
<a href="https://www.youtube.com/watch?v=yjCPn3IZRJQ">Видео AMD water</a>
""".strip()

# Fans
fan_instructions.clear()
fan_instructions.update({
    "aquarium": """
<b>🌀 Аквариумный корпус</b>

1️⃣ Проверьте отверстия под 120/140 мм.  
2️⃣ Низ (вдув): 3×120, стрелка вверх.  
3️⃣ Бок (вдув): 2–3×120, стрелка внутрь.  
4️⃣ Верх (выдув): 3×140, стрелка наружу.  
5️⃣ Зад (выдув): 1×120, стрелка направо.  
6️⃣ Подключите:
   • <code>CPU_FAN</code> → кулер  
   • Нижние/боковые → HUB → <code>SYS_FAN1/2</code>  
   • Верхние/задние → <code>SYS_FAN3/4</code>  
7️⃣ ARGB: D‑Out→D‑In→<code>ARGB_HEADER</code>.  
8️⃣ Кабели стяжками за лотком.
""".strip(),
    "classic_bottom": """
<b>🌀 Классический корпус (БП внизу)</b>

1️⃣ Перед (вдув): 2–3×140, стрелка внутрь.  
2️⃣ Верх (выдув): 2×120, стрелка наружу.  
3️⃣ Зад (выдув): 1×120.  
4️⃣ Подключите:
   • Передние → HUB (SATA) → <code>SYS_FAN1</code>  
   • Верхние → Y‑кабель → <code>SYS_FAN2</code>  
   • Задний → <code>SYS_FAN3</code>  
5️⃣ ARGB → <code>ARGB_HEADER</code> + SATA.  
6️⃣ Кабели стяжками за лотком.
""".strip(),
    "classic_top": """
<b>🌀 Классический корпус (БП сверху)</b>

1️⃣ Перед (вдув): 2×120, стрелка внутрь.  
2️⃣ Зад (выдув): 1×120, стрелка наружу.  
3️⃣ Передние → Y‑кабель → <code>SYS_FAN1/2</code>  
4️⃣ Задний → <code>SYS_FAN3</code>  
5️⃣ ARGB → D‑Out→D‑In→<code>ARGB_HEADER</code>.  
6️⃣ Кабели под кожухом.
""".strip(),
    "already_installed": """
<b>🌀 Вентиляторы уже установлены</b>

1️⃣ Проверьте направление стрелок.  
2️⃣ Подключите:
   • <code>CPU_FAN</code> → кулер  
   • <code>SYS_FAN</code> → корпус  
3️⃣ ARGB 3‑pin → <code>ARGB_HEADER</code>, RGB 4‑pin → контроллер.  
4️⃣ Кабели стяжками.
""".strip(),
})

# PSU
power_supply_instructions = """
<b>🔌 Установка блока питания (ATX)</b>

1️⃣ Отключите питание и выньте кабель.  
2️⃣ Установите вентилятором вниз или к фильтру.  
3️⃣ Закрутите 4 винта крест‑накрест.  
4️⃣ Подключите:
   • ATX 24‑pin → матплата  
   • EPS 8‑pin → CPU  
   • PCI‑E/12VHPWR → GPU  
   • SATA Power → накопители и хабы  
   • Molex → старые устройства  
5️⃣ Кабели стяжками за лотком.  
6️⃣ Подключите кабель, включите тумблер «1».  
<a href="https://rutube.ru/video/98be6d9b389beee69b686336528481ea/">Видео PSU</a>
""".strip()

# GPU
gpu_instructions = """
<b>🎮 Установка видеокарты</b>

1️⃣ Снимите заглушки PCI‑E.  
2️⃣ Отожмите защелку слота.  
3️⃣ Вставьте карту ровно — щелчок.  
4️⃣ Закрутите винты.  
5️⃣ Подключите питание 6/8‑pin или 12VHPWR.  
6️⃣ Установите подпорку при необходимости.  
7️⃣ Кабели не мешают лопастям.
""".strip()

# Wires
wires_instructions = f"""
<b>🔗 Подключение кабелей</b>

1️⃣ ATX 24‑pin → правый край матплаты.  
2️⃣ EPS 8‑pin → верхний край.  
3️⃣ PCI‑E/12VHPWR → GPU.  
4️⃣ SATA Power → SSD/HDD, хабы.  
5️⃣ SATA Data → порт на плате.

6️⃣ Фронт‑панель PANEL1 (IMG_5330.jpg):
   • 1️⃣ HDD_LED+ → HDD+
   • 3️⃣ HDD_LED‑ → HDD‑
   • 2️⃣ PLED+ → PLED+
   • 4️⃣ PLED‑ → PLED‑
   • 5️⃣ RESET‑ → RES‑
   • 7️⃣ RESET+ → RES+
   • 6️⃣ POWER+ → PW+
   • 8️⃣ POWER‑ → PW‑
   • 9️⃣ KEY → пусто

🔟 Вентиляторы: CPU_FAN, SYS_FAN1/2/3, PUMP_FAN  
1️⃣1️⃣ ARGB / RGB (см. выше)  
1️⃣2️⃣ Кабели стяжками за лотком.
""".strip()

# OS
WIN_TEXT = """
<b>🖥️ Установка Windows 10/11</b>

1️⃣ Скачайте Media Creation Tool.  
2️⃣ Создайте UEFI‑GPT флешку (8 ГБ+).  
3️⃣ В BIOS включите AHCI, отключите Secure Boot.  
4️⃣ Загрузитесь с флешки (F11/F12/Esc).  
5️⃣ Разделы: EFI, MSR, NTFS.  
6️⃣ Установите драйверы и обновления.
""".strip()

LINUX_TEXT = """
<b>🐧 Установка Ubuntu 22.04 LTS</b>

1️⃣ Скачайте ISO, проверьте SHA256.  
2️⃣ Rufus (DD) или Etcher, UEFI‑GPT.  
3️⃣ BIOS: AHCI on, Secure Boot off.  
4️⃣ Загрузитесь → Install Ubuntu.  
5️⃣ Разметьте GPT: EFI, swap, ext4.  
6️⃣ <code>sudo ubuntu-drivers autoinstall</code>.  
7️⃣ <code>sudo apt update && sudo apt upgrade -y</code>.
""".strip()

MAC_TEXT = """
<b>🍎 Установка macOS (Hackintosh/OpenCore)</b>

1️⃣ Создайте флешку через GibMacOS.  
2️⃣ BIOS: AHCI=Enabled, XHCI Hand‑Off=Enabled, Secure Boot=Disabled, VT-d=Disabled.  
3️⃣ Загрузитесь → Install macOS.  
4️⃣ Формат APFS/GUID.  
5️⃣ Установите OC на SSD, скопируйте EFI.  
6️⃣ Kexts: Lilu, VirtualSMC, WhateverGreen, AppleALC.  
7️⃣ Настройте config.plist.  
8️⃣ Перезагрузитесь без флешки.
""".strip()

# ─────────────────────────────────────────────────────────────
# 2 ▸ Прогресс и утилиты
# ─────────────────────────────────────────────────────────────
TOTAL_STEPS = 8

def get_progress_text(p, total=TOTAL_STEPS):
    p = max(0, min(p, total))
    pct = round(p * 100 / total)
    bar = '🟢' * p + '⚪' * (total - p)
    return f"Прогресс: [{bar}] {pct}%"

def increment_progress(cid):
    d = get_user_data(cid)
    d["progress"] = max(0, min(d.get("progress", 0) + 1, TOTAL_STEPS))
    set_user_data(cid, d)

def decrement_progress(cid):
    d = get_user_data(cid)
    d["progress"] = max(0, min(d.get("progress", 0) - 1, TOTAL_STEPS))
    set_user_data(cid, d)

def current_progress_text(cid):
    return get_progress_text(get_user_data(cid).get("progress", 0))

async def send_stage_message(u, txt, header="", reply_markup=None):
    await u.effective_message.reply_text(
        (f"<b>{header}</b>\n" if header else "") + txt,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# ─────────────────────────────────────────────────────────────
# 3 ▸ Обработчики
# ─────────────────────────────────────────────────────────────
async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    cid = u.effective_chat.id
    set_user_data(cid, {"progress": 0})
    await send_stage_message(
        u,
        "🌟 <b>Ассистент сборки ПК</b>\n\nВыберите режим:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Я готов", callback_data="ready")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")],
        ])
    )

async def assistant_pc(u: Update, c: ContextTypes.DEFAULT_TYPE):
    # вызывается из main.py
    q = u.callback_query; await q.answer()
    await send_stage_message(
        u,
        "Проверьте наличие компонентов и инструментов:\n"
        "- Материнская плата, процессор, охлаждение\n"
        "- ОЗУ, SSD/M.2/HDD\n"
        "- Блок питания, корпус, видеокарта\n"
        "- Отвёртки, пинцет, стяжки, термопаста",
        header="Режим ассистента сборки",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Я готов", callback_data="ready")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")],
        ])
    )

async def handle_preparation_choice(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    if q.data == "ready":
        await q.edit_message_text(PREPARATION_FULL, parse_mode="HTML")
        increment_progress(q.message.chat_id)
        await send_stage_message(
            u,
            f"{current_progress_text(q.message.chat_id)}\n\nНажмите «Дальше».",
            header="🛠️ Подготовка завершена",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Назад⏪", callback_data="back_to_start"),
                    InlineKeyboardButton("Дальше⏩", callback_data="next_step")
                ],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
            ])
        )
    else:
        await q.edit_message_text("Подготовьтесь и запустите сборку позже.")

async def back_to_start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    decrement_progress(u.effective_chat.id)
    await start(u, c)

async def process_next_step(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(
        u,
        "Выберите платформу процессора:",
        header="💻 Выбор платформы",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Intel", callback_data="Intel"),
                InlineKeyboardButton("AMD", callback_data="AMD")
            ],
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_start"),
                InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")
            ]
        ])
    )

async def back_to_preparation(u: Update, c: ContextTypes.DEFAULT_TYPE):
    decrement_progress(u.effective_chat.id)
    await assistant_pc(u, c)

async def process_platform_choice(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    d = get_user_data(q.message.chat_id)
    d.update(platform=q.data, step_index=0)
    set_user_data(q.message.chat_id, d)
    await show_step(u, c)

async def show_step(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; d = get_user_data(q.message.chat_id)
    lst = steps[d["platform"]]["instructions"]
    idx = d["step_index"]
    if idx < len(lst):
        await send_stage_message(u, lst[idx], header="⚙️ Установка процессора")
        d["step_index"] += 1; set_user_data(q.message.chat_id, d)
        increment_progress(q.message.chat_id)
        await send_stage_message(
            u,
            f"{current_progress_text(q.message.chat_id)}\n\nНажмите «Дальше».",
            header="⚙️ Установка процессора",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Назад⏪", callback_data="back_to_platform"),
                    InlineKeyboardButton("Дальше⏩", callback_data="next_step_cooling")
                ],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
            ])
        )

async def back_to_platform(u: Update, c: ContextTypes.DEFAULT_TYPE):
    decrement_progress(u.effective_chat.id)
    await process_next_step(u, c)

async def handle_cooling_choice(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(
        u,
        "Тип охлаждения:",
        header="❄️ Система охлаждения",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Воздушное", callback_data="air"),
                InlineKeyboardButton("Жидкостное", callback_data="water")
            ],
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_platform"),
                InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")
            ]
        ])
    )

async def handle_cooling_selection(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    info = get_user_data(q.message.chat_id)
    await send_stage_message(u, cooling_instructions[info["platform"]][q.data], header="❄️ Система охлаждения")
    increment_progress(q.message.chat_id)
    await send_stage_message(
        u,
        f"{current_progress_text(q.message.chat_id)}\n\nНажмите «Дальше».",
        header="❄️ Система охлаждения",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_cooling"),
                InlineKeyboardButton("Дальше⏩", callback_data="next_step_ram")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def back_to_cooling(u: Update, c: ContextTypes.DEFAULT_TYPE):
    decrement_progress(u.effective_chat.id)
    await handle_cooling_choice(u, c)

async def handle_ram_choice(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(
        u,
        "Сколько планок ОЗУ устанавливаете?",
        header="💾 Установка ОЗУ",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("1", callback_data="1"),
                InlineKeyboardButton("2", callback_data="2"),
                InlineKeyboardButton("4", callback_data="4")
            ],
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_cooling"),
                InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")
            ]
        ])
    )

async def handle_ram_choice_selection(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await q.edit_message_text(ram_instructions[q.data], parse_mode="HTML")
    increment_progress(q.message.chat_id)
    await send_stage_message(
        u,
        f"{current_progress_text(q.message.chat_id)}\n\nНажмите «Дальше».",
        header="💾 Установка ОЗУ",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_ram"),
                InlineKeyboardButton("Дальше⏩", callback_data="next_step_m2")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def back_to_ram(u: Update, c: ContextTypes.DEFAULT_TYPE):
    decrement_progress(u.effective_chat.id)
    await handle_ram_choice(u, c)

async def handle_m2_choice(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(u, M2_DETAILED, header="🗜️ M.2 SSD")
    increment_progress(q.message.chat_id)
    await send_stage_message(
        u,
        f"{current_progress_text(q.message.chat_id)}\n\nНажмите «Дальше».",
        header="🗜️ M.2 SSD",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_ram"),
                InlineKeyboardButton("Дальше⏩", callback_data="next_step_fans")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def back_to_m2(u: Update, c: ContextTypes.DEFAULT_TYPE):
    decrement_progress(u.effective_chat.id)
    await handle_m2_choice(u, c)

async def handle_fan_choice(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(
        u,
        "Тип корпуса:",
        header="🌀 Установка вентиляторов",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Аквариумный", callback_data="aquarium")],
            [InlineKeyboardButton("Классический (БП внизу)", callback_data="classic_bottom")],
            [InlineKeyboardButton("Классический (БП сверху)", callback_data="classic_top")],
            [InlineKeyboardButton("Уже установлены", callback_data="already_installed")],
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_m2"),
                InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")
            ]
        ])
    )

async def handle_fan_instructions(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await q.edit_message_text(fan_instructions[q.data], parse_mode="HTML")
    increment_progress(q.message.chat_id)
    await send_stage_message(
        u,
        f"{current_progress_text(q.message.chat_id)}\n\nНажмите «Дальше».",
        header="🌀 Установка вентиляторов",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_fans"),
                InlineKeyboardButton("Дальше⏩", callback_data="next_step_power_supply")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def back_to_fans(u: Update, c: ContextTypes.DEFAULT_TYPE):
    decrement_progress(u.effective_chat.id)
    await handle_fan_choice(u, c)

async def handle_power_supply_choice(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(u, power_supply_instructions, header="🔌 Блок питания")
    increment_progress(q.message.chat_id)
    await send_stage_message(
        u,
        f"{current_progress_text(q.message.chat_id)}\n\nНажмите «Дальше».",
        header="🔌 Блок питания",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_fans"),
                InlineKeyboardButton("Дальше⏩", callback_data="next_step_gpu_check")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def back_to_power(u: Update, c: ContextTypes.DEFAULT_TYPE):
    decrement_progress(u.effective_chat.id)
    await handle_power_supply_choice(u, c)

async def ask_gpu_presence(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(
        u,
        "Есть дискретная видеокарта?",
        header="🎮 Видеокарта",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Да", callback_data="gpu_yes"),
                InlineKeyboardButton("Нет", callback_data="gpu_no")
            ],
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_power"),
                InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")
            ]
        ])
    )

async def handle_gpu_yes(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(u, gpu_instructions, header="🎮 Установка видеокарты")
    increment_progress(q.message.chat_id)
    await send_stage_message(
        u,
        f"{current_progress_text(q.message.chat_id)}\n\nНажмите «Дальше».",
        header="🎮 Установка видеокарты",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_gpu"),
                InlineKeyboardButton("Дальше⏩", callback_data="next_step_wires")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def handle_gpu_no(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    increment_progress(q.message.chat_id)
    await send_stage_message(
        u,
        f"{current_progress_text(q.message.chat_id)}\n\nНажмите «Дальше».",
        header="🎮 Видеокарта",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_gpu"),
                InlineKeyboardButton("Дальше⏩", callback_data="next_step_wires")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def back_to_gpu(u: Update, c: ContextTypes.DEFAULT_TYPE):
    decrement_progress(u.effective_chat.id)
    await ask_gpu_presence(u, c)

async def handle_wires_instruction(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(u, wires_instructions, header="🔗 Подключение кабелей")
    img = Path(__file__).with_name("IMG_5330.jpg")
    if img.exists():
        with open(img, "rb") as ph:
            await c.bot.send_photo(q.message.chat_id, ph, caption="Схема PANEL1")
    increment_progress(q.message.chat_id)
    await send_stage_message(
        u,
        f"{current_progress_text(q.message.chat_id)}\n\nНажмите «Дальше» для установки ОС.",
        header="🔗 Подключение кабелей",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_wires"),
                InlineKeyboardButton("Дальше⏩", callback_data="next_step_os")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def back_to_wires(u: Update, c: ContextTypes.DEFAULT_TYPE):
    decrement_progress(u.effective_chat.id)
    await handle_wires_instruction(u, c)

async def ask_os_question(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(
        u,
        "Нужна помощь с установкой ОС?",
        header="💿 Установка ОС",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Да", callback_data="os_yes"),
                InlineKeyboardButton("Нет", callback_data="os_no")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def handle_os_help_yes(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(
        u,
        "Выберите ОС:",
        header="💿 Установка ОС",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Windows", callback_data="os_windows"),
                InlineKeyboardButton("Linux", callback_data="os_linux"),
                InlineKeyboardButton("macOS", callback_data="os_mac")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def handle_os_help_no(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(
        u,
        "Переходим к завершению сборки.",
        header="💿 Установка ОС",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="back_to_wires"),
                InlineKeyboardButton("Завершить", callback_data="finish_assembly")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def handle_os_windows(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(u, WIN_TEXT, header="🖥️ Установка Windows")
    await send_stage_message(
        u,
        "Нажмите «Завершить», чтобы закончить.",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="os_yes"),
                InlineKeyboardButton("Завершить", callback_data="finish_assembly")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def handle_os_linux(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(u, LINUX_TEXT, header="🐧 Установка Ubuntu")
    await send_stage_message(
        u,
        "Нажмите «Завершить», чтобы закончить.",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="os_yes"),
                InlineKeyboardButton("Завершить", callback_data="finish_assembly")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def handle_os_mac(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(u, MAC_TEXT, header="🍎 Установка macOS")
    await send_stage_message(
        u,
        "Нажмите «Завершить», чтобы закончить.",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Назад⏪", callback_data="os_yes"),
                InlineKeyboardButton("Завершить", callback_data="finish_assembly")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def finish_assembly(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    await send_stage_message(
        u,
        "🎉 <b>Сборка завершена!</b> Приятного пользования новым ПК!",
        header="🎉 Готово",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Главное меню", callback_data="go_home")]
        ])
    )

async def go_home(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query
    if q:
        await q.answer()
    from main import start_main_menu
    await start_main_menu(u, c)

# ─────────────────────────────────────────────────────────────
# 4 ▸ Регистрация обработчиков
# ─────────────────────────────────────────────────────────────
def setup_handlers(app):
    # Обработчики навигации внутри ассистента
    app.add_handler(CallbackQueryHandler(handle_preparation_choice, pattern="^(ready|not_ready)$"))
    app.add_handler(CallbackQueryHandler(back_to_start,             pattern="^back_to_start$"))
    app.add_handler(CallbackQueryHandler(process_next_step,         pattern="^next_step$"))
    app.add_handler(CallbackQueryHandler(back_to_preparation,       pattern="^back_to_preparation$"))
    app.add_handler(CallbackQueryHandler(process_platform_choice,   pattern="^(Intel|AMD)$"))
    app.add_handler(CallbackQueryHandler(back_to_platform,          pattern="^back_to_platform$"))
    app.add_handler(CallbackQueryHandler(handle_cooling_choice,     pattern="^next_step_cooling$"))
    app.add_handler(CallbackQueryHandler(handle_cooling_selection,  pattern="^(air|water)$"))
    app.add_handler(CallbackQueryHandler(back_to_cooling,           pattern="^back_to_cooling$"))
    app.add_handler(CallbackQueryHandler(handle_ram_choice,         pattern="^next_step_ram$"))
    app.add_handler(CallbackQueryHandler(handle_ram_choice_selection, pattern="^(1|2|4)$"))
    app.add_handler(CallbackQueryHandler(back_to_ram,               pattern="^back_to_ram$"))
    app.add_handler(CallbackQueryHandler(handle_m2_choice,          pattern="^next_step_m2$"))
    app.add_handler(CallbackQueryHandler(back_to_m2,                pattern="^back_to_m2$"))
    app.add_handler(CallbackQueryHandler(handle_fan_choice,         pattern="^next_step_fans$"))
    app.add_handler(CallbackQueryHandler(handle_fan_instructions,   pattern="^(aquarium|classic_bottom|classic_top|already_installed)$"))
    app.add_handler(CallbackQueryHandler(back_to_fans,              pattern="^back_to_fans$"))
    app.add_handler(CallbackQueryHandler(handle_power_supply_choice,pattern="^next_step_power_supply$"))
    app.add_handler(CallbackQueryHandler(back_to_power,             pattern="^back_to_power$"))
    app.add_handler(CallbackQueryHandler(ask_gpu_presence,          pattern="^next_step_gpu_check$"))
    app.add_handler(CallbackQueryHandler(handle_gpu_yes,            pattern="^gpu_yes$"))
    app.add_handler(CallbackQueryHandler(handle_gpu_no,             pattern="^gpu_no$"))
    app.add_handler(CallbackQueryHandler(back_to_gpu,               pattern="^back_to_gpu$"))
    app.add_handler(CallbackQueryHandler(handle_wires_instruction,  pattern="^next_step_wires$"))
    app.add_handler(CallbackQueryHandler(back_to_wires,             pattern="^back_to_wires$"))
    app.add_handler(CallbackQueryHandler(ask_os_question,           pattern="^next_step_os$"))
    app.add_handler(CallbackQueryHandler(handle_os_help_yes,        pattern="^os_yes$"))
    app.add_handler(CallbackQueryHandler(handle_os_help_no,         pattern="^os_no$"))
    app.add_handler(CallbackQueryHandler(handle_os_windows,         pattern="^os_windows$"))
    app.add_handler(CallbackQueryHandler(handle_os_linux,           pattern="^os_linux$"))
    app.add_handler(CallbackQueryHandler(handle_os_mac,             pattern="^os_mac$"))
    app.add_handler(CallbackQueryHandler(finish_assembly,           pattern="^finish_assembly$"))
    app.add_handler(CallbackQueryHandler(go_home,                   pattern="^go_home$"))