import time

import streamlit as st
from PyPDF2 import PdfReader
from docx import Document

from summarizator import Summarizator

summarizator = Summarizator()

#  логотип и название
col1, col2 = st.columns([1, 1])

with col1:
    st.header('Персональный помощник для студентов')

with col2:
    st.image("happy_stud.jpg")

# Боковая панель
st.sidebar.image("Text_Sum.png", width=300)
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


# Считываем текст из PDF-файла
def read_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


# Считываем текст из Word-документа
def read_word(file_path):
    document = Document(file_path)
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs)


def load_doc():
    uploaded_file = st.file_uploader(label='Выберите файл с текстом, краткое содержание которого вы хотите получить')
    if uploaded_file is not None:
        # Проверяем формат файла
        if uploaded_file.name.endswith('.pdf'):
            # Считываем текст из PDF-файла
            text = read_pdf(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            # Считываем текст из Word-документа
            text = read_word(uploaded_file)
        else:
            print("Error: Unsupported file format")

        # Проверяем длину текста
        if len(text) < 30:
            print("Error: Input text is too short")
        else:
            ## Разделяем текст на фрагменты максимальной длины последовательности
            chunk_size = 512
            chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

            return chunks

    else:
        return None


res = load_doc()
button_pres = st.button('Получить краткое содержание текста')

# если нажата кнопка, то пауза 1 сек., запуск шариков, вывод краткого содержания
if res and button_pres:
    with st.spinner('Wait for it...'):
        time.sleep(1)
        text = summarizator.summarizate(res)
    st.balloons()
    st.success("Краткое содержание текста:")

    # Печатаем результат
    for num, s in enumerate(text):
        st.write(f"{num+1} тезис:")
        st.write(s)

# streamlit run main.py

