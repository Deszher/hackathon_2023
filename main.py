import time

import streamlit as st
from typing import Optional, List

from summarizator import Summarizator
from extract_file import extract_file
from text_to_speach import TTSProvider
from config import Config

config = Config.from_env()

tts = TTSProvider(config.yandex_tts_token)
summarizator = Summarizator()

#  логотип и название
col1, col2 = st.columns([1, 1])

with col1:
    st.header('Персональный помощник для студентов')

with col2:
    st.image("assets/happy_stud.jpg")

# Боковая панель
st.sidebar.image("assets/Text_Sum.png", width=300)
st.sidebar.title("About the project:")
st.sidebar.info(
    """
    Наше приложение - это ваш верный помощник, который позволит вам получать краткую информацию
     из статей, лекций и конспектов. Больше не нужно тратить много времени на чтение длинных 
     текстов и отмечание важных моментов. Мы сделали все возможное, чтобы вы могли быстро и 
     легко получать самое важное из учебных материалов.
    """
)

st.sidebar.info(
    """
   Сокращает текст, оставляя основные моменты
    """
)

st.sidebar.info(
    """
    Вы можете воспользоваться данным приложением для получения краткой информации
    """
)


def load_doc() -> Optional[List[str]]:
    uploaded_file = st.file_uploader(label='Выберите файл с текстом, краткое содержание которого вы хотите получить')

    if uploaded_file is None:
        return None

    chunks = []
    try:
        chunks = extract_file(uploaded_file)
        return chunks
    except Exception as err:
        print(err)
        return None


res = load_doc()
button_pres = st.button('Получить краткое содержание текста')

if 'text' not in st.session_state:
    st.session_state.text = []

# если нажата кнопка, то пауза 1 сек., запуск шариков, вывод краткого содержания
if res and button_pres:
    print(res)
    with st.spinner('Wait for it...'):
        time.sleep(1)
        text = summarizator.summarizate(res)
    st.balloons()
    st.success("Краткое содержание текста:")

    # Печатаем результат
    for num, s in enumerate(text):
        st.write(f"{num+1} тезис:")
        st.write(s)

    text_to_audio = tts.convert(tts.write_file(text[0]))
    time.sleep(1)
    st.audio(text_to_audio, format="audio/raw", start_time=0, sample_rate=None)

# streamlit run main.py

