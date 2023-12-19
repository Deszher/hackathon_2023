import os

from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Self


@dataclass()
class Config(dict):
    yandex_tts_token: str

    @classmethod
    def from_env(cls) -> Self:
        load_dotenv()

        return cls(
            yandex_tts_token=os.getenv("YANDEX_TTS_TOKEN"),
        )
