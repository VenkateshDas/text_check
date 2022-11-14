from fastapi import FastAPI
from text_check.analyze.validation import validate_text, TextValidation
from text_check.analyze.corrector import GrammarCorrector
from pydantic import BaseModel

app = FastAPI()

gc = GrammarCorrector()


class Request(BaseModel):
    input_sentence: str


@app.get("/")
def read_root():
    return {"health": "Alive"}

@app.post("/correct")
def get_correction(data: Request) -> TextValidation:
    validated_text = validate_text(data.input_sentence, gc)
    return validated_text
