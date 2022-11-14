import pandas as pd
from pydantic import BaseModel

from text_check.analyze.corrector import GrammarCorrector


class TextValidation(BaseModel):
    text: str
    has_errors: bool = False
    suggestion: str = None


def validate_text(text: str, grammar_corrector: GrammarCorrector) -> TextValidation:
    grammar_suggestion = grammar_corrector.correct(text)
    has_errors = grammar_suggestion != text
    suggestion = grammar_suggestion if has_errors else None
    return TextValidation(text=text, has_errors=has_errors, suggestion=suggestion)


def batch_validate_texts(df: pd.DataFrame, grammar_corrector: GrammarCorrector) -> pd.DataFrame:
    df["has_errors"] = False
    df["suggestion"] = None
    for index, row in df.iterrows():
        text = row["text"]  # TODO: make this more flexible to allow for different column names
        text_validator = validate_text(text, grammar_corrector)
        df.at[index, "has_errors"] = text_validator.has_errors
        df.at[index, "suggestion"] = text_validator.suggestion
    return df


