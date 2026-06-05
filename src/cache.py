import sqlite3
import pandas as pd
import json
import logging

class KanbanCache:
    def __init__(self, db_path="kanban_local.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cards (
                    _id TEXT PRIMARY KEY,
                    name TEXT,
                    card_type TEXT,
                    lane TEXT,
                    coluna_kanban TEXT,
                    sprint TEXT,
                    createdAt TIMESTAMP,
                    dtDone TIMESTAMP,
                    estimated_days REAL,
                    actual_days REAL,
                    slippage REAL,
                    aging_days REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS resultados_monte_carlo (
                    data_simulacao TEXT,
                    contexto TEXT,
                    categoria TEXT,
                    itens_pendentes INTEGER,
                    p50 INTEGER,
                    p85 INTEGER,
                    p95 INTEGER
                )
            """)

    def upsert_cards(self, df):
        if df.empty:
            return
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql('temp_cards', conn, if_exists='replace', index=False)
            conn.execute("DELETE FROM cards WHERE _id IN (SELECT _id FROM temp_cards)")
            conn.execute("""
                INSERT INTO cards (_id, name, card_type, lane, coluna_kanban, sprint,
                                   createdAt, dtDone, estimated_days, actual_days, slippage, aging_days)
                SELECT _id, name, card_type, lane, coluna_kanban, sprint,
                       createdAt, dtDone, estimated_days, actual_days, slippage, aging_days
                FROM temp_cards
            """)
            conn.execute("DROP TABLE temp_cards")
            logging.info(f"Cache atualizado com {len(df)} cards.")

    def save_simulation_results(self, df_results):
        if df_results.empty:
            return
        with sqlite3.connect(self.db_path) as conn:
            df_results.to_sql('resultados_monte_carlo', conn, if_exists='append', index=False)

    def load_cards(self):
        return pd.read_sql("SELECT * FROM cards", sqlite3.connect(self.db_path))