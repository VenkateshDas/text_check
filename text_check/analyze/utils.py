import pandas as pd
from datetime import datetime
import os


def load_dataset(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df


def save_dataset(df: pd.DataFrame, output_path: str = None):
    file_name = f"outputs_{datetime.now().strftime('%H-%M-%S')}.csv"
    if os.path.exists(output_path):
        df.to_csv(os.path.join(output_path,), index=False)
    else:
        os.makedirs('output')
        df.to_csv(os.path.join(output_path, file_name), index=False)

# TODO: add logging