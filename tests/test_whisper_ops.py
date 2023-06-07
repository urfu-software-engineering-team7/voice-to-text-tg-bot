# from  import *
from whisper_ops import transcribe_to_text


class TestTranscribeToText:
    def test_male_mp3(self):
        with open('Male.mp3', 'r') as f:
            res = transcribe_to_text(f)

        assert res == " Натратно спать, от родней камням быть, в этот век преступный, постижный, ни жить не чувствовать уделзовидный. Прошу, молчи, не смею меня будить."

    def test_female_mp3(self):
        with open('Female.mp3', 'r') as f:
            res = transcribe_to_text(f)

        assert res == " Камесыт не будешь, Мать-дество говорил о мне, хотя нарисовой бумаге вполне."

    def test_clean_mp3(self):
        with open('Clean.mp3', 'r') as f:
            res = transcribe_to_text(f)

        assert res == "Audio is emtpy"

    def test_broken_mp3(self):
        with open('Broken.mp3', 'r') as f:
            res = transcribe_to_text(f)

        assert res == "Found error in work with wisper"
