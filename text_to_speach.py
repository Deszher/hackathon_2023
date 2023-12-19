import os
import time

import requests

# https://yandex.ru/video/preview/13029480301595259351

root_path = os.path.dirname(__file__)
target_path = ""


class TTSProvider:
    token: str

    def __init__(self, token: str):
        self.token = token

    def synthesize(self, text):
        url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
        headers = {"Authorization": "Api-Key " + self.token, }

        data = {
            "text": text,
            "lang": "ru-RU",
            "voice": "jane",
            "emotion": "good",
            "speed": "1.1",
            "format": "lpcm",
            "sampleRateHertz": 48000,
        }

        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RecursionError(f"Invalid response received: code: {resp.status_code}, message: {resp.text},")

            for chunk in resp.iter_content(chunk_size=None):
                yield chunk

    @staticmethod
    def write_file(text):
        """
        Пишет чанки в файл
        :param text:
        :return:
        """

        filename = str(int(time.time()))
        with open(filename + ".raw", "wb") as f:
            for audio_content in synthesize(text):
                f.write(audio_content)

        time.sleep(2)

        return filename

    @staticmethod
    def convert(filename):
        """
        Для конверсии в wav
        :param filename:
        :return:
        """

        with open(target_path + filename + ".raw", "rb") as inp_f:
            data = inp_f.read()
            with wave.open(target_path + filename + ".wav", "wb") as out_f:
                out_f.setnchannels(1)
                out_f.setsampwidth(2)  # number of bytes
                out_f.setframerate(48000)
                out_f.writeframesraw(data)
        return f"{target_path + filename}.wav"
