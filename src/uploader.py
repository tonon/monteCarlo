import pandas as pd
import os
from datetime import datetime
import logging

class CSVUploader:
    def __init__(self, filename="monte_carlo_history.csv"):
        self.filename = filename

    def save_results(self, stats, backlog_info, context="Geral"):
        """
        stats: dicionário vindo do MonteCarloSimulator
        backlog_info: pode ser um int (total) ou dict (detalhado)
        """
        # Se o backlog_info for um dicionário, transformamos em string para o CSV
        items_summary = str(backlog_info) if isinstance(backlog_info, dict) else backlog_info
        
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "contexto": context,
            "backlog_items": items_summary,
            "p50_days": stats.get('p50'),
            "p85_days": stats.get('p85'),
            "p95_days": stats.get('p95'),
            "max_days": stats.get('max'), # Adicionado para ver o pior cenário
            "min_days": stats.get('min')  # Adicionado para ver o melhor cenário
        }
        
        df_new = pd.DataFrame([nova_linha])

        try:
            # Verifica se o arquivo existe para decidir se escreve o cabeçalho (header)
            file_exists = os.path.isfile(self.filename)
            
            df_new.to_csv(
                self.filename, 
                mode='a', 
                index=False, 
                header=not file_exists, 
                encoding='utf-8-sig' # Melhora compatibilidade com Excel
            )
            logging.info(f"📊 Resultados salvos com sucesso em {self.filename}")
        except Exception as e:
            logging.error(f"❌ Erro ao salvar CSV: {e}")