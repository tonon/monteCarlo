import pandas as pd
from .base import BaseExtractor

class CSVExtractor(BaseExtractor):
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def fetch_board_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path)
        # converte colunas de data
        for col in ['createdAt', 'dtDone', 'updatedAt']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df