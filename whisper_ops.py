import whisper
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


base_model = whisper.load_model("base")


# def transcribe_to_text(file):
    # result = base_model.transcribe(file.name, fp16=False, language='ru')
    # transcribed_text = result.get("text")

    # if transcribed_text is None:
        # return "Audio could not be transcribed"

    # if len(transcribed_text) == 0:
        # return "Audio is emtpy"

    # return transcribed_text


def transcribe_to_text(filename):
    try:
        with open(filename, 'rb') as f:
            result = base_model.transcribe(f.name, fp16=False, language='ru')

    except Exception as e:
        logger.error(e)
        return "Audio could not be transcribed"

    text = result.get("text")
    if text is not None:
        return text

    return "Audio is empty"

