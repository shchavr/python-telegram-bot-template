#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import logging
import random
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING = range(1)

reply_keyboard = [
    ["Наука", "История"],
    ["Природа", "Случайный"],
    ["Стоп"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

facts = {
    "Наука": [
        "Свет проходит от Солнца до Земли примерно за 8 минут.",
        "Вода может существовать в трех состояниях: твердом, жидком и газообразном.",
        "Человеческий мозг на 75% состоит из воды.",
        "Атомы на 99.9999999999999% пусты.",
        "Земля вращается вокруг своей оси со скоростью около 1670 километров в час.",
        "Генетический материал человека на 99.9% идентичен генетическому материалу шимпанзе.",
        "Температура внутри звезды может достигать 15 миллионов градусов Цельсия.",
        "Ультразвук используется в медицине для диагностики и лечения.",
        "Микробы, живущие в нашем организме, составляют до 90% клеток, которые находятся в нашем теле.",
        "Кристаллы соли могут помочь в сохранении продуктов, так как обладают антимикробными свойствами."
    ],
    "История": [
        "Древние египтяне строили пирамиды, используя тысячи рабочих.",
        "Первая известная цивилизация — Шумеры в Месопотамии.",
        "Вторжение в Великобританию произошло в 1066 году во время Нормандского завоевания.",
        "В 1492 году Колумб открыл Америку.",
        "Римская империя достигла своего максимального развития около 117 года н.э.",
        "Сунь Цзы, древнекитайский полководец, написал 'Искусство войны' более 2500 лет назад.",
        "Первые Олимпийские игры прошли в Греции в 776 году до н.э.",
        "В Средние века европейцы верили, что Земля плоская и окружена морем.",
        "Фараоны Древнего Египта правили более 3000 лет.",
        "Эпидемия чумы в Европе в XIV веке убила около 25 миллионов человек."
    ],
    "Природа": [
        "В мире существует около 8,7 миллионов видов живых организмов.",
        "Самая высокая гора на Земле — Эверест, высота 8848 метров.",
        "Медузы не имеют мозга, сердца и костей.",
        "Лягушки могут замедлять свой метаболизм так, что они могут 'спать' в течение многих месяцев.",
        "Слон — единственное млекопитающее, которое не может прыгать.",
        "Леса обеспечивают около 28% кислорода на Земле.",
        "Большие океанские волны могут достигать высоты более 30 метров.",
        "У различных видов бабочек могут быть разные цвета и узоры на крыльях.",
        "Фаун на Антарктиде и других континентах развивается отдельно, что делает экосистему уникальной.",
        "Коралловые рифы являются одним из самых разнообразных экосистем на планете."
    ],
    "Случайный": [
        "Водопад Анхель в Венесуэле — самый высокий водопад в мире, высота 979 метров.",
        "В Австралии больше овец, чем людей.",
        "Курицы могут помнить лица до 100 различных людей.",
        "Бобры имеют непрерывный рост зубов, которые они должны стачивать.",
        "Дельфины могут распознавать себя в зеркале.",
        "Панды могут есть до 38 килограммов бамбука в день.",
        "Альбатрос может пролететь более 10 000 километров без остановки.",
        "В мире существует более 2000 видов растений, которые являются съедобными.",
        "Самая тёмная тень создаётся в полнолуние, когда луна полностью освещает землю.",
        "Выдры держатся за руки, когда спят, чтобы не потерять друг друга в воде."
    ]
}


def get_random_fact(category: str) -> str:
    """Получить случайный факт по заданной категории."""
    logger.info(f"Запрос факта для категории: {category}")  # Логгируем категорию
    
    if category in facts:
        fact = random.choice(facts[category])  # Выбираем случайный факт из списка
        logger.info(f"{fact}")  # Логгируем полученный факт
        return fact
    else:
        logger.error(f"Неизвестная категория: {category}")
        return "Не удалось получить факт, попробуйте другую категорию."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начните разговор и покажите варианты для категорий фактов."""
    user = update.message.from_user
    logger.info(f"User {user.full_name} started app.")
    
    await update.message.reply_text(
        "Привет! Я бот-генератор фактов. Выберите категорию:",
        reply_markup=markup
    )

    return CHOOSING

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора категории фактов от пользователя."""
    category = update.message.text
    if category == "Стоп":
        await update.message.reply_text("Вы остановили бота. Чтобы запустить снова, введите /start.")
        return ConversationHandler.END

    context.user_data["category"] = category


    fact = get_random_fact(category)
    await update.message.reply_text(f"{fact}")

    return CHOOSING

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершить разговор и попрощаться с пользователем."""
    await update.message.reply_text("Спасибо за использование бота! До свидания!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик для отмены."""
    await update.message.reply_text("Вы отменили разговор. До свидания!")
    return ConversationHandler.END

def main() -> None:
    """Запуск бота."""
    application = Application.builder().token("7266582099:AAHE3QmlHbA_9Jn1gC4amAzYo8I1bQRzNHA").build()

    # Определение обработчиков для разговоров
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, regular_choice)
            ],
        },
        fallbacks=[CommandHandler("done", done), CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()



# Попытка использовать API
# import os
# import logging
# from typing import Dict
# import requests
# from telegram import ReplyKeyboardMarkup, Update
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     ContextTypes,
#     ConversationHandler,
#     MessageHandler,
#     filters,
# )

# # Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )

# logger = logging.getLogger(__name__)

# CHOOSING = range(1)

# reply_keyboard = [
#     ["Наука", "История"],
#     ["Природа", "Случайный"],
#     ["Стоп"],
# ]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

# def get_random_fact(category: str) -> str:
#     """Получить случайный факт по заданной категории."""
#     logger.info(f"Запрос факта для категории: {category}")  # Логгируем категорию
#     if category == "Наука":
#         response = requests.get("https://some-random-api.ml/facts/science")
#     elif category == "История":
#         response = requests.get("https://api.adviceslip.com/advice")  # Это не совсем факты, но можно использовать другое API
#     elif category == "Природа":
#         response = requests.get("https://some-random-api.ml/facts/nature")
#     else:  # Случайный
#         response = requests.get("https://uselessfacts.jsph.pl/random.json?language=ru")

#     if response.status_code == 200:
#         if category in ["Наука", "Природа"]:
#             fact = response.json().get("fact", "Нет доступных фактов.")
#             logger.info(f"Получен факт: {fact}")  # Логгируем полученный факт
#             return fact
#         elif category == "Случайный":
#             fact = response.json().get('text', 'Нет доступных фактов.')  # Проверяем ключ
#             return fact
#         return response.json().get('slip', {}).get('advice', 'Нет доступных фактов.')

#     logger.error(f"Ошибка получения факта: {response.status_code}")  # Логгируем ошибку
#     return "Не удалось получить факт, попробуйте еще раз."

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Начните разговор и покажите варианты для категорий фактов."""
#     user = update.message.from_user
#     logger.info(f"User {user.full_name} started app.")
    
#     await update.message.reply_text(
#         "Привет! Я бот-генератор фактов. Выберите категорию:",
#         reply_markup=markup
#     )

#     return CHOOSING

# async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Обработка выбора категории фактов от пользователя."""
#     category = update.message.text
#     if category == "Стоп":


#         await update.message.reply_text("Вы остановили бота. Чтобы запустить снова, введите /start.")
#         return ConversationHandler.END

#     context.user_data["category"] = category
#     fact = get_random_fact(category)
#     await update.message.reply_text(f"Вот ваш факт о {category}: {fact}")

#     return CHOOSING

# async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Завершить разговор и попрощаться с пользователем."""
#     await update.message.reply_text("Спасибо за использование бота! До свидания!")
#     return ConversationHandler.END

# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Обработчик для отмены."""
#     await update.message.reply_text("Вы отменили разговор. До свидания!")
#     return ConversationHandler.END

# def main() -> None:
#     """Запуск бота."""
#     application = Application.builder().token("7266582099:AAHE3QmlHbA_9Jn1gC4amAzYo8I1bQRzNHA").build()

#     # Определение обработчиков для разговоров
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("start", start)],
#         states={
#             CHOOSING: [
#                 MessageHandler(filters.TEXT & ~filters.COMMAND, regular_choice)
#             ],
#         },
#         fallbacks=[CommandHandler("done", done), CommandHandler("cancel", cancel)],
#     )

