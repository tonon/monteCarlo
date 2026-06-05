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
