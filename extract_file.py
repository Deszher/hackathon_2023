from pypdf import PdfReader
from docx import Document
import io
from typing import List


# Считываем текст из PDF-файла
def read_pdf(file: io.BytesIO) -> str:
    reader = PdfReader(file)
    content = ''
    for page in reader.pages:
        content += page.extract_text()
    return content


# Считываем текст из Word-документа
def read_word(file: io.BytesIO) -> str:
    document = Document(file)
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs)


def read_txt(file: io.BytesIO) -> str:
    return file.read().decode()


def extract_file(file: io.BytesIO) -> List[str]:
    # Проверяем формат файла
    if file.name.endswith('.pdf'):
        # Считываем текст из PDF-файла
        text_str = read_pdf(file)
    elif file.name.endswith('.docx'):
        # Считываем текст из Word-документа
        text_str = read_word(file)
    elif file.name.endswith('.txt'):
        # Считываем текст из Word-документа
        text_str = read_txt(file)
    else:
        raise ValueError("Error: Unsupported file format")

    # Проверяем длину текста
    if len(text_str) < 30:
        raise ValueError("Error: Input text is too short")

    # Разделяем текст на фрагменты максимальной длины последовательности
    chunk_size = 512
    chunks = [text_str[i:i + chunk_size] for i in range(0, len(text_str), chunk_size)]

    return chunks
