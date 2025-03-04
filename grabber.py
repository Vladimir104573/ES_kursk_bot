import logging
import asyncio
from config import token

import requests
import time as tm

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.methods import DeleteWebhook


def emergency_situation(string):
    string = string.lower()
    if "ракетная опасность" in string and "noindex" in string:
        return f"{string.split('noindex>')[1][-7:-2]} - РО"

    elif "отбой ракетной опасности" in string and "noindex" in string:
        return f"{string.split('noindex>')[1][-7:-2]} - ОРО"

    elif "БПЛА" in string and "noindex" in string:
        return f"{string.split('noindex>')[1][-7:-2]} - БПЛА"

    elif "БПЛА" in string and "отбой" in string and "noindex" in string:
        return f"{string.split('noindex>')[1][-7:-2]} - ОБПЛА"
    else:
        return "No update"


bot = Bot(token=token)
dp = Dispatcher()
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac Os X 10.9; rv:45.0) Gecko/201001101 Firefox/45.0"}
link = "https://kursk-news.ru/all"


@dp.message(CommandStart())
async def command_start_handler(message: Message):

    data = []

    # req = requests.get(link, headers=headers)
    # text = req.text.split("div")
    # for string in text:
    #     update = emergency_situation(string)
    #     if update not in data:
    #         data.append(update)
    #
    # tm.sleep(60)

    while True:

        req = requests.get(link, headers=headers)
        text = req.text.split("div")

        for string in text:
            update = emergency_situation(string)
            if update not in data:
                data.append(update)
                print(update)

        tm.sleep(5)


@dp.message()
async def message_handler(message: Message):
    update_time = tm.strftime('%d.%m.%Y %H+3:%M:%S', tm.gmtime())
    logging.info(f"{update_time}; chat id = {message.from_user.id}; user name = {message.from_user.full_name}; "
                 f"message type = {message.content_type}, {message.chat.id}")

    await message.answer("Сообщение доставлено. Спасибо, что связались с нами!")


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())