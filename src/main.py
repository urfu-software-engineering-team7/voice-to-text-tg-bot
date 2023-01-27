#!/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import logging
import whisper
# import threading
# for local files/buffers parallel cleanup

from threading import Thread
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, filters

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# main transcribing model
whisper_base_model = whisper.load_model("base")


def transcribe_to_text(filename):
    try:
        with open(filename, 'rb') as f:
            result = whisper_base_model.transcribe(f.name, fp16=False, language='ru')

    except Exception as e:
        print(e)
        return None

    return result.get("text")


def voice_to_text(update, context) -> None:
    message = update.effective_message

    # downloading file
    filename = f"{update.effective_message.chat.id}_{update.message.from_user.id}{update.message.message_id}.ogg"
    voice_file = context.bot.get_file(update.message.voice.file_id)
    voice_file.download(filename)

    # transcribing to text with whisper
    res = transcribe_to_text(filename)
    if res is None:
        message.reply_text("Could not transcribe")
        return

    if len(res) == 0:
        message.reply_text("Voice message is empty")

    else:
        message.reply_text(res)

    try:
        os.remove(filename)
    except Exception as e:
        logger.warning(f"Removing file {filename} caused error:\n{e}")


def video_to_text(update, context) -> None:
    message = update.effective_message

    message.reply_text("function video to audio translation is started")

    # downloading file
    filename = f"{update.effective_message.chat.id}_{update.message.from_user.id}{update.message.message_id}.mp4"
    voice_file = context.bot.get_file(update.message.video_note.file_id)
    voice_file.download(filename)

    # transcribing to text with whisper
    res = transcribe_to_text(filename)
    if res is None:
        message.reply_text("Could not transcribe")
        return

    if len(res) == 0:
        message.reply_text("Voice message is empty")

    else:
        message.reply_text(res)

    try:
        os.remove(filename)
    except Exception as e:
        logger.warning(f"Removing file {filename} caused error:\n{e}")
	
	
def _add_handlers(dispatcher) -> None:
    dispatcher.add_handler(MessageHandler(filters.Filters.voice, voice_to_text))
    dispatcher.add_handler(MessageHandler(filters.Filters.video_note, video_to_text))
	

def main():
    try:
        updater = Updater(BOT_TOKEN)

    except Exception as e:
        print(f"Error during bot initialization: {e}")
        exit(1)

    # handling commands/events from users
    _add_handlers(updater.dispatcher)

    # start the bot
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
