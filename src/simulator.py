import numpy as np
import pandas as pd

class MonteCarloSimulator:
    def __init__(self, historical_df):
        if historical_df.empty:
            self.throughput = np.array([1])
            return
        # Agrupa entregas por dia
        entregas = historical_df.groupby(pd.to_datetime(historical_df['dtDone']).dt.date).size()
        datas = pd.date_range(entregas.index.min(), entregas.index.max()).date
        self.throughput = entregas.reindex(datas, fill_value=0).values

    def run(self, backlog_size, iterations=10000):
        if backlog_size <= 0:
            return {'p50': 0, 'p85': 0, 'p95': 0}
        samples = []
        for _ in range(iterations):
            days = 0
            delivered = 0
            while delivered < backlog_size:
                delivered += np.random.choice(self.throughput)
                days += 1
            samples.append(days)
        return {
            'p50': int(np.percentile(samples, 50)),
            'p85': int(np.percentile(samples, 85)),
            'p95': int(np.percentile(samples, 95)),
            'max': int(np.max(samples)),
            'min': int(np.min(samples))
        }