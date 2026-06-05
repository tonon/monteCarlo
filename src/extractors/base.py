from abc import ABC, abstractmethod
import pandas as pd

class BaseExtractor(ABC):
    @abstractmethod
    def fetch_board_data(self) -> pd.DataFrame:
        """
        Retorna DataFrame com colunas:
        _id, name, card_type, lane, coluna_kanban, sprint,
        createdAt, dtDone, estimated_days, actual_days, slippage, aging_days
        """
        pass