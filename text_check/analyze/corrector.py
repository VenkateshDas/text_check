from abc import ABC, abstractmethod
from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM
import torch
from typing import Dict, Any, Optional

DEFAULT_GEC_PARAMS = {
    "model_tag": "prithivida/grammar_error_correcter_v1",
    "correction_prefix": "gec: ",
    'do_sample': True,
    'max_length': 256,
    'top_k': 50,
    'temperature': 0.9,
    'top_p': 0.95,
    'num_beams': 5,
    'early_stopping': False,
    'num_return_sequences': 1,
}


class TextCorrector(ABC):
    @abstractmethod
    def correct(self, text: str):
        pass


class GrammarCorrector(TextCorrector):
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        self.params = params or DEFAULT_GEC_PARAMS
        model_tag = self.params.get('model_tag', DEFAULT_GEC_PARAMS['model_tag'])
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_tag)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_tag).to(self.device)

    def _tokenize(self, input_sentence: str) -> torch.Tensor:
        return self. tokenizer.encode(input_sentence, return_tensors='pt').to(self.device)
    
    def _generate_texts(self, input_ids: torch.Tensor) -> set:
        preds = self.model.generate(
            input_ids,
            do_sample=self.params.get('do_sample', DEFAULT_GEC_PARAMS['do_sample']),
            max_length=self.params.get('max_length', DEFAULT_GEC_PARAMS['max_length']),
            top_k=self.params.get('top_k', DEFAULT_GEC_PARAMS['top_k']),
            temperature=self.params.get('temperature', DEFAULT_GEC_PARAMS['temperature']),
            top_p=self.params.get('top_p', DEFAULT_GEC_PARAMS['top_p']),
            num_beams=self.params.get('num_beams', DEFAULT_GEC_PARAMS['num_beams']),
            early_stopping=self.params.get('early_stopping', DEFAULT_GEC_PARAMS['early_stopping']),
            num_return_sequences=self.params.get('num_return_sequences', DEFAULT_GEC_PARAMS['num_return_sequences']),
        )
        generated_texts = set()
        for pred in preds:  
            generated_texts.add(self.tokenizer.decode(pred, skip_special_tokens=True).strip())
        
        return generated_texts

    def correct(self, text: str) -> str:
        correction_prefix = self.params.get("correction_prefix", DEFAULT_GEC_PARAMS["correction_prefix"])  # "grammar: " "gec: "
        input_sentence = correction_prefix + text
        input_ids = self._tokenize(input_sentence)
        corrected_texts = self._generate_texts(input_ids)
        corrected_text = list(corrected_texts)[0]

        return corrected_text


class SpellingCorrector(TextCorrector):
    pass