#     application.add_handler(conv_handler)

#     # Запуск бота
#     application.run_polling()

# if __name__ == '__main__':
#     main()




# import os
# from dotenv import load_dotenv
# from telegram.ext import ApplicationBuilder

# def main():
#     load_dotenv()  # Загрузка переменных окружения из файла .env
#     token = os.getenv("BOT_TOKEN")

#     # Вывод токена на экран (не публикуйте этот токен в открытых источниках!)
#     print(f"Токен: {token}")

#     if not token:
#         print("Ошибка: токен бота не установлен или не загружен.")
#         return  # Прекратить выполнение, если токен не загружен

#     application = ApplicationBuilder().token(token).build()
#     # ... остальная логика вашего бота ...

# if __name__ == "__main__":
#     main()




# Попытка усовершенстовать бота
# import os
# import logging
# import random
# from telegram import ReplyKeyboardMarkup, Update
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     ContextTypes,
#     ConversationHandler,
#     MessageHandler,
#     filters,
# )

# # Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )

# logger = logging.getLogger(__name__)

# CHOOSING, FACTS, QUIZ = range(3)

# reply_keyboard = [
#     ["Факты", "Викторина"],
#     ["Стоп"],
# ]

# facts = {
#     "Наука": [
#         "Свет проходит от Солнца до Земли примерно за 8 минут.",
#         "Вода может существовать в трех состояниях: твердом, жидком и газообразном.",
#         "Человеческий мозг на 75% состоит из воды.",
#     ],
#     "История": [
#         "Древние египтяне строили пирамиды, используя тысячи рабочих.",
#         "Первая известная цивилизация — Шумеры в Месопотамии.",
#     ],
#     "Природа": [
#         "В мире существует около 8,7 миллионов видов живых организмов.",
#         "Самая высокая гора на Земле — Эверест, высота 8848 метров.",
#     ],
#     "Случайный": [
#         "Водопад Анхель в Венесуэле — самый высокий водопад в мире, высота 979 метров.",
#         "В Австралии больше овец, чем людей.",
#     ]
# }

