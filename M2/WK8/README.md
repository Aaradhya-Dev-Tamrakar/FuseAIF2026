# fuseAiF_wk8_sp500_forecasting

**Week 8 — Forecasting: Classical to Modern Forecasters**
Fusemachines AI Fellowship 2026 · Aaradhya Dev Tamrakar

## Dataset
Monthly S&P 500 Index, 1990–2024 (420 months), via `yfinance`. Network access
to Yahoo Finance was blocked in the execution sandbox; the notebook falls back
to a synthetic lognormal-walk series (seeded, with an injected −34% single-month
shock mirroring the March 2020 COVID crash) so the full pipeline — data prep
through investment memo — runs end-to-end. See the Q1 cell in
`W8_Forecasting_Assignment.ipynb` for the fallback logic.

## Submission date
June 27, 2026

## Contents
- `W8_Forecasting_Assignment.ipynb` — fully executed notebook, all 23 questions
- `wk8_forecasting.pdf` — PDF export of the executed notebook
- `assignment/sp500_sarima_v1.pkl` — fitted SARIMAX model, required deliverable
- `requirements.txt` — pinned dependency versions
- `plots/` — 12 saved figures (ACF/PACF, SARIMA diagnostics, SARIMA forecast
  + CI, Prophet components, LightGBM feature importance and prediction
  intervals, MASE comparison, error-by-month, error-by-horizon)
- `misc/discussion_answers.md` — all 8 discussion questions
- `misc/ai_prompt_logs.md` — 5 AI-prompt critique entries

## Key results

| Model | MASE | RMSE |
|---|---|---|
| Holt-Winters | 2.6556 | 110.4 |
| SARIMA(1,1,1)(0,1,1,12) | 2.6971 | 112.4 |
| LSTM | ~2.78 | ~110 |
| XGBoost (recursive) | 3.9659 | 146.8 |
| Naive (baseline) | 4.0561 | 150.2 |
| Seasonal-Naive | 5.2462 | 189.3 |
| LightGBM (recursive) | 6.2266 | 217.9 |
| Prophet | 7.8203 | 307.5 |
| MLP | 24.4701 | 986.9 |
| **4-model Ensemble** (Holt-Winters + SARIMA + LSTM + XGBoost) | **2.44** | 96.7 |

**Diebold-Mariano test** (ensemble vs best single model): p = 0.0092 —
statistically significant improvement at the 5% level.

**Recommendation:** Deploy the 4-model ensemble for production accuracy, with
Holt-Winters retained as an interpretable, low-latency fallback for regulatory
contexts. Full reasoning in Q23 of the notebook.

## Known follow-up
SARIMA residuals fail Ljung-Box at the seasonal lags (12, 24); see
`misc/discussion_answers.md` Discussion Q3 for the diagnosed fix
(increase seasonal MA/AR order) — not yet refit in this submission cycle.

## Setup
```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace W8_Forecasting_Assignment.ipynb
```
