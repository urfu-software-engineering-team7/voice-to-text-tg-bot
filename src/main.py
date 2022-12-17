#!/bin/env python3.9
# -*- coding: utf-8 -*-

import os
# for local files/buffers parallel cleanup

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

print(BOT_TOKEN)
