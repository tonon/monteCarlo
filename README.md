# Monte Carlo Delivery Estimator

**A data‑driven tool for product teams to forecast delivery timelines using probabilistic simulations.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 What is this?

Agile teams often struggle with inaccurate delivery estimates – either over‑optimistic or overly conservative. This tool uses **Monte Carlo simulation** on your team’s historical throughput to answer the question:

> *“Given our past delivery rate, how many days will it take to finish our current backlog with 85% or 95% confidence?”*

The result is a probabilistic forecast (e.g., “P85 = 12 days”) that helps you manage stakeholders’ expectations, reduce anxiety, and make better trade‑off decisions.

---

## ✨ Features

- **Plug‑and‑play data connectors** – Load historical data from:
  - **CSV** (generic format, sample included)
  - **Trello** (via API – optional)
  - Any other kanban tool by implementing a simple `BaseExtractor`
- **Monte Carlo engine** – Simulates thousands of possible futures based on your team’s real throughput.
- **Interactive dashboard** – Built with Streamlit to visualise:
  - Distribution of simulated completion days
  - P50, P85, P95 percentiles
  - Comparison across different backlog slices (by lane, card type, etc.)
- **SQLite cache** – Stores cards and simulation results for later analysis.
- **Portfolio‑ready** – Clean architecture, environment‑based configuration, ready to deploy.

---

## 🧠 Why Monte Carlo for product managers?

Traditional “gut‑feeling” estimates are often wrong. Monte Carlo replaces guesswork with a transparent, statistically sound method. It:

- Uses your team’s **actual historical throughput** (cards delivered per day)
- Accounts for natural variability (some days are slow, some are fast)
- Produces **confidence intervals** that stakeholders can understand
- Helps you say “no” to unrealistic deadlines with data

This is **not** a planning poker replacement – it’s a complementary tool for technical PMs who want to bring rigour into forecasting.

---

## 🛠️ Tech stack

| Layer          | Technology                                            |
|----------------|-------------------------------------------------------|
| Language       | Python 3.9+                                           |
| Simulation     | NumPy, Pandas                                         |
| Backend / CLI  | Python + SQLite (via `LocalCache`)                   |
| Dashboard      | Streamlit + Plotly                                    |
| Data connectors| CSV, Trello (optional) – easily extensible to Jira, Asana, etc. |
| Config         | `python-dotenv` + `.env`                             |
| Orchestration  | Makefile (install, run, dash, clean)                 |

---

## 📦 Installation & usage

### 1. Clone the repository
```bash
git clone https://github.com/your-username/monte-carlo-delivery-estimator.git
cd monte-carlo-delivery-estimator

## ⚙️ Configuration Details

### Environment Variables (`.env`)

| Variable | Description | Example |
|----------|-------------|---------|
| `EXTRACTOR` | Data source: `csv` or `trello` | `csv` |
| `CSV_PATH` | Path to CSV file (when using CSV extractor) | `data/sample_kanban_history.csv` |
| `TRELLO_API_KEY` | Trello API key (if using Trello) | `your_api_key` |
| `TRELLO_TOKEN` | Trello token | `your_token` |
| `TRELLO_BOARD_ID` | Trello board ID | `abc123` |

### Database Schema (SQLite)

The tool creates two tables:

**`cards`** – stores all kanban cards:
```sql
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
resultados_monte_carlo – stores simulation results:

sql
data_simulacao TEXT,
contexto TEXT,
categoria TEXT,
itens_pendentes INTEGER,
p50 INTEGER,
p85 INTEGER,
p95 INTEGER
Simulation Parameters
You can adjust the Monte Carlo engine by editing src/simulator.py:

iterations – number of simulated futures (default 10,000)

Confidence percentiles – P50, P85, P95 (hardcoded, but you can add others)

Throughput calculation – based on historical daily deliveries

Extending with New Connectors
To add a new data source (e.g., Jira, Asana):

Create a new class in src/extractors/ that inherits from BaseExtractor

Implement fetch_board_data() returning a DataFrame with the required columns

Update the .env to select your new extractor

Example skeleton:

python
from .base import BaseExtractor

class JiraExtractor(BaseExtractor):
    def __init__(self, api_token, project_key):
        self.api_token = api_token
        self.project_key = project_key

    def fetch_board_data(self):
        # call Jira API, transform to DataFrame
        return df
📊 Dashboard Preview
Below are screenshots of the Streamlit dashboard in action. (Add your own images here.)

Monte Carlo Forecast Tab
<img width="1830" height="862" alt="image" src="https://github.com/user-attachments/assets/7a8a8477-5dac-4eee-99ec-af40425090f4" />

Example: P85 trend over time and comparison bar chart.

Slippage Analysis Tab
https://docs/images/slippage_analysis.png
Example: Histogram and boxplot of estimation errors by card type.

Aging Report Tab
https://docs/images/aging_report.png
Example: Distribution of open cards by age and list of oldest cards.

Tip: Place your screenshots inside a docs/images/ folder in the repository and reference them accordingly.

Live Demo
You can also run the dashboard locally after following the installation steps:

bash
make dash
Then open http://localhost:8501 in your browser.

