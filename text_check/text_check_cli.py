from text_check.analyze.corrector import GrammarCorrector
from text_check.analyze.validation import validate_text, batch_validate_texts
from text_check.analyze.utils import load_dataset, save_dataset
import os
from pathlib import Path


def main(input_file_path: str = None, text: str = None):
    # TODO: add parameters dictionary
    grammar_corrector = GrammarCorrector()
    
    if input_file_path:
        df = load_dataset(input_file_path)
        df = batch_validate_texts(df, grammar_corrector)
        output_path = os.path.join(Path(__file__).parent.absolute(), "output")
        save_dataset(df, output_path)

    elif text:
        text_validator = validate_text(text, grammar_corrector)
        print("Validation result:")
        print("Input text:", text_validator.text)
        print("Has errors:", text_validator.has_errors)
        if text_validator.has_errors:
            print("Suggestion:", text_validator.suggestion)
    
    elif all([input_file_path, text]):
        raise ValueError("You can only provide either a file path or a text, not both.")
    
    else:
        raise ValueError("You must provide either a file path or a text.")


if __name__ == "__main__":
    # TODO: use Fire for CLI
    main()