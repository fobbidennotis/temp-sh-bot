import os
from aiogram import F, Dispatcher, Bot
from aiogram.types import ContentType, File, Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
import requests
import asyncio
from aiohttp import ClientSession


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


async def download_and_upload_file(msg, bot: Bot) -> str:
    file_id = await file_check(msg)

    if file_id is None:
        return "Ensure your message holds a file"

    try:
        file: File = await bot.get_file(file_id)
    except TelegramBadRequest:
        return "Sadly, this bot can only upload media up to 20MB"

    res = requests.post(
        "https://temp.sh/upload", files={"file": open(file.file_path, "rb")},
        timeout=1000,
    )

    return res.text


@dp.message(Command(commands=["start", "help"]))
async def start_help_command(msg: Message) -> None:
    await msg.reply(
        "This bot is made as a Telegram interface for temp.sh. Convenient for use in groups. To upload a file and retrieve a temporary URL, reply to a message that holds your desired file with the /wrap command. Source code: https://github.com/fobbidennotis/temp-sh-bot"
    )


@dp.message(F.content_type == ContentType.VIDEO)
@dp.message(F.content_type == ContentType.PHOTO)
@dp.message(F.content_type == ContentType.DOCUMENT)
@dp.message(F.content_type == ContentType.AUDIO)
async def handle_sent_file(msg: Message, bot: Bot) -> None:
    await msg.reply(await download_and_upload_file(msg, bot))


@dp.message(Command("wrap"))
async def wrap_command(msg: Message, bot: Bot) -> None:
    if not msg.reply_to_message:
        await msg.reply("You have to reply to a message")
        return

    await msg.reply(await download_and_upload_file(msg.reply_to_message, bot))


async def main() -> None:
    from aiogram.client.session.aiohttp import AiohttpSession
    from aiogram.client.telegram import TelegramAPIServer

    session = AiohttpSession(
        api=TelegramAPIServer.from_base('http://localhost:8081')
    )
    bot = Bot(os.environ["TELEGRAM_BOT_TOKEN"], session=session)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
