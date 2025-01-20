import os
from aiogram import Dispatcher, Bot
from aiogram.types import File, InlineQuery, Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
import requests
import asyncio

bot: Bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
dp: Dispatcher = Dispatcher()


async def file_check(msg: Message):
    if msg.video:
        return msg.video.file_id
    if msg.photo:
        return msg.photo[-1].file_id
    if msg.document:
        return msg.document.file_id
    if msg.audio:
        return msg.audio.file_id
    return None


@dp.message(Command(commands=["start", "help"]))
async def start_help_command(msg: Message) -> None:
    await msg.reply(
        "This bot is made as a telegram interface for temp.sh . Convenient for use in groups. To upload a file and retrieve a temporary URL, reply to a message that holds your desired file with the /wrap command. Source code: https://github.com/fobbidennotis/temp-sh-bot"
    )


@dp.message(Command("wrap"))
async def wrap_command(msg: Message) -> None:
    if not msg.reply_to_message:
        await msg.reply("You have to reply to a message")
        return

    file_id = await file_check(msg.reply_to_message)

    if file_id == None:
        await msg.reply("Ensure your message holds a file")
        return

    try:
        file: File = await bot.get_file(file_id)
    except TelegramBadRequest:
        await msg.reply("Sadly, this bot can only upload files up to 20MB in size")
        return

    bio = await bot.download(file)

    res = requests.post("https://temp.sh/upload", files={"file": bio})

    await msg.reply(res.text)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