# questions = {
#     "Какой элемент химической таблицы обозначается символом 'O'?": ["Кислород", "Азот", "Водород", "Углерод"],
#     "Какой океан самый большой?": ["Атлантический", "Индийский", "Тихий", "Северный Ледовитый"],
# }

# def get_random_fact(category: str) -> str:
#     logger.info(f"Запрос факта для категории: {category}")
    
#     if category in facts:
#         fact = random.choice(facts[category])
#         logger.info(f"{fact}")
#         return fact
#     else:
#         logger.error(f"Неизвестная категория: {category}")
#         return "Не удалось получить факт, попробуйте другую категорию."

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     user = update.message.from_user
#     logger.info(f"User {user.full_name} started app.")
    
#     await update.message.reply_text(
#         "Привет! Я бот-генератор фактов и викторин. Выберите опцию:",
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
#     )

#     return CHOOSING

# async def facts_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     await update.message.reply_text("Выберите категорию фактов: Наука, История, Природа, Случайный.")

#     return FACTS

# async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     category = update.message.text
#     fact = get_random_fact(category)
#     await update.message.reply_text(f"{fact}")
    
#     # Предложить выбрать снова
#     await update.message.reply_text(
#         "Хотите получить еще факты или вернуться в меню? (Введите 'Факты' для выбора фактов, 'Викторина' для викторины или 'Стоп' для выхода)",
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
#     )

#     return CHOOSING

# async def quiz_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     question = random.choice(list(questions.keys()))
#     options = questions[question]
#     reply_keyboard = [[option] for option in options]


#     await update.message.reply_text(question, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
#     context.user_data["correct_answer"] = options[0]  # Первая опция — правильный ответ

#     return QUIZ

# async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     user_answer = update.message.text
#     correct_answer = context.user_data["correct_answer"]
    
#     if user_answer == correct_answer:
#         await update.message.reply_text("Правильно! Молодец!")
#     else:
#         await update.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}.")
    
#     # Предложить выбрать снова
#     await update.message.reply_text(
#         "Хотите продолжить викторину или вернуться в меню? (Введите 'Факты' для выбора фактов, 'Викторина' для викторины или 'Стоп' для выхода)",
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
#     )

#     return CHOOSING

# async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     await update.message.reply_text("Спасибо за использование бота! До свидания!")
#     return ConversationHandler.END

# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     await update.message.reply_text("Вы отменили разговор. До свидания!")
#     return ConversationHandler.END

# def main() -> None:
#     application = Application.builder().token("7266582099:AAHE3QmlHbA_9Jn1gC4amAzYo8I1bQRzNHA").build()

#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("start", start)],
#         states={
#             CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, facts_choice)],
#             FACTS: [
#                 MessageHandler(filters.TEXT & ~filters.COMMAND, regular_choice)
#             ],
#             QUIZ: [
#                 MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_answer)
#             ],
#         },
#         fallbacks=[CommandHandler("done", done), CommandHandler("cancel", cancel)],
#     )

#     application.add_handler(conv_handler)

#     application.run_polling()

# if __name__ == '__main__':
#     main()