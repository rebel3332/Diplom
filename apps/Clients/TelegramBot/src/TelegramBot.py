import requests
from telebot.async_telebot import AsyncTeleBot
import asyncio
from mylib import *
import os
from dotenv import load_dotenv

if __name__ == '__main__':
    if load_dotenv():
        loging.INFO("Read ENVIROMENTS from file .env")
    else:
        loging.WARM("File .env don't found. You can used ENVIROMENTS in your OS.")

    TELEGRAM_API = os.getenv('TELEGRAM_API')
    SERVER_URL = os.getenv('SERVER_URL')

    bot = AsyncTeleBot(TELEGRAM_API)

    # Handle '/start' and '/help'
    @bot.message_handler(commands=['start'])
    async def send_welcome(message):
        loging.INFO('/start')
        await bot.reply_to(message, """\
    Привет.\b
    Это Telegram бот, который умеет делать предсказания для акции Амазон\b
    Минимальный шаг предсказания, неделя.\b
    /help - помощь                     
    """)


    @bot.message_handler(commands=['predict'])
    async def send_welcome(message):
        loging.INFO('/predict')
        wordsFromMessage = message.text.replace('  ', ' ').split(' ')
        if len(wordsFromMessage) == 2:
            data = wordsFromMessage[1]
            # r = requests.get(SERVER_URL + '/predict', json=data)
            loging.INFO(f'{SERVER_URL}/predict/{data}')
            try:
                r = requests.get(f'{SERVER_URL}/predict/{data}')
                await bot.reply_to(message, r.text)
            except Exception as ex:
                loging.ERROR(str(ex))
                await bot.reply_to(message, 'К сожалению произошла ошибка')
        else:
            await bot.reply_to(message, """Надо ввести диапазон предсказания, например 1w или 10w
Пример: /predict 1w""")


    @bot.message_handler(commands=['help'])
    async def send_welcome(message):
            loging.INFO('/help')
            await bot.reply_to(message, """Помощ:
    /predict <временной диапазон>   -   Выводит предсказание цены на заданный временной диапазон.
                                        Доступны 1w, 2w, 3w, ...
                                        Пример: /predict 1w""")


    # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
    @bot.message_handler(func=lambda message: True)
    async def echo_message(message):
        await bot.reply_to(message, "К сожалению такой команды нет, для вывода помощи наберите /help")

    loging.INFO(f'Telegram bot is start')
    asyncio.run(bot.polling())