#!/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import logging
import whisper_ops

from dotenv import load_dotenv
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    filters,
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    logger.critical("Bot token is not found in .env file")
    exit(1)


async def download_speech(update, context, video_note=False) -> str:
    filename = f"{update.effective_message.chat.id}_{update.message.from_user.id}{update.message.message_id}.ogg"

    if video_note is True:
        voice_file = await context.bot.get_file(update.message.video_note.file_id)
    else:
        voice_file = await context.bot.get_file(update.message.voice.file_id)

    await voice_file.download_to_drive(filename)
    return filename


async def voice_to_text(update, context) -> None:
    filename = await download_speech(update, context)

    # transcribing to text with whisper
    res = whisper_ops.transcribe_to_text(filename)
    if res is None:
        await update.message.reply_text("Could not transcribe")
        return

    if len(res) == 0:
        await update.message.reply_text("Voice message is empty")

    else:
        await update.message.reply_text(res)

    try:
        os.remove(filename)
    except Exception as e:
        logger.warning(f"Removing file {filename} caused error:\n{e}")


async def video_to_text(update, context) -> None:
    # downloading file
    filename = await download_speech(update, context, video_note=True)

    # transcribing to text with whisper
    res = whisper_ops.transcribe_to_text(filename)
    if res is None:
        await update.message.reply_text("Could not transcribe")
        return

    if len(res) == 0:
        await update.message.reply_text("Voice message is empty")

    else:
        await update.message.reply_text(res)

    try:
        os.remove(filename)
    except Exception as e:
        logger.warning(f"Removing file {filename} caused error:\n{e}")


async def help(update, context):
    await update.message.reply_text("""
            Send me any audio file and I will translate it into text
            """)


def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()

    except Exception as e:
        print(f"Error during bot initialization: {e}")
        exit(1)

    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.VOICE, voice_to_text))
    app.add_handler(MessageHandler(filters.VIDEO_NOTE, video_to_text))

    # start the bot
    app.run_polling()


if __name__ == "__main__":
    main()
