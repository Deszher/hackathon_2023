import os
import subprocess
import time

import requests

from creds import token

# https://yandex.ru/video/preview/13029480301595259351

root_path = os.path.dirname(__file__)
target_path = ""

"""
token убрать
"""


def synthesize(text):
    url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
    headers = {"Authorization": "Api-Key " + token, }

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


def convert(filename):
    """
    Для конверсии в wav
    :param filename:
    :return:
    """
    # # собираю команду конвертации
    cmd = " ".join([
        root_path + "\\sox\\sox.exe",
        "-r 48000 -b 16 -e signed-integer -c 1",
        target_path + filename + ".raw",
        target_path + filename + ".wav"
    ])

    # выполняю команду конвертации
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    return f"{target_path + filename}.wav"