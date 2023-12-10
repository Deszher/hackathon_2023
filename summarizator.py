from transformers import T5TokenizerFast, T5ForConditionalGeneration
from typing import List


# https://huggingface.co/d0rj/rut5-base-summ
class Summarizator:
    _tokenizer: T5TokenizerFast
    _model: T5ForConditionalGeneration

    PRETRAINED_MODEL_NAME = "d0rj/rut5-base-summ"

    def __init__(self):
        self._tokenizer = T5TokenizerFast.from_pretrained(self.PRETRAINED_MODEL_NAME)
        self._model = T5ForConditionalGeneration.from_pretrained(self.PRETRAINED_MODEL_NAME)

    def summarizate(self, input: List[str]) -> List[str]:
        summaries = []
        for chunk in input:
            encoded_input = self._tokenizer.encode(chunk, return_tensors='pt')
            result = self._model.generate(encoded_input, max_length=96, min_length=30, do_sample=False)
            summary = self._tokenizer.decode(result[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
            summaries.append(summary)

        return summaries
