#!/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import logging
# for local files/buffers parallel cleanup

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def unknown_text(update, context) -> None:
    update.message.reply_text("Unknown command type /help to get a list of available commands")


def error(update, context) -> None:
    logger.warning(f"Update {update} caused error {context.error}")


def _add_handlers(dispatcher) -> None:
    dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
    dispatcher.add_error_handler(error)


def main():
    try:
        updater = Updater(BOT_TOKEN)
    except Exception as e:
        print(e)
        exit(1)

    # _add_handlers line is essenstial for command handling
    _add_handlers(updater.dispatcher)

    # Start the Bot
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    updater.idle()


if __name__ == "__main__":
    main()

