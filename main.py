import os
import pandas as pd
import logging
from dotenv import load_dotenv
from src.cache import KanbanCache
from src.simulator import MonteCarloSimulator
from src.extractors.csv_extractor import CSVExtractor
from src.extractors.trello import TrelloExtractor

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_simulation(simulator, backlog_df, label, category):
    if backlog_df.empty:
        return None
    items = len(backlog_df)
    res = simulator.run(items)
    logging.info(f"{category:15} | {label:25} | itens: {items:3} | P85: {res['p85']:2} dias")
    return {
        "data_simulacao": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "contexto": label,
        "categoria": category,
        "itens_pendentes": items,
        "p50": res['p50'],
        "p85": res['p85'],
        "p95": res['p95']
    }

def main():
    # Escolhe extrator
    extractor_type = os.getenv("EXTRACTOR", "csv")
    if extractor_type == "trello":
        extractor = TrelloExtractor()
    else:
        csv_path = os.getenv("CSV_PATH", "data/sample_kanban_history.csv")
        extractor = CSVExtractor(csv_path)

    df = extractor.fetch_board_data()
    if df.empty:
        logging.error("Nenhum dado retornado.")
        return

    # Cache
    cache = KanbanCache()
    cache.upsert_cards(df)

    # Histórico (cards com dtDone) e backlog
    historico = df.dropna(subset=['dtDone']).copy()
    backlog = df[df['dtDone'].isna()].copy()

    if historico.empty:
        logging.error("Sem histórico de entregas.")
        return

    sim = MonteCarloSimulator(historico)
    resultados = []

    # Simula por lane
    for lane, group in backlog.groupby('lane'):
        if not group.empty:
            r = run_simulation(sim, group, f"Lane: {lane}", "lane")
            if r: resultados.append(r)

    # Simula por tipo
    for tipo, group in backlog.groupby('card_type'):
        if not group.empty and pd.notna(tipo):
            r = run_simulation(sim, group, f"Tipo: {tipo}", "tipo")
            if r: resultados.append(r)

    # Simula geral
    if not backlog.empty:
        r = run_simulation(sim, backlog, "Backlog Geral", "geral")
        if r: resultados.append(r)

    if resultados:
        df_res = pd.DataFrame(resultados)
        cache.save_simulation_results(df_res)
        df_res.to_csv("resultados_monte_carlo.csv", index=False)
        logging.info(f"Salvos {len(resultados)} cenários.")
    else:
        logging.warning("Nenhuma simulação gerada.")

if __name__ == "__main__":
    main()