from typing import Final
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater

## API токен бота та назва
TOKEN: Final = ''
BOT_USERNAME = '@banderaounbot'

## Стартове повідомлення
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 Початок роботи")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привіт! Щоб почати, натисни кнопку нижче 👇",
        reply_markup=reply_markup
    )

## Коли користувач натискає "Початок роботи"
async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🚀 Початок роботи":
        await show_main_menu(update, context)

## Головне меню
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keys_to_clear = [   ## Вирішення проблеми з прапорцями
        "awaiting_period_input",
        "awaiting_expense_period_input",
        "awaiting_comment_input",
        "awaiting_expense_sum",
        "awaiting_profit_sum",
        "awaiting_date_input",
        "awaiting_source_selection",
        "awaiting_category_input",
        "awaiting_subcategory_input"
    ]
    for key in keys_to_clear:
        context.user_data.pop(key, None)
    keyboard = [
        [KeyboardButton("➕ Додати прибуток"), KeyboardButton("📈 Перегляд прибутку"), KeyboardButton("📊 Статистика")],
        [KeyboardButton("➕ Додати витрату"), KeyboardButton("📉 Перегляд витрат"), KeyboardButton("🔢 Ліміти")],
        [KeyboardButton("⚙️ Управління акаунтом")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("✅ Головне меню:", reply_markup=reply_markup)

## Меню після додавання прибутку
async def show_after_adding_profit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["previous_menu"] = "after_adding_profit"
    keyboard = [
        [KeyboardButton("✅ Підтвердити")],
        [KeyboardButton("✏️ Змінити суму")],
        [KeyboardButton("💬 Коментар")],
        [KeyboardButton("📅 Дата")],
        [KeyboardButton("📌 Джерело")],
        [KeyboardButton("↩️ Головне меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("✔️ Що бажаєте зробити далі?", reply_markup=reply_markup)

## Функція для виводу джерел (в Додаванні прибутку)
async def show_sources_menu(update: Update):
    keyboard = [
        [KeyboardButton("Джерело 1"), KeyboardButton("Джерело 2")],
        [KeyboardButton("Джерело 3"), KeyboardButton("Джерело 4")],
        [KeyboardButton("Джерело 5"), KeyboardButton("Джерело 6")],
        [KeyboardButton("Джерело 7"), KeyboardButton("Не вказувати")],
        [KeyboardButton("↩️ Повернутися")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Оберіть джерело прибутку:",
        reply_markup=reply_markup
    )

## Вивід меню після натискання "Дата" (Додавання прибутку)
async def show_date_menu(update: Update):
    keyboard = [
        [KeyboardButton("Сьогодні"), KeyboardButton("Вчора")],
        [KeyboardButton("↩️ Повернутися")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🗓️ Оберіть дату зі списку або введіть самостійно у форматі dd/mm/yyyy",
        reply_markup=reply_markup
    )

## Вивід меню після натискання "Коментар" (Додавання прибутку)
async def show_comment_menu(update: Update):
    keyboard = [[KeyboardButton("↩️ Повернутися")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "💬 Введіть коментар:",
        reply_markup=reply_markup
    )

## Меню після додавання витрати (Додавання витрати)
async def show_after_adding_expense_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["previous_menu"] = "after_adding_expense"
    keyboard = [
        [KeyboardButton("✅ Підтвердити")],
        [KeyboardButton("✏️ Змінити суму")],
        [KeyboardButton("💬 Коментар")],
        [KeyboardButton("📅 Дата")],
        [KeyboardButton("📌 Категорія")]
    ]

    # Якщо обрана категорія, додаємо кнопку підкатегорії
    if context.user_data.get("selected_category"):
        keyboard.append([KeyboardButton("📂 Підкатегорія")])

    keyboard.append([KeyboardButton("↩️ Головне меню")])

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("✔️ Що бажаєте зробити далі?", reply_markup=reply_markup)

## Меню після вибору "Категорія" (Додавання витрати)
async def show_categories_menu(update: Update):
    keyboard = [
        [KeyboardButton("Категорія 1"), KeyboardButton("Категорія 2")],
        [KeyboardButton("Категорія 3"), KeyboardButton("Категорія 4")],
        [KeyboardButton("Категорія 5"), KeyboardButton("Категорія 6")],
        [KeyboardButton("Категорія 7"), KeyboardButton("Не вказувати")],
        [KeyboardButton("↩️ Повернутися")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🗂️ Оберіть категорію витрати:",
        reply_markup=reply_markup
    )

## Меню після вибору "Підкатегорія" (Додавання витрати)
async def show_subcategories_menu(update: Update):
    keyboard = [
        [KeyboardButton("Підкатегорія 1"), KeyboardButton("Підкатегорія 2")],
        [KeyboardButton("Підкатегорія 3"), KeyboardButton("Підкатегорія 4")],
        [KeyboardButton("Підкатегорія 5"), KeyboardButton("Підкатегорія 6")],
        [KeyboardButton("Підкатегорія 7"), KeyboardButton("Не вказувати")],
        [KeyboardButton("↩️ Повернутися")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "📂 Оберіть підкатегорію:",
        reply_markup=reply_markup
    )

async def show_expense_subcategories_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔴 Тут буде SQL-запит, щоб отримати підкатегорії для вибраної категорії
    # Наприклад: підтягуємо список з БД: subcategories = get_subcategories(category_id)

    # Заглушка-кнопки для тесту
    keyboard = [
        [KeyboardButton("Підкатегорія 1"), KeyboardButton("Підкатегорія 2")],
        [KeyboardButton("Підкатегорія 3"), KeyboardButton("Підкатегорія 4")],
        [KeyboardButton("Підкатегорія 5"), KeyboardButton("Підкатегорія 6")],
        [KeyboardButton("Підкатегорія 7"), KeyboardButton("Не вказано")],
        [KeyboardButton("↩️ Повернутися"), KeyboardButton("↩️ Головне меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "📂 Оберіть підкатегорію витрати:",
        reply_markup=reply_markup
    )
    context.user_data["previous_menu"] = "choose_expense_subcategory"

## Вивід меню після натискання "Дата" (додавання витрати)
async def show_expense_date_menu(update: Update):
    keyboard = [
        [KeyboardButton("Сьогодні"), KeyboardButton("Вчора")],
        [KeyboardButton("↩️ Повернутися")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🗓️ Оберіть дату зі списку або введіть самостійно у форматі dd/mm/yyyy",
        reply_markup=reply_markup
    )

## Меню після вибору "📈 Перегляд прибутку"
async def show_profit_period_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("За весь час")],
        [KeyboardButton("За рік")],
        [KeyboardButton("За місяць")],
        [KeyboardButton("За тиждень")],
        [KeyboardButton("За сьогодні")],
        [KeyboardButton("↩️ Головне меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🗓️ Оберіть період у меню або введіть його самостійно у форматі dd/mm/yyyy:dd/mm/yyyy",
        reply_markup=reply_markup
    )

# Коли користувач натискає "➕ Додати прибуток"
async def add_profit_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "➕ Додати прибуток":
        context.user_data["awaiting_profit_sum"] = True  # Чекаємо суму
        keyboard = [[KeyboardButton("↩️ Головне меню")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Щоб додати прибуток, введіть суму:",
            reply_markup=reply_markup
        )

## Коли користувач натискає "➕ Додати витрату"
async def add_expense_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "➕ Додати витрату":
        context.user_data["awaiting_expense_sum"] = True  # Чекаємо введення суми витрати
        keyboard = [[KeyboardButton("↩️ Головне меню")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "💸 Введіть суму витрат:",
            reply_markup=reply_markup
        )

async def show_statistics_menu(update: Update):
    keyboard = [
        [KeyboardButton("📈 Статистика прибутку")],
        [KeyboardButton("📉 Статистика витрат")],
        [KeyboardButton("↩️ Головне меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "📊 Оберіть тип статистики:",
        reply_markup=reply_markup
    )

async def show_graphs_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, all_sources: bool):
    # Меню графіків після вибору варіанту
    context.user_data["previous_menu"] = "graphs_menu"
    if all_sources:
        keyboard = [
            [KeyboardButton("Pie Chart")],
            [KeyboardButton("Bars")],
            [KeyboardButton("Scatter Plot")],
            [KeyboardButton("↩️ Повернутися")],
            [KeyboardButton("↩️ Головне меню")]
        ]
    else:
        keyboard = [
            [KeyboardButton("Bars")],
            [KeyboardButton("Scatter Plot")],
            [KeyboardButton("↩️ Повернутися")],
            [KeyboardButton("↩️ Головне меню")]
        ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "📊 Оберіть графік для відображення:",
        reply_markup=reply_markup
    )

async def show_limits_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Мої ліміти")],
        [KeyboardButton("Новий ліміт")],
        [KeyboardButton("↩️ Головне меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🔒 Меню лімітів:", reply_markup=reply_markup)
    context.user_data["previous_menu"] = "limits_list"


async def show_user_limits_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔴 ПІД SQL: Отримати список лімітів користувача
    # limits = get_user_limits(user_id)
    limits = ["Ліміт 1", "Ліміт 2", "Ліміт 3"]  # Заглушка

    keyboard = [[KeyboardButton(limit)] for limit in limits]
    keyboard.append([KeyboardButton("↩️ Повернутися"), KeyboardButton("↩️ Головне меню")])

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "📝 Оберіть ліміт для перегляду:",
        reply_markup=reply_markup
    )
    context.user_data["previous_menu"] = "limits_menu"

async def show_limit_details(update: Update, context: ContextTypes.DEFAULT_TYPE, limit_name: str):
    # 🔴 ПІД SQL (запит №15): Отримати деталі ліміту за назвою limit_name
    # details = get_limit_details(limit_name)
    details = "Сума: 1000 грн\nКатегорія: Категорія 1\nПідкатегорія: Підкатегорія 2\nПеріод: Місяць"  # Заглушка

    await update.message.reply_text(
        f"ℹ️ Інформація про ліміт:\n\n{details}"
    )

    keyboard = [
        [KeyboardButton("❌ Видалити")],
        [KeyboardButton("↩️ Повернутися")],
        [KeyboardButton("↩️ Головне меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    context.user_data["previous_menu"] = "limit_details"
    await update.message.reply_text(
        "🛠️ Що бажаєте зробити з лімітом?",
        reply_markup=reply_markup
    )

async def handle_new_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Підготовка під SQL-запит для перевірки кількості лімітів
    # 🔴 SQL-запит №13 (поки лишаємо місце)
    user_id = update.effective_user.id
    # кількість_лімітів = db.get_user_limits_count(user_id) # заглушка

    # Заглушка для тесту (наприклад)
    limits_count = 5  # заміни це на реальний запит

    if limits_count >= 8:
        await update.message.reply_text(
            "❗ Ви вже маєте 8 лімітів. Спочатку видаліть один з них, щоб додати новий."
        )
        await show_user_limits_menu(update, context)
        context.user_data["previous_menu"] = "limits_menu"
        return

    # Якщо все гаразд – запитуємо суму
    await update.message.reply_text(
        "💬 Впишіть суму для встановлення загального ліміту на всі витрати або спочатку оберіть конкретну категорію",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("За категорією")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ],
            resize_keyboard=True
        )
    )
    context.user_data["awaiting_limit_sum"] = True
    context.user_data["previous_menu"] = "new_limit"

async def show_user_limits_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔴 Тут буде SQL-запит №13 для отримання лімітів
    # limits = db.get_user_limits(user_id)  # заглушка
    limits = ["Ліміт 1", "Ліміт 2", "Ліміт 3"]  # заглушка

    keyboard = [[KeyboardButton(limit)] for limit in limits]
    keyboard.append([KeyboardButton("↩️ Повернутися")])
    keyboard.append([KeyboardButton("↩️ Головне меню")])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "📋 Ваші ліміти:",
        reply_markup=reply_markup
    )
    context.user_data["previous_menu"] = "limits_menu"


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Якщо користувач у режимі введення суми
    if context.user_data.get("awaiting_profit_sum"):
        if text == "↩️ Головне меню":
            context.user_data["awaiting_profit_sum"] = False
            await show_main_menu(update, context)
            return
        try:
            profit = float(text)
            await update.message.reply_text(f"✅ Додано прибуток: {profit} грн")
            context.user_data["profit_sum"] = profit ## зберігання даних для виведення та зберігання в БД
            context.user_data["awaiting_profit_sum"] = False
            await show_after_adding_profit_menu(update, context)
        except ValueError:
            await update.message.reply_text("❌ Будь ласка, введіть коректне число!")
        return

        # Якщо користувач натиснув "↩️ Головне меню" у будь-якому місці
    if text == "↩️ Головне меню":
        await show_main_menu(update, context)
        return

    if text == "✅ Підтвердити":
        if context.user_data.get("awaiting_profit_sum") or context.user_data.get("profit_sum"):
            # Підтвердження для прибутку
            profit_sum = context.user_data.get("profit_sum", "Не вказано")
            source = context.user_data.get("selected_source", "Не вказано")
            date = context.user_data.get("selected_date", "Не вказано")
            comment = context.user_data.get("comment", "Не вказано")
            # ТУТ: SQL для прибутку (якщо потрібно)
            result_message = (
                f"✅ Прибуток успішно додано!\n\n"
                f"💰 Сума: {profit_sum}\n"
                f"📌 Джерело: {source}\n"
                f"🗓️ Дата: {date}\n"
                f"💬 Коментар: {comment}"
            )
        elif context.user_data.get("awaiting_expense_sum") or context.user_data.get("expense_sum"):
            # Підтвердження для витрати
            expense_sum = context.user_data.get("expense_sum", "Не вказано")
            category = context.user_data.get("selected_category", "Не вказано")
            subcategory = context.user_data.get("selected_subcategory", "Не вказано")
            date = context.user_data.get("selected_date", "Не вказано")
            comment = context.user_data.get("comment", "Не вказано")
            # ТУТ: SQL для витрати (якщо потрібно)
            result_message = (
                f"✅ Витрату успішно додано!\n\n"
                f"💸 Сума: {expense_sum}\n"
                f"🗂️ Категорія: {category}\n"
                f"📂 Підкатегорія: {subcategory}\n"
                f"🗓️ Дата: {date}\n"
                f"💬 Коментар: {comment}"
            )
        else:
            await update.message.reply_text("❌ Немає даних для підтвердження.")
            return

        await update.message.reply_text(result_message)
        context.user_data.clear()
        await show_main_menu(update, context)
        return

    if text == "✏️ Змінити суму":
        context.user_data["awaiting_profit_sum"] = True
        await update.message.reply_text("Введіть нову суму:")
        return

    if text == "💬 Коментар":
        context.user_data["awaiting_comment_input"] = True
        # Важливо: вказуємо, для чого цей коментар
        context.user_data["current_mode"] = "profit" if context.user_data.get("awaiting_profit_sum") else "expense"
        await show_comment_menu(update)
        return

    if text == "↩️ Повернутися":
        previous_menu = context.user_data.get("previous_menu", "main_menu")

        if previous_menu == "after_adding_expense":
            await show_after_adding_expense_menu(update, context)
        elif previous_menu == "after_adding_profit":
            await show_after_adding_profit_menu(update, context)
        elif previous_menu == "statistics":
            await show_statistics_menu(update)
            context.user_data["previous_menu"] = "main_menu"
        elif previous_menu == "graphs_menu":
            await show_graphs_menu(update, context, all_sources=context.user_data.get("graph_all_sources", False))
        elif previous_menu == "profit_statistics_period":
            # Повертаємось до вибору періоду статистики прибутку
            keyboard = [
                [KeyboardButton("За весь період"), KeyboardButton("За рік")],
                [KeyboardButton("За місяць"), KeyboardButton("За тиждень")],
                [KeyboardButton("За сьогодні"), KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(
                "🗓️ Оберіть період для перегляду статистики прибутку:",
                reply_markup=reply_markup
            )
            context.user_data["awaiting_period_input"] = True

        elif previous_menu == "expense_statistics_period":
            # Повертаємось до вибору періоду витрат
            keyboard = [
                [KeyboardButton("за весь період"), KeyboardButton("за рік")],
                [KeyboardButton("за місяць"), KeyboardButton("за тиждень")],
                [KeyboardButton("за сьогодні"), KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(
                "🗓️ Оберіть період або введіть його самостійно у форматі dd/mm/yyyy:dd/mm/yyyy",
                reply_markup=reply_markup
            )
            context.user_data["awaiting_expense_period_input"] = True

        elif previous_menu == "graphs_menu_expense":
            # Повернення до меню з вибором "за усіма категоріями" чи "обрати категорію"
            keyboard = [
                [KeyboardButton("За усіма категоріями")],
                [KeyboardButton("Обрати категорію")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "expense_statistics_period"

        elif previous_menu == "choose_expense_category":
            # Повертаємося до меню "за усіма категоріями / обрати категорію"
            keyboard = [
                [KeyboardButton("За усіма категоріями")],
                [KeyboardButton("Обрати категорію")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "expense_statistics_period"
            return

        elif previous_menu == "graphs_menu_choose_category":
            # Повертаємося до меню вибору категорії
            categories = ["Категорія 1", "Категорія 2", "Категорія 3", "Категорія 4", "Категорія 5", "Категорія 6",
                          "Категорія 7", "Не вказувати"]
            keyboard = [[KeyboardButton(cat)] for cat in categories]
            keyboard.append([KeyboardButton("↩️ Повернутися"), KeyboardButton("↩️ Головне меню")])
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🗂️ Оберіть категорію:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "choose_expense_category"
            return

        elif previous_menu == "user_limits_menu":
            keyboard = [
                [KeyboardButton("Мої ліміти")],
                [KeyboardButton("Новий ліміт")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🔙 Меню лімітів:", reply_markup=reply_markup)

        elif previous_menu == "limits_menu":
            await show_limits_menu(update, context)
            context.user_data["previous_menu"] = "main_menu"
            return

        elif previous_menu == "limit_details":
            await show_user_limits_menu(update, context)
            context.user_data["previous_menu"] = "limits_menu"
            return

        else:
            await show_main_menu(update, context)
        return

    ## дата
    if text == "📅 Дата":
        context.user_data["awaiting_date_input"] = True
        # Важливо: вказуємо, де ми – у прибутку чи витраті
        context.user_data["current_mode"] = "profit" if context.user_data.get("awaiting_profit_sum") else "expense"
        await show_date_menu(update)
        return

    if text == "📌 Джерело":
        context.user_data["awaiting_source_selection"] = "profit"  # Мітка: вибір джерела для прибутку
        await show_sources_menu(update)
        return

    if text in ["Джерело 1", "Джерело 2", "Джерело 3", "Джерело 4", "Джерело 5", "Джерело 6", "Джерело 7",
                "Не вказувати"]:
        if context.user_data.get("awaiting_source_selection") == "profit":
            await update.message.reply_text(f"✅ Джерело обрано: {text}")
            context.user_data["selected_source"] = text
        ## Тут треба реалізувати SQL-запит 1

        ##
            context.user_data["selected_source"] = text ## зберігання даних для виведення та зберігання в БД
            await show_after_adding_profit_menu(update, context)
            context.user_data.pop("awaiting_source_selection")  # Очищаємо мітку
            return


    ## Введення та валідація дати для прибутку та витрат
    if context.user_data.get("awaiting_date_input"):
        if text == "↩️ Повернутися":
            context.user_data["awaiting_date_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update, context)
            else:
                await show_after_adding_expense_menu(update, context)
            return

        if text == "Сьогодні":
            date = datetime.now().strftime("%d/%m/%Y")
            context.user_data["selected_date"] = date
            await update.message.reply_text(f"✅ Дата встановлена: {date}")
            context.user_data["awaiting_date_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update, context)
            else:
                await show_after_adding_expense_menu(update, context)
            return

        if text == "Вчора":
            date = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
            context.user_data["selected_date"] = date
            await update.message.reply_text(f"✅ Дата встановлена: {date}")
            context.user_data["awaiting_date_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update, context)
            else:
                await show_after_adding_expense_menu(update, context)
            return

        try:
            parsed_date = datetime.strptime(text, "%d/%m/%Y")
            context.user_data["selected_date"] = text
            await update.message.reply_text(f"✅ Дата встановлена: {text}")
            context.user_data["awaiting_date_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update, context)
            else:
                await show_after_adding_expense_menu(update, context)
        except ValueError:
            await update.message.reply_text(
                "❌ Неправильний формат дати. Введіть у форматі dd/mm/yyyy, наприклад: 05/06/2025"
            )
        return

    ## Додавання та валідація коментаря
    if context.user_data.get("awaiting_comment_input"):
        if text == "↩️ Повернутися":
            context.user_data["awaiting_comment_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update, context)
            else:
                await show_after_adding_expense_menu(update, context)
            return

        # Валідація: довжина коментаря від 3 до 200
        if 3 <= len(text) <= 200:
            context.user_data["comment"] = text
            await update.message.reply_text("✅ Коментар додано!")
            context.user_data["awaiting_comment_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update, context)
            else:
                await show_after_adding_expense_menu(update, context)
        else:
            await update.message.reply_text(
                "❌ Коментар має бути від 3 до 200 символів. Спробуйте ще раз!"
            )
        return

    ## Обробка введення суми витрат (Додати витрату)
    if context.user_data.get("awaiting_expense_sum"):
        if text == "↩️ Головне меню":
            context.user_data["awaiting_expense_sum"] = False
            await show_main_menu(update, context)
            return

        # Валідація: число > 0 і, наприклад, < 100000
        try:
            expense = float(text)
            if expense <= 0 or expense > 100000:
                await update.message.reply_text("❌ Сума має бути > 0 і < 100000. Спробуйте ще раз!")
                return
            context.user_data["expense_sum"] = expense
            await update.message.reply_text(f"✅ Суму витрат додано: {expense} грн")
            context.user_data["awaiting_expense_sum"] = False
            await show_after_adding_expense_menu(update, context)
        except ValueError:
            await update.message.reply_text("❌ Будь ласка, введіть коректне число!")
        return

    if text == "📌 Категорія":
        context.user_data["awaiting_category_input"] = True
        await show_categories_menu(update)
        return

    ## Вибір категорії витрат
    if context.user_data.get("awaiting_category_input"):
        if text == "↩️ Повернутися":
            context.user_data["awaiting_category_input"] = False
            await show_after_adding_expense_menu(update, context)
            return
        if text in ["Категорія 1", "Категорія 2", "Категорія 3", "Категорія 4", "Категорія 5", "Категорія 6",
                    "Категорія 7", "Не вказувати"]:
            await update.message.reply_text(f"✅ Категорія обрана: {text}")
            context.user_data["selected_category"] = text
            ## Тут треба реалізувати SQL-запит 3

            ##
            context.user_data["awaiting_category_input"] = False
            await show_after_adding_expense_menu(update, context)
        else:
            await update.message.reply_text("❌ Будь ласка, виберіть категорію зі списку!")
        return

    if text == "📂 Підкатегорія":
        context.user_data["awaiting_subcategory_input"] = True
        await show_subcategories_menu(update)
        return

    ## меню для підкатегорій (додавання витрат)
    if context.user_data.get("awaiting_subcategory_input"):
        if text == "↩️ Повернутися":
            context.user_data["awaiting_subcategory_input"] = False
            await show_after_adding_expense_menu(update, context)
            return
        if text in ["Підкатегорія 1", "Підкатегорія 2", "Підкатегорія 3", "Підкатегорія 4", "Підкатегорія 5",
                    "Підкатегорія 6", "Підкатегорія 7", "Не вказувати"]:
            await update.message.reply_text(f"✅ Підкатегорія обрана: {text}")
            context.user_data["selected_subcategory"] = text
            ## Тут треба реалізувати SQL-запит 4

            ##
            context.user_data["awaiting_subcategory_input"] = False
            await show_after_adding_expense_menu(update, context)
        else:
            await update.message.reply_text("❌ Будь ласка, виберіть підкатегорію зі списку!")
        return

    if text == "📈 Перегляд прибутку":
        await show_profit_period_menu(update, context)
        return

    # Перегляд прибутку: кнопки періоду ## SQL-запит 7
    ## UPD: Треба додати функцію виведення по 10 елементів
    if context.user_data.get("awaiting_profit_period_input"):
        if text == "За весь час":
            await update.message.reply_text("✅ Ви обрали перегляд за весь час.")
            # ТУТ: SQL-запит №7 — всі записи
            context.user_data["awaiting_profit_period_input"] = False
            return

        if text == "За рік":
            start_date = (datetime.now() - timedelta(days=365)).strftime("%d/%m/%Y")
            end_date = datetime.now().strftime("%d/%m/%Y")
            await update.message.reply_text(f"✅ Період: {start_date} — {end_date}")
            # ТУТ: SQL-запит №7 — записи за рік
            context.user_data["awaiting_profit_period_input"] = False
            return

        if text == "За місяць":
            start_date = (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y")
            end_date = datetime.now().strftime("%d/%m/%Y")
            await update.message.reply_text(f"✅ Період: {start_date} — {end_date}")
            # ТУТ: SQL-запит №7 — записи за місяць
            context.user_data["awaiting_profit_period_input"] = False
            return

        if text == "За тиждень":
            start_date = (datetime.now() - timedelta(days=7)).strftime("%d/%m/%Y")
            end_date = datetime.now().strftime("%d/%m/%Y")
            await update.message.reply_text(f"✅ Період: {start_date} — {end_date}")
            # ТУТ: SQL-запит №7 — записи за тиждень
            context.user_data["awaiting_profit_period_input"] = False
            return

        if text == "За сьогодні":
            date = datetime.now().strftime("%d/%m/%Y")
            await update.message.reply_text(f"✅ Дата: {date}")
            # ТУТ: SQL-запит №7 — записи за сьогодні
            context.user_data["awaiting_profit_period_input"] = False
            return

    # Валідація введеного вручну періоду (якщо користувач вводить самостійно)
    if ":" in text and context.user_data.get("awaiting_profit_period_input"):
        try:
            start_str, end_str = text.split(":")
            start_date = datetime.strptime(start_str.strip(), "%d/%m/%Y")
            end_date = datetime.strptime(end_str.strip(), "%d/%m/%Y")
            if start_date > end_date:
                await update.message.reply_text("❌ Початкова дата не може бути пізнішою за кінцеву!")
                return

            #### Тут треба реалізувати SQL-запит №7
            await update.message.reply_text(f"✅ Період встановлено: {start_str} — {end_str}")
            context.user_data["awaiting_profit_period_input"] = False
            ####
        except ValueError:
            await update.message.reply_text(
                "❌ Неправильний формат! Введіть у форматі dd/mm/yyyy:dd/mm/yyyy"
            )
        return

    if text == "📊 Статистика":
        await show_statistics_menu(update)
        context.user_data["previous_menu"] = "main_menu"
        return

    # ➡️ Перехід до підрозділу №8 (Статистика прибутку)
    if text == "📈 Статистика прибутку":
        keyboard = [
            [KeyboardButton("За весь період"), KeyboardButton("За рік")],
            [KeyboardButton("За місяць"), KeyboardButton("За тиждень")],
            [KeyboardButton("За сьогодні"), KeyboardButton("↩️ Головне меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🗓️ Оберіть період або введіть його самостійно у форматі dd/mm/yyyy:dd/mm/yyyy",
            reply_markup=reply_markup
        )
        # Ставимо прапорець, що користувач зараз вводить період
        context.user_data["awaiting_period_input"] = True
        return

    # ➡️ Обробка вибору періоду у Статистиці прибутку
    if context.user_data.get("awaiting_period_input"):
        if text == "↩️ Головне меню":
            context.user_data["awaiting_period_input"] = False
            await show_main_menu(update, context)
            return

        # Обробка вибору "За рік", "За місяць", "За тиждень", "За сьогодні"
        now = datetime.now()
        if text == "За рік":
            start_date = (now - timedelta(days=365)).strftime("%d/%m/%Y")
            end_date = now.strftime("%d/%m/%Y")
            await update.message.reply_text(f"📈 Статистика прибутку за рік (з {start_date} по {end_date})")
            # 🔴 Місце для SQL-запиту (наприклад, SQL SELECT за цей період)
        elif text == "За місяць":
            start_date = (now - timedelta(days=30)).strftime("%d/%m/%Y")
            end_date = now.strftime("%d/%m/%Y")
            await update.message.reply_text(f"📈 Статистика прибутку за місяць (з {start_date} по {end_date})")
            # 🔴 Місце для SQL-запиту
        elif text == "За тиждень":
            start_date = (now - timedelta(days=7)).strftime("%d/%m/%Y")
            end_date = now.strftime("%d/%m/%Y")
            await update.message.reply_text(f"📈 Статистика прибутку за тиждень (з {start_date} по {end_date})")
            # 🔴 Місце для SQL-запиту
        elif text == "За сьогодні":
            date = now.strftime("%d/%m/%Y")
            await update.message.reply_text(f"📈 Статистика прибутку за сьогодні: {date}")
            # 🔴 Місце для SQL-запиту
        elif text == "За весь період":
            await update.message.reply_text("📈 Статистика прибутку за весь період")
            # 🔴 Місце для SQL-запиту (усі записи)
        elif ":" in text:  # введено власний період
            try:
                start_str, end_str = text.split(":")
                start_date = datetime.strptime(start_str.strip(), "%d/%m/%Y")
                end_date = datetime.strptime(end_str.strip(), "%d/%m/%Y")
                if start_date > end_date:
                    await update.message.reply_text("❌ Початкова дата не може бути пізнішою за кінцеву!")
                    return
                await update.message.reply_text(f"📈 Статистика прибутку за період: {start_str} — {end_str}")
                # 🔴 Місце для SQL-запиту
            except ValueError:
                await update.message.reply_text("❌ Неправильний формат! Введіть у форматі dd/mm/yyyy:dd/mm/yyyy")
                return
        else:
            await update.message.reply_text("❌ Будь ласка, оберіть варіант зі списку!")
            return

        # Після відображення статистики – показуємо наступне меню
        keyboard = [
            [KeyboardButton("За усіма джерелами")],
            [KeyboardButton("Обрати джерело")],
            [KeyboardButton("↩️ Повернутися")],
            [KeyboardButton("↩️ Головне меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)

        # Встановлюємо прапорець, щоб знати, куди повертатися
        context.user_data["previous_menu"] = "profit_statistics_period"
        context.user_data["awaiting_period_input"] = False
        return

    if text == "За усіма джерелами":
        context.user_data["graph_all_sources"] = True
        await show_graphs_menu(update, context, all_sources=True)
        context.user_data["previous_menu"] = "statistics"
        return

    # ➡️ Обробка вибору графіків (усі джерела)
    if context.user_data.get("previous_menu") == "graphs_menu" and context.user_data.get("graph_all_sources"):
        if text == "Pie Chart":
            # 🔴 Місце для генерації / SQL графіка "Pie Chart"
            await update.message.reply_text("✅ Ви обрали графік: Pie Chart")
            # ТУТ: Інтеграція побудови графіка
            await update.message.reply_text("📊 Графік Pie Chart готовий! (інтегрується пізніше)")
        elif text == "Bars":
            # 🔴 Місце для генерації / SQL графіка "Bars"
            await update.message.reply_text("✅ Ви обрали графік: Bars")
            # ТУТ: Інтеграція побудови графіка
            await update.message.reply_text("📊 Графік Bars готовий! (інтегрується пізніше)")
        elif text == "Scatter Plot":
            # 🔴 Місце для генерації / SQL графіка "Scatter Plot"
            await update.message.reply_text("✅ Ви обрали графік: Scatter Plot")
            # ТУТ: Інтеграція побудови графіка
            await update.message.reply_text("📊 Графік Scatter Plot готовий! (інтегрується пізніше)")
        elif text == "↩️ Повернутися":
            # Повертаємось до вибору "За усіма джерелами" / "Обрати джерело"
            keyboard = [
                [KeyboardButton("За усіма джерелами")],
                [KeyboardButton("Обрати джерело")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "profit_statistics_period"
            return
        elif text == "↩️ Головне меню":
            await show_main_menu(update, context)
            return
        else:
            await update.message.reply_text("❌ Будь ласка, оберіть варіант зі списку!")
            return

        # ✅ Після відображення графіка – виводимо підсумкову статистику (можеш замінити текст на результат SQL)
        await update.message.reply_text("📈 Підсумкова статистика: (сюди пізніше підключається SQL)")

        # ✅ Після цього повертаємо користувача у головне меню
        await show_main_menu(update, context)
        return

    # ➡️ Обробка кнопки "Обрати джерело"
    if text == "Обрати джерело":
        # Тут буде SQL-запит №1 (отримати джерела, наприклад 1-7)
        # Зараз заглушка - кнопки для джерел:
        keyboard = [
            [KeyboardButton("Джерело 1"), KeyboardButton("Джерело 2")],
            [KeyboardButton("Джерело 3"), KeyboardButton("Джерело 4")],
            [KeyboardButton("Джерело 5"), KeyboardButton("Джерело 6")],
            [KeyboardButton("Джерело 7"), KeyboardButton("Не вказано")],
            [KeyboardButton("↩️ Повернутися")],
            [KeyboardButton("↩️ Головне меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("🔎 Оберіть джерело:", reply_markup=reply_markup)
        context.user_data["previous_menu"] = "choose_source"
        return

    # ➡️ Обробка вибору конкретного джерела
    if context.user_data.get("previous_menu") == "choose_source":
        if text.startswith("Джерело") or text == "Не вказано":
            await update.message.reply_text(f"✅ Джерело обрано: {text}")
            # Тут буде SQL-запит №9 (записи по конкретному джерелу)
            # Заглушка — повідомлення
            await update.message.reply_text("📊 Дані за обраним джерелом отримано! (інтегрується пізніше)")

            # Показуємо кнопки для графіків (без Pie Chart)
            keyboard = [
                [KeyboardButton("Bars")],
                [KeyboardButton("Scatter Plot")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("📊 Оберіть графік для перегляду:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "graphs_menu_choose_source"
            return
        elif text == "↩️ Повернутися":
            # Повертаємось до вибору "За усіма джерелами" / "Обрати джерело"
            keyboard = [
                [KeyboardButton("За усіма джерелами")],
                [KeyboardButton("Обрати джерело")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "profit_statistics_period"
            return
        elif text == "↩️ Головне меню":
            await show_main_menu(update, context)
            return
        else:
            await update.message.reply_text("❌ Будь ласка, оберіть джерело зі списку!")
            return

    # ➡️ Обробка вибору графіка (для обраного джерела)
    if context.user_data.get("previous_menu") == "graphs_menu_choose_source":
        if text == "Bars":
            # 🔴 Місце для генерації / SQL-запиту "Bars" для конкретного джерела
            await update.message.reply_text("✅ Ви обрали графік: Bars")
            # ТУТ: інтеграція побудови графіка
            await update.message.reply_text("📊 Графік Bars готовий! (інтегрується пізніше)")
        elif text == "Scatter Plot":
            # 🔴 Місце для генерації / SQL-запиту "Scatter Plot" для конкретного джерела
            await update.message.reply_text("✅ Ви обрали графік: Scatter Plot")
            # ТУТ: інтеграція побудови графіка
            await update.message.reply_text("📊 Графік Scatter Plot готовий! (інтегрується пізніше)")
        elif text == "↩️ Повернутися":
            # Повертаємось до вибору джерела
            keyboard = [
                [KeyboardButton("Джерело 1"), KeyboardButton("Джерело 2")],
                [KeyboardButton("Джерело 3"), KeyboardButton("Джерело 4")],
                [KeyboardButton("Джерело 5"), KeyboardButton("Джерело 6")],
                [KeyboardButton("Джерело 7"), KeyboardButton("Не вказано")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🔎 Оберіть джерело:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "choose_source"
            return
        elif text == "↩️ Головне меню":
            await show_main_menu(update, context)
            return
        else:
            await update.message.reply_text("❌ Будь ласка, оберіть графік зі списку!")
            return

        # ✅ Після відображення графіка – виводимо підсумкову статистику
        await update.message.reply_text("📈 Підсумкова статистика: (сюди пізніше підключається SQL)")

        # ✅ Повертаємо користувача у головне меню
        await show_main_menu(update, context)
        return

    if text == "📉 Статистика витрат":
        keyboard = [
            [KeyboardButton("за весь період"), KeyboardButton("за рік")],
            [KeyboardButton("за місяць"), KeyboardButton("за тиждень")],
            [KeyboardButton("за сьогодні"), KeyboardButton("↩️ Головне меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🗓️ Оберіть період або введіть його самостійно у форматі dd/mm/yyyy:dd/mm/yyyy",
            reply_markup=reply_markup
        )
        context.user_data["awaiting_expense_period_input"] = True
        context.user_data["previous_menu"] = "expense_period_selection"
        return

    if context.user_data.get("awaiting_expense_period_input"):
        if text == "↩️ Повернутися":
            # Повернення до вибору періоду (цей блок, а не головне меню!)
            keyboard = [
                [KeyboardButton("за весь період"), KeyboardButton("за рік")],
                [KeyboardButton("за місяць"), KeyboardButton("за тиждень")],
                [KeyboardButton("за сьогодні"), KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(
                "🗓️ Оберіть період або введіть його самостійно у форматі dd/mm/yyyy:dd/mm/yyyy",
                reply_markup=reply_markup
            )
            return

        if text == "↩️ Головне меню":
            context.user_data["awaiting_expense_period_input"] = False
            await show_main_menu(update, context)
            return

        now = datetime.now()
        recognized = False

        if text.lower() == "за рік":
            start_date = (now - timedelta(days=365)).strftime("%d/%m/%Y")
            end_date = now.strftime("%d/%m/%Y")
            await update.message.reply_text(f"📉 Статистика витрат за рік (з {start_date} по {end_date})")
            recognized = True
        elif text.lower() == "за місяць":
            start_date = (now - timedelta(days=30)).strftime("%d/%m/%Y")
            end_date = now.strftime("%d/%m/%Y")
            await update.message.reply_text(f"📉 Статистика витрат за місяць (з {start_date} по {end_date})")
            recognized = True
        elif text.lower() == "за тиждень":
            start_date = (now - timedelta(days=7)).strftime("%d/%m/%Y")
            end_date = now.strftime("%d/%m/%Y")
            await update.message.reply_text(f"📉 Статистика витрат за тиждень (з {start_date} по {end_date})")
            recognized = True
        elif text.lower() == "за сьогодні":
            date = now.strftime("%d/%m/%Y")
            await update.message.reply_text(f"📉 Статистика витрат за сьогодні: {date}")
            recognized = True
        elif text.lower() == "за весь період":
            await update.message.reply_text("📉 Статистика витрат за весь період")
            recognized = True
        elif ":" in text:  # Введено власний період
            try:
                start_str, end_str = text.split(":")
                start_date = datetime.strptime(start_str.strip(), "%d/%m/%Y")
                end_date = datetime.strptime(end_str.strip(), "%d/%m/%Y")
                if start_date > end_date:
                    await update.message.reply_text("❌ Початкова дата не може бути пізнішою за кінцеву!")
                    return
                await update.message.reply_text(f"📉 Статистика витрат за період: {start_str} — {end_str}")
                recognized = True
            except ValueError:
                await update.message.reply_text("❌ Неправильний формат! Введіть у форматі dd/mm/yyyy:dd/mm/yyyy")
                return

        if recognized:
            # Після успішного вибору/введення періоду – показуємо наступне меню
            keyboard = [
                [KeyboardButton("За усіма категоріями")],
                [KeyboardButton("Обрати категорію")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)

            context.user_data["previous_menu"] = "expense_statistics_period"
            context.user_data["awaiting_expense_period_input"] = False
        else:
            await update.message.reply_text(
                "❌ Будь ласка, оберіть варіант зі списку або введіть період у форматі dd/mm/yyyy:dd/mm/yyyy")
        return

    if text == "📉 Статистика витрат": ## не знайшов кращого варіанту пофіксити баг з цією кнопкою
        keyboard = [
            [KeyboardButton("за весь період"), KeyboardButton("за рік")],
            [KeyboardButton("за місяць"), KeyboardButton("за тиждень")],
            [KeyboardButton("за сьогодні"), KeyboardButton("↩️ Головне меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🗓️ Оберіть період або введіть його самостійно у форматі dd/mm/yyyy:dd/mm/yyyy",
            reply_markup=reply_markup
        )
        context.user_data["awaiting_expense_period_input"] = True
        context.user_data["previous_menu"] = "expense_period_selection"
        return

    if text == "За усіма категоріями":
        # Під прапорець для подальшої обробки графіків
        context.user_data["expense_graph_all_categories"] = True

        # Показуємо кнопки графіків
        keyboard = [
            [KeyboardButton("Pie Chart")],
            [KeyboardButton("Bars")],
            [KeyboardButton("Scatter Plot")],
            [KeyboardButton("↩️ Повернутися")],
            [KeyboardButton("↩️ Головне меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("📊 Оберіть графік для відображення:", reply_markup=reply_markup)

        # Зберігаємо попереднє меню для кнопки "↩️ Повернутися"
        context.user_data["previous_menu"] = "graphs_menu_expense"
        return

    if context.user_data.get("previous_menu") == "graphs_menu_expense" and context.user_data.get(
            "expense_graph_all_categories"):
        if text == "Pie Chart":
            # Місце для SQL-запиту (отримати дані за всіма категоріями і побудувати графік Pie Chart)
            await update.message.reply_text("✅ Ви обрали графік: Pie Chart")
            await update.message.reply_text("📊 Графік Pie Chart готовий! (сюди підключається SQL-запит)")
        elif text == "Bars":
            # Місце для SQL-запиту (отримати дані за всіма категоріями і побудувати графік Bars)
            await update.message.reply_text("✅ Ви обрали графік: Bars")
            await update.message.reply_text("📊 Графік Bars готовий! (сюди підключається SQL-запит)")
        elif text == "Scatter Plot":
            # Місце для SQL-запиту (отримати дані за всіма категоріями і побудувати графік Scatter Plot)
            await update.message.reply_text("✅ Ви обрали графік: Scatter Plot")
            await update.message.reply_text("📊 Графік Scatter Plot готовий! (сюди підключається SQL-запит)")
        elif text == "↩️ Повернутися":
            # Повертаємося до меню вибору опцій статистики витрат
            keyboard = [
                [KeyboardButton("За усіма категоріями")],
                [KeyboardButton("Обрати категорію")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "expense_statistics_period"
            return
        elif text == "↩️ Головне меню":
            await show_main_menu(update, context)
            return
        else:
            await update.message.reply_text("❌ Будь ласка, оберіть варіант зі списку!")
            return

        # ✅ Після відображення графіка — повертаємо користувача у головне меню
        await update.message.reply_text("🔄 Повертаємося у головне меню...")
        context.user_data["previous_menu"] = "main_menu"
        await show_main_menu(update, context)
        return

    if text == "Обрати категорію":
        # 🟡 Тут буде SQL-запит №3 (отримати категорії)
        categories = ["Категорія 1", "Категорія 2", "Категорія 3", "Категорія 4", "Категорія 5", "Категорія 6",
                      "Категорія 7", "Не вказувати"]

        keyboard = [[KeyboardButton(cat)] for cat in categories]
        keyboard.append([KeyboardButton("↩️ Повернутися"), KeyboardButton("↩️ Головне меню")])

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("🗂️ Оберіть категорію:", reply_markup=reply_markup)

        # Встановлюємо прапорець-індикатор
        context.user_data["previous_menu"] = "choose_expense_category"
        return

    if context.user_data.get("previous_menu") == "choose_expense_category":
        if text in ["Категорія 1", "Категорія 2", "Категорія 3", "Категорія 4", "Категорія 5", "Категорія 6",
                    "Категорія 7", "Не вказувати"]:
            await update.message.reply_text(f"✅ Категорія обрана: {text}")
            context.user_data["selected_expense_category"] = text
            # 🟡 Місце для SQL-запиту №11 (обробка записів по категорії)

            keyboard = [
                [KeyboardButton("Pie Chart")],
                [KeyboardButton("Bars")],
                [KeyboardButton("Scatter Plot")],
                [KeyboardButton("Обрати підкатегорію")],
                [KeyboardButton("↩️ Повернутися"), KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("📊 Оберіть графік або підкатегорію:", reply_markup=reply_markup)

            context.user_data["previous_menu"] = "graphs_menu_choose_category"
            return

        elif text == "↩️ Повернутися":
            keyboard = [
                [KeyboardButton("За усіма категоріями")],
                [KeyboardButton("Обрати категорію")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "expense_statistics_period"
            return

        elif text == "↩️ Головне меню":
            await show_main_menu(update, context)
            return

        else:
            await update.message.reply_text("❌ Будь ласка, оберіть категорію зі списку!")
            return

    # Вибір підкатегорії
    if context.user_data.get("previous_menu") == "choose_expense_subcategory":
        if text in ["Підкатегорія 1", "Підкатегорія 2", "Підкатегорія 3", "Підкатегорія 4", "Підкатегорія 5",
                    "Підкатегорія 6", "Підкатегорія 7", "Не вказано"]:
            await update.message.reply_text(f"✅ Підкатегорія обрана: {text}")
            context.user_data["selected_subcategory"] = text
            # 🔴 Тут буде SQL-запит №4 (завантажити дані для статистики підкатегорії)

            # Переходимо до вибору графіків (без Pie Chart)
            keyboard = [
                [KeyboardButton("Bars")],
                [KeyboardButton("Scatter Plot")],
                [KeyboardButton("↩️ Повернутися")],
                [KeyboardButton("↩️ Головне меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("📊 Оберіть графік для перегляду:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "graphs_menu_expense_subcategory"
            return
        elif text == "↩️ Повернутися":
            await show_expense_subcategories_menu(update, context)  # або меню категорій
            return
        elif text == "↩️ Головне меню":
            await show_main_menu(update, context)
            return
        else:
            await update.message.reply_text("❌ Будь ласка, оберіть підкатегорію зі списку!")
            return

    # Обробка меню графіків або підкатегорії після вибору категорії
    if context.user_data.get("previous_menu") == "graphs_menu_choose_category":
        if text == "Pie Chart":
            await update.message.reply_text("✅ Ви обрали графік: Pie Chart")
            await update.message.reply_text("📊 Графік Pie Chart готовий! (сюди підключається SQL-запит)")
            context.user_data["previous_menu"] = "main_menu"
            await show_main_menu(update, context)
            return
        elif text == "Bars":
            await update.message.reply_text("✅ Ви обрали графік: Bars")
            await update.message.reply_text("📊 Графік Bars готовий! (сюди підключається SQL-запит)")
            context.user_data["previous_menu"] = "main_menu"
            await show_main_menu(update, context)
            return
        elif text == "Scatter Plot":
            await update.message.reply_text("✅ Ви обрали графік: Scatter Plot")
            await update.message.reply_text("📊 Графік Scatter Plot готовий! (сюди підключається SQL-запит)")
            context.user_data["previous_menu"] = "main_menu"
            await show_main_menu(update, context)
            return
        elif text == "Обрати підкатегорію":
            await show_expense_subcategories_menu(update, context)
            return
        elif text == "↩️ Повернутися":
            # Повертаємось до вибору категорії
            categories = ["Категорія 1", "Категорія 2", "Категорія 3", "Категорія 4", "Категорія 5", "Категорія 6",
                          "Категорія 7", "Не вказувати"]
            keyboard = [[KeyboardButton(cat)] for cat in categories]
            keyboard.append([KeyboardButton("↩️ Повернутися"), KeyboardButton("↩️ Головне меню")])
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🗂️ Оберіть категорію:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "choose_expense_category"
            return
        elif text == "↩️ Головне меню":
            await show_main_menu(update, context)
            return
        else:
            await update.message.reply_text("❌ Будь ласка, оберіть варіант зі списку!")
            return


    if context.user_data.get("previous_menu") == "graphs_menu_expense_subcategory":
        if text == "Bars":
            await update.message.reply_text("✅ Ви обрали графік: Bars")
            await update.message.reply_text("📊 Графік Bars готовий! (сюди підключається SQL-запит)")
            context.user_data["previous_menu"] = "main_menu"
            await show_main_menu(update, context)
            return
        elif text == "Scatter Plot":
            await update.message.reply_text("✅ Ви обрали графік: Scatter Plot")
            await update.message.reply_text("📊 Графік Scatter Plot готовий! (сюди підключається SQL-запит)")
            context.user_data["previous_menu"] = "main_menu"
            await show_main_menu(update, context)
            return
        elif text == "↩️ Повернутися":
            await show_expense_subcategories_menu(update, context)
            return
        elif text == "↩️ Головне меню":
            await show_main_menu(update, context)
            return
        else:
            await update.message.reply_text("❌ Будь ласка, оберіть графік зі списку!")
            return

    if text == "Мої ліміти":
        await show_user_limits_menu(update, context)
        return

    if text == "🔢 Ліміти":
        await show_limits_menu(update, context)
        context.user_data["previous_menu"] = "main_menu"
        return

    if context.user_data.get("previous_menu") == "limits_menu":
        if text in ["Ліміт 1", "Ліміт 2", "Ліміт 3"]:
            await show_limit_details(update, context, text)
            context.user_data["selected_limit"] = text
            return
        elif text == "↩️ Повернутися":
            await show_limits_menu(update, context)
            return
        elif text == "↩️ Головне меню":
            await show_main_menu(update, context)
            return

    if context.user_data.get("previous_menu") == "limit_details":
        if text == "❌ Видалити":
            # 🔴 ПІД SQL: видалити ліміт з БД за назвою context.user_data["selected_limit"]
            # delete_limit(context.user_data["selected_limit"])
            await update.message.reply_text(
                "✅ Ліміт успішно видалено. Ви можете створити його знову за допомогою опції 'Новий ліміт'"
            )
            await show_limits_menu(update, context)
            return
        elif text == "↩️ Повернутися":
            await show_user_limits_menu(update, context)
            return
        elif text == "↩️ Головне меню":
            await show_main_menu(update, context)
            return

    if text == "Новий ліміт":
        await handle_new_limit(update, context)
        return

    if context.user_data.get("awaiting_limit_sum"):
        if text == "↩️ Повернутися":
            context.user_data.pop("awaiting_limit_sum")
            await show_user_limits_menu(update, context)
            context.user_data["previous_menu"] = "limits_menu"
            return
        elif text == "↩️ Головне меню":
            context.user_data.pop("awaiting_limit_sum")
            await show_main_menu(update, context)
            return
        elif text == "За категорією":
            # Перехід до вибору категорії (прикладний виклик твоєї функції)
            context.user_data.pop("awaiting_limit_sum", None)
            await show_categories_menu(update)
            context.user_data["previous_menu"] = "new_limit_category"
            return
        else:
            try:
                limit_sum = float(text)
                # 🔴 SQL-запит №14 – створення ліміту з сумою
                await update.message.reply_text(
                    f"✅ Ліміт встановлено: {limit_sum} грн. Ви можете налаштувати категорію пізніше."
                )
                await show_user_limits_menu(update, context)
                context.user_data.pop("awaiting_limit_sum")
                return
            except ValueError:
                await update.message.reply_text("❌ Будь ласка, введіть коректне число!")
                return

    if text == "За категорією":
        # 🔴 SQL-запит №3 (отримуємо категорії користувача)
        categories = ["Категорія 1", "Категорія 2", "Категорія 3", "Категорія 4", "Категорія 5", "Категорія 6",
                      "Категорія 7", "Не вказано"]
        keyboard = [[KeyboardButton(cat)] for cat in categories]
        keyboard.append([KeyboardButton("Повернутися"), KeyboardButton("Головне меню")])
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("🗂️ Оберіть категорію:", reply_markup=reply_markup)
        context.user_data["previous_menu"] = "new_limit_category"
        return

    if context.user_data.get("previous_menu") == "new_limit_category":
        if text in ["Категорія 1", "Категорія 2", "Категорія 3", "Категорія 4", "Категорія 5", "Категорія 6",
                    "Категорія 7", "Не вказано"]:
            context.user_data["selected_limit_category"] = text
            await update.message.reply_text(
                f"✅ Категорія обрана: {text}\n\nВведіть суму ліміту або оберіть підкатегорію.",
                reply_markup=ReplyKeyboardMarkup([
                    [KeyboardButton("За підкатегорією")],
                    [KeyboardButton("Повернутися")],
                    [KeyboardButton("Головне меню")]
                ], resize_keyboard=True)
            )
            context.user_data["previous_menu"] = "new_limit_selected_category"
            return
        elif text == "Повернутися":
            # Повертаємося у меню "Новий ліміт"
            await handle_new_limit(update, context)
            return
        elif text == "Головне меню":
            await show_main_menu(update, context)
            return
        else:
            await update.message.reply_text("❌ Будь ласка, оберіть варіант зі списку!")
            return

    if context.user_data.get("previous_menu") == "new_limit_selected_category":
        if text == "Повернутися":
            # Повернення до вибору категорії
            categories = ["Категорія 1", "Категорія 2", "Категорія 3", "Категорія 4", "Категорія 5", "Категорія 6",
                          "Категорія 7", "Не вказано"]
            keyboard = [[KeyboardButton(cat)] for cat in categories]
            keyboard.append([KeyboardButton("Повернутися"), KeyboardButton("Головне меню")])
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🗂️ Оберіть категорію:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "new_limit_category"
            return
        elif text == "Головне меню":
            await show_main_menu(update, context)
            return
        elif text == "За підкатегорією":
            # 🔴 SQL: отримати підкатегорії для обраної категорії
            subcategories = ["Підкатегорія 1", "Підкатегорія 2", "Підкатегорія 3", "Підкатегорія 4", "Підкатегорія 5",
                             "Не вказано"]
            keyboard = [[KeyboardButton(sub)] for sub in subcategories]
            keyboard.append([KeyboardButton("Повернутися"), KeyboardButton("Головне меню")])
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("📂 Оберіть підкатегорію:", reply_markup=reply_markup)
            context.user_data["previous_menu"] = "new_limit_subcategory"
            return
        else:
            # Користувач вводить СУМУ ліміту для обраної категорії
            try:
                limit_sum = float(text)
                # 🔴 SQL-запит №14 (зберігаємо ліміт для категорії)
                await update.message.reply_text(
                    f"✅ Ліміт для категорії '{context.user_data.get('selected_limit_category', 'Не вказано')}' встановлено: {limit_sum} грн."
                )
                await show_user_limits_menu(update, context)
                context.user_data.pop("previous_menu")
                context.user_data.pop("selected_limit_category")
                return
            except ValueError:
                await update.message.reply_text("❌ Будь ласка, введіть коректне число або оберіть підкатегорію!")
                return


# ➡️ Обробка помилок
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# ➡️ Основна логіка
def main():
    print("✅ Стартуємо бота...")
    application = Application.builder().token(TOKEN).build()

    # Обробники
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🚀 Початок роботи$"), handle_start_button))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^➕ Додати прибуток$"), add_profit_button))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^➕ Додати витрату$"), add_expense_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_error_handler(error)

    print("🤖 Бот працює (polling)...")
    application.run_polling(poll_interval=1)

if __name__ == "__main__":
    main()
