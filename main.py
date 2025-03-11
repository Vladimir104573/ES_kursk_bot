import logging
import asyncio
from config import token

import requests
import time as tm

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.methods import DeleteWebhook


async def cycle():
    while True:
        await bot.send_message(text='ok', chat_id='-1002407238556')
        tm.sleep(10)


def emergency_situation(string):
    global RE, BPLAE

    string = string.lower()
    if "ракетная опасность" in string and "noindex" in string:
        RE = True
        return ['RE', f"{string.split('noindex>')[1][-7:-2]}", True]

    elif "отбой ракетной опасности" in string and "noindex" in string:
        RE = False
        return ['RE', f"{string.split('noindex>')[1][-7:-2]}", False]

    elif "БПЛА" in string and "noindex" in string:
        BPLAE = True
        return ['BPLAE', f"{string.split('noindex>')[1][-7:-2]}", True]

    elif "БПЛА" in string and "отбой" in string and "noindex" in string:
        BPLAE = False
        return ['BPLAE', f"{string.split('noindex>')[1][-7:-2]}", False]
    else:
        return 0


async def send_messages(emergency, status):
    if emergency == 'RE':

        if status is True:
            message = '💥Внимание! Ракетная Опасность!💥'
        else:
            message = '🟢Отбой ракетной опасности!🟢'

    if emergency == 'BPLAE':

        if status is True:
            message = '🔴Внимание! Опасность атаки БПЛА!🔴'
        else:
            message = '🟢Отбой опасности атаки БПЛА!🟢'

    file = open('data.txt', 'r')
    data = file.read().split()
    file.close()

    for number in data:
        await bot.send_message(text=message, chat_id=number)


def show_bot_values():
    return f"Сборка информации с новостного сайта: {GRABBING_SITE}\n" \
           f"Ракетная опасность: {RE}\n" \
           f"Опасность атаки БПЛА: {BPLAE}\n"


def bot_commands_help():
    return f"Другие команды:\n" \
           f"/dev_start - начать собирать данные с новостного сайтв\n" \
           f"/RE - изменить статус ракетной опасности\n"\
           f"/BPLAE - изменить статус опасности атаки БПЛА\n" \
           f"/dev_help - показать все переменные бота / помощь по командам\n" \
           f"/dev_stop - прекратить собирать данные с новостного сайта\n"


bot = Bot(token=token)
dp = Dispatcher()

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac Os X 10.9; rv:45.0) Gecko/201001101 Firefox/45.0"}
link = "https://kursk-news.ru/all"

group_id = -1002407238556
GRABBING_SITE = False
RE = False
BPLAE = False


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}! Чтобы получать уведомления о ракетной опасности"
                         f" и опасности атаки БПЛА введите /warn. Чтобы отписаться от рассылки, введите /stop.")


@dp.message(Command('warn'))
async def add_chat_warning(message: Message):
    number = str(message.chat.id)

    file = open('data.txt', 'r')
    data = file.read().split()
    file.close()

    if number in data:
        await message.answer(f"Похоже, что Вы уже подписались на рассылку.")

    else:
        data.append(number)
        data = ' '.join(data)

        file = open('data.txt', 'w')
        file.write(data)
        file.close()

        await message.answer("Вы подписались на рассылку и будете получать уведомления."
                             " Чтобы отписаться, введите /stop.")


@dp.message(Command('stop'))
async def remove_chat_warning(message: Message):
    number = str(message.chat.id)

    file = open('data.txt', 'r')
    data = file.read().split()
    file.close()

    if number not in data:
        await message.answer(f"Похоже, что Вы ещё не подписались на рассылку.")

    else:
        data.remove(number)
        data = ' '.join(data)

        file = open('data.txt', 'w')
        file.write(data)
        file.close()

        await message.answer("Вы отписались от рассылки и больше не будете получать уведомления."
                             " Чтобы подписаться, введите /warn.")


@dp.message(Command('dev_start'))
async def dev_start(message: Message):
    global GRABBING_SITE, RE, BPLAE
    if message.chat.id != group_id:
        pass

    await message.answer("Начинаем собирать данные...")

    GRABBING_SITE = True
    RE = False
    BPLAE = False

    await message.answer(show_bot_values())
    data = []

    await cycle()

    # req = requests.get(link, headers=headers)
    # text = req.text.split("div")
    #
    # for string in text:
    #     update = emergency_situation(string)
    #     if update not in data and update != 0:
    #         data.append(update)
    #         print(data)
    #
    # tm.sleep(5)
    #
    # await message.answer('ok')
    #
    # while GRABBING_SITE:
    #
    #     req = requests.get(link, headers=headers)
    #     text = req.text.split("div")
    #
    #     for string in text:
    #         update = emergency_situation(string)
    #         if update not in data and update != 0:
    #             data.append(update)
    #             print(data)
    #             await send_messages(update[0], update[2])
    #
    #     tm.sleep(5)


@dp.message(Command('RE'))
async def RE(message: Message):
    global RE
    if message.chat.id != group_id:
        pass

    RE = not RE
    await send_messages('RE', RE)


@dp.message(Command('BPLAE'))
async def dev_help(message: Message):
    global BPLAE
    if message.chat.id != group_id:
        pass

    BPLAE = not BPLAE
    await send_messages('BPLAE', BPLAE)


@dp.message(Command('dev_help'))
async def dev_help(message: Message):
    if message.chat.id != group_id:
        pass

    await message.answer(show_bot_values())
    await message.answer((bot_commands_help()))


@dp.message(Command('dev_stop'))
async def dev_stop(message: Message):
    global GRABBING_SITE, RE, BPLAE
    if message.chat.id != group_id:
        pass

    await message.answer("Прекращаем собирать данные...")

    GRABBING_SITE = False
    RE = False
    BPLAE = False

    await message.answer(show_bot_values())


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())