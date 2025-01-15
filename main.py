import configparser
import json

from telethon.sync import TelegramClient
from telethon import connection

from datetime import date, datetime

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetHistoryRequest

import logging
import time
import asyncio
from config import api_id, api_hash, username, token

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.methods import DeleteWebhook

client = TelegramClient(username, api_id, api_hash)
client.start()

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


async def dump_all_messages(channel):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    class DateTimeEncoder(json.JSONEncoder):
        '''Класс для сериализации записи дат в JSON'''

        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open('channel_messages.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main():
    channel = await client.get_entity("https://t.me/efssefsefefsf")
    await dump_all_messages(channel)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
