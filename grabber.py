from telethon.sync import TelegramClient
from telethon import errors

import time
import asyncio

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest
from config import api_id, api_hash, username


client = TelegramClient(username, api_id, api_hash)
client.start()


async def dump_all_messages(channel):
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз
    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    while True:
        try:
            history = await client(GetHistoryRequest(
                peer=channel,
                offset_id=offset_msg,
                offset_date=None, add_offset=0,
                limit=limit_msg, max_id=0, min_id=0,
                hash=0))
            if not history.messages:
                time.sleep(60)
            messages = history.messages
            for message in messages:
                all_messages.append(message.to_dict())
            for i in all_messages:
                print(i)
            print("done...")
        except errors.FloodWaitError as e:
            print(f"Flood wait {e.seconds}")
            await asyncio.sleep(e.seconds)


async def main():
    channel = await client.get_entity("https://t.me/efssefsefefsf")
    await dump_all_messages(channel)


with client:
    client.loop.run_until_complete(main())