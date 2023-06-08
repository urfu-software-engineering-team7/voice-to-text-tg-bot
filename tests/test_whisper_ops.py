from whisper_ops import transcribe_to_text


class TestTranscribeToText:
    def test_male_mp3(self):
        res = transcribe_to_text('./mp3_samples/Male.mp3')
        assert res == " Натратно спать, от родней камням быть, в этот век преступный, постижный, ни жить не чувствовать уделзовидный. Прошу, молчи, не смею меня будить."

    def test_female_mp3(self):
        res = transcribe_to_text('./mp3_samples/Female.mp3')
        assert res == " Камесыт не будешь, Мать-дество говорил о мне, хотя нарисовой бумаге вполне."

    def test_clean_mp3(self):
        res = transcribe_to_text('./mp3_samples/Clean.mp3')
        assert res == " Редактор субтитров А.Семкин Корректор А.Егорова"

    def test_broken_mp3(self):
        res = transcribe_to_text('./mp3_samples/Broken.mp3')
        assert res == "Audio could not be transcribed"

