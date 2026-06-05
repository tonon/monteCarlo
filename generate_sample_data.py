import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

start = datetime(2025, 12, 1)
end = datetime(2026, 5, 31)
today = datetime(2026, 6, 3)

card_types = ['Bug', 'Feature', 'Tech Debt', 'Ops']
lanes = ['Backlog', 'Desenvolvimento', 'Code Review', 'Homologação', 'Done']
sprints = [f'Sprint {i}' for i in range(10, 19)]
cards = []
counter = 1

# Cards concluídos
for _ in range(150):
    created = start + timedelta(days=random.randint(0, (end - start).days))
    cycle = max(1, int(np.random.gamma(2, 2)))
    done = min(created + timedelta(days=cycle), end)
    card_type = random.choice(card_types)
    estimated = max(1, int(cycle * random.uniform(0.7, 1.3)))
    actual = cycle
    slippage = actual - estimated

    cards.append({
        '_id': f'CARD-{counter:03d}',
        'name': f'{card_type} task {counter}',
        'card_type': card_type,
        'lane': 'Done',
        'coluna_kanban': 'Done',
        'sprint': random.choice(sprints),
        'createdAt': created.strftime('%Y-%m-%d'),
        'dtDone': done.strftime('%Y-%m-%d'),
        'estimated_days': estimated,
        'actual_days': actual,
        'slippage': slippage,
        'aging_days': ''
    })
    counter += 1

# Cards abertos
for _ in range(50):
    created = start + timedelta(days=random.randint(0, (today - start).days))
    aging = (today - created).days
    aging = max(1, aging)
    card_type = random.choice(card_types)
    lane = random.choice(['Desenvolvimento', 'Code Review', 'Homologação', 'Backlog'])
    estimated = random.randint(2, 15)

    cards.append({
        '_id': f'CARD-{counter:03d}',
        'name': f'{card_type} task {counter}',
        'card_type': card_type,
        'lane': lane,
        'coluna_kanban': lane,
        'sprint': random.choice(sprints),
        'createdAt': created.strftime('%Y-%m-%d'),
        'dtDone': '',
        'estimated_days': estimated,
        'actual_days': '',
        'slippage': '',
        'aging_days': aging
    })
    counter += 1

df = pd.DataFrame(cards)
df.to_csv("data/sample_kanban_history.csv", index=False, encoding='utf-8-sig')
print(f"Arquivo gerado: data/sample_kanban_history.csv com {len(df)} cards.")