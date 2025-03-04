import logging
import asyncio
from config import token

import requests
import time as tm

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.methods import DeleteWebhook


bot = Bot(token=token)
dp = Dispatcher()
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac Os X 10.9; rv:45.0) Gecko/201001101 Firefox/45.0"}
link = "https://kursk-news.ru/all"
group_id = -1002407238556
pulling_messages = False


@dp.message(CommandStart())
async def command_start_handler(message: Message):



async def message_handler(message: Message):
    update_time = tm.strftime('%d.%m.%Y %H+3:%M:%S', tm.gmtime())
    logging.info(f"{update_time}; chat id = {message.from_user.id}; user name = {message.from_user.full_name}; "
                 f"message type = {message.content_type}")

    await message.answer("Сообщение доставлено. Спасибо, что связались с нами!")


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())