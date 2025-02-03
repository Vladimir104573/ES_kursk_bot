import logging
import time
import asyncio
from config import token

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.methods import DeleteWebhook


bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}!")


@dp.message()
async def message_handler(message: Message):
    update_time = time.strftime('%d.%m.%Y %H+3:%M:%S', time.gmtime())
    logging.info(f"{update_time}; chat id = {message.from_user.id}; user name = {message.from_user.full_name}; "
                 f"message type = {message.content_type}")

    await message.answer("Сообщение доставлено. Спасибо, что связались с нами!")


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())