#!/bin/env python3.9
# -*- coding: utf-8 -*-

import os
import logging
# for local files/buffers parallel cleanup

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters
from telegram.constants import MAX_MESSAGE_LENGTH

UPLOAD_LIMIT = 58

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def split_long_message(text: str) -> List[str]:
    length = len(text)
    if length < MAX_MESSAGE_LENGTH:
        return [text]

    results = []
    for i in range(0, length, MAX_MESSAGE_LENGTH):
        results.append(text[i:MAX_MESSAGE_LENGTH])

    return results


def download_and_prep(file_name: str, message: Message) -> None:
    message.voice.get_file().download(file_name)
    message.reply_chat_action(action=ChatAction.TYPING)


# TODO: this funciton must be rewritten to work with whisper <17-12-22, modernpacifist> #
def transcribe(file_name: str, message: Message, lang_code: str = 'ru-RU', alternatives: List[str] = ['en-US', 'uk-UA']) -> List[str]:
    media_info = MediaInfo.parse(file_name)
    if len(media_info.audio_tracks) != 1 or not hasattr(media_info.audio_tracks[0], 'sampling_rate'):
        os.remove(file_name)
        raise ValueError('Failed to detect sample rate')
    actual_duration = round(media_info.audio_tracks[0].duration / 1000)

    sample_rate = media_info.audio_tracks[0].sampling_rate
    encoding = RecognitionConfig.AudioEncoding.OGG_OPUS
    if sample_rate not in SUPPORTED_SAMPLE_RATES:
        message.reply_text('Your voice message has a sample rate of {} Hz which is not in the list '
                           'of supported sample rates ({}).\n\nI will try to resample it, '
                           'but this may reduce recognition accuracy'
                           .format(sample_rate,
                                   ', '.join(str(int(rate / 1000)) + ' kHz' for rate in SUPPORTED_SAMPLE_RATES)
                                   ),
                           quote=True)
        message.reply_chat_action(action=ChatAction.TYPING)
        encoding, file_name, sample_rate = resample(file_name)
    config = RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate,
        enable_automatic_punctuation=True,
        language_code=lang_code,
        alternative_language_codes=alternatives,
    )

    try:
        response = upload_to_gs(file_name, config) \
            if actual_duration > UPLOAD_LIMIT \
            else regular_upload(file_name, config)
    except Exception as e:
        print(e)
        os.remove(file_name)
        return ['Failed']

    with conn.cursor() as cur:
        cur.execute("insert into customer(user_id) values (%s) on conflict (user_id) do nothing;",
                    (message.chat_id,))
        cur.execute("update customer set balance = balance - (%s) where user_id = (%s);",
                    (actual_duration, message.chat_id))
        cur.execute("insert into stat(user_id, message_timestamp, duration) values (%s, current_timestamp, %s);",
                    (message.chat_id, actual_duration))
        conn.commit()

    os.remove(file_name)

    message_text = ''
    for result in response.results:
        message_text += result.alternatives[0].transcript + '\n'

    return split_long_message(message_text)


def voice_to_text(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    # if message.voice.duration > MY_NERVES_LIMIT:
        # message.reply_text(POLITE_RESPONSE, quote=True)
        # return

    chat_id = update.effective_message.chat.id
    file_name = '%s_%s%s.ogg' % (chat_id, update.message.from_user.id, update.message.message_id)
    download_and_prep(file_name, message)

    transcriptions = transcribe(file_name, update.message)

    if len(transcriptions) == 0 or transcriptions[0] == '':
        message.reply_text('Transcription results are empty. You can try setting language manually by '
                           'replying to the voice message with the language code like ru-RU or en-US',
                           quote=True)
        return

    for transcription in transcriptions:
        message.reply_text(transcription, quote=True)


def unknown_text(update, context) -> None:
    update.message.reply_text("Unknown command type /help to get a list of available commands")


def error(update, context) -> None:
    logger.warning(f"Update {update} caused error {context.error}")


def _add_handlers(dispatcher) -> None:
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_to_text))
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

