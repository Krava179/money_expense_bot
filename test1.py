from typing import Final
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, Updater

## API токен бота та назва
TOKEN: Final = '7824502490:AAEacrJ8XMEoxuky3l2rKkNZyT_q5wnXLbQ'
BOT_USERNAME = '@money_expenses_control_bot'

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
        await show_main_menu(update)

## Головне меню
async def show_main_menu(update: Update):
    keyboard = [
        [KeyboardButton("➕ Додати прибуток"), KeyboardButton("📈 Перегляд прибутку"), KeyboardButton("📊 Статистика")],
        [KeyboardButton("➕ Додати витрату"), KeyboardButton("📉 Перегляд витрат"), KeyboardButton("🔢 Ліміти")],
        [KeyboardButton("⚙️ Управління акаунтом")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("✅ Головне меню:", reply_markup=reply_markup)

## Меню після додавання прибутку
async def show_after_adding_profit_menu(update: Update):
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

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Якщо користувач у режимі введення суми
    if context.user_data.get("awaiting_profit_sum"):
        if text == "↩️ Головне меню":
            context.user_data["awaiting_profit_sum"] = False
            await show_main_menu(update)
            return
        try:
            profit = float(text)
            await update.message.reply_text(f"✅ Додано прибуток: {profit} грн")
            context.user_data["profit_sum"] = profit ## зберігання даних для виведення та зберігання в БД
            context.user_data["awaiting_profit_sum"] = False
            await show_after_adding_profit_menu(update)
        except ValueError:
            await update.message.reply_text("❌ Будь ласка, введіть коректне число!")
        return

        # Якщо користувач натиснув "↩️ Головне меню" у будь-якому місці
    if text == "↩️ Головне меню":
        await show_main_menu(update)
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
        await show_main_menu(update)
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
            await show_after_adding_profit_menu(update)
        elif previous_menu == "statistics":
            await show_statistics_menu(update)
            context.user_data["previous_menu"] = "main_menu"
        elif previous_menu == "graphs_menu":
            await show_graphs_menu(update, context, all_sources=context.user_data.get("graph_all_sources", False))
        else:
            await show_main_menu(update)
        return

    ## дата
    if text == "📅 Дата":
        context.user_data["awaiting_date_input"] = True
        # Важливо: вказуємо, де ми – у прибутку чи витраті
        context.user_data["current_mode"] = "profit" if context.user_data.get("awaiting_profit_sum") else "expense"
        await show_date_menu(update)
        return

    if text == "📌 Джерело":
        await show_sources_menu(update)
        return

    if text in ["Джерело 1", "Джерело 2", "Джерело 3", "Джерело 4", "Джерело 5", "Джерело 6", "Джерело 7",
                "Не вказувати"]:
        await update.message.reply_text(f"✅ Джерело обрано: {text}")
        ## Тут треба реалізувати SQL-запит 1

        ##
        context.user_data["selected_source"] = text ## зберігання даних для виведення та зберігання в БД
        await show_after_adding_profit_menu(update)
        return


    ## Введення та валідація дати для прибутку та витрат
    if context.user_data.get("awaiting_date_input"):
        if text == "↩️ Повернутися":
            context.user_data["awaiting_date_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update)
            else:
                await show_after_adding_expense_menu(update, context)
            return

        if text == "Сьогодні":
            date = datetime.now().strftime("%d/%m/%Y")
            context.user_data["selected_date"] = date
            await update.message.reply_text(f"✅ Дата встановлена: {date}")
            context.user_data["awaiting_date_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update)
            else:
                await show_after_adding_expense_menu(update, context)
            return

        if text == "Вчора":
            date = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
            context.user_data["selected_date"] = date
            await update.message.reply_text(f"✅ Дата встановлена: {date}")
            context.user_data["awaiting_date_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update)
            else:
                await show_after_adding_expense_menu(update, context)
            return

        try:
            parsed_date = datetime.strptime(text, "%d/%m/%Y")
            context.user_data["selected_date"] = text
            await update.message.reply_text(f"✅ Дата встановлена: {text}")
            context.user_data["awaiting_date_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update)
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
                await show_after_adding_profit_menu(update)
            else:
                await show_after_adding_expense_menu(update, context)
            return

        # Валідація: довжина коментаря від 3 до 200
        if 3 <= len(text) <= 200:
            context.user_data["comment"] = text
            await update.message.reply_text("✅ Коментар додано!")
            context.user_data["awaiting_comment_input"] = False
            if context.user_data.get("current_mode") == "profit":
                await show_after_adding_profit_menu(update)
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
            await show_main_menu(update)
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

    # Якщо користувач у режимі введення періоду
    if context.user_data.get("awaiting_period_input"):
        if text == "↩️ Головне меню":
            context.user_data["awaiting_period_input"] = False
            await show_main_menu(update)
            return

        # Валідація: має бути формат dd/mm/yyyy:dd/mm/yyyy
        try:
            period_parts = text.split(":")
            if len(period_parts) == 2:
                datetime.strptime(period_parts[0], "%d/%m/%Y")
                datetime.strptime(period_parts[1], "%d/%m/%Y")
                context.user_data["selected_period"] = text
                context.user_data["awaiting_period_input"] = False
                await update.message.reply_text("✅ Період встановлено!")

                # Після успішної валідації показуємо меню «За всіма джерелами» / «Обрати джерело»
                keyboard = [
                    [KeyboardButton("За усіма джерелами")],
                    [KeyboardButton("Обрати джерело")],
                    [KeyboardButton("↩️ Повернутися")],
                    [KeyboardButton("↩️ Головне меню")]
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                await update.message.reply_text("🔍 Оберіть опцію:", reply_markup=reply_markup)
            else:
                raise ValueError  # щоб спрацював except
        except ValueError:
            await update.message.reply_text(
                "❌ Неправильний формат. Введіть у форматі dd/mm/yyyy:dd/mm/yyyy, наприклад: 01/01/2024:31/12/2024"
            )
        return

    if text == "За усіма джерелами":
        context.user_data["graph_all_sources"] = True
        await show_graphs_menu(update, context, all_sources=True)
        context.user_data["previous_menu"] = "statistics"
        return

    if text == "Обрати джерело":
        context.user_data["graph_all_sources"] = False
        keyboard = [
            [KeyboardButton("Джерело 1"), KeyboardButton("Джерело 2")],
            [KeyboardButton("Джерело 3"), KeyboardButton("Джерело 4")],
            [KeyboardButton("Джерело 5"), KeyboardButton("Джерело 6")],
            [KeyboardButton("Джерело 7"), KeyboardButton("Не вказано")],
            [KeyboardButton("↩️ Повернутися")],
            [KeyboardButton("↩️ Головне меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Оберіть джерело:", reply_markup=reply_markup)
        context.user_data["previous_menu"] = "statistics"
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