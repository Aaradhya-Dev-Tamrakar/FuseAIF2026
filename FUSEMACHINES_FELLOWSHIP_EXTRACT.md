# Fusemachines AI Fellowship 2026 — Extracted Data

***Source: AARADHYA_MASTER_v137.md · Updated July 9, 2026***

This extract also applies to the workspace repository FuseAIF2026, which functions as the organization-level archive for the fellowship work. Each assignment is typically maintained in a separate private repository, while this repo stores the weekly notes, extracted summaries, references, and organizational materials that tie the work together.

Full archive repository: <https://github.com/Aaradhya-Dev-Tamrakar/FuseAIF2026>

---

## 1. Program Facts

| Field | Value |
| --- | --- | --- |
| Program | Fusemachines AI Fellowship 2026 |
| Role | Fuse AI Fellow |
| Duration | 24 weeks (6 months) |
| Start | May 4, 2026 (Wk1 Monday) |
| End | Oct 18, 2026 (Sunday) |
| Cadence | Mon–Sun weekly cycle, flips every Monday 00:00 NPT |
| Current status (as of current date, July 9, 2026) | **Wk 10/24, ongoing** |
| Week formula | `floor((today − May 4 2026) / 7) + 1`, capped at 24 |
| Facilitator | **Season** |
| WK8 lecture presenter | Susan Ghimire |
| Admission | Passed entrance exam (March 2026): linear algebra, calculus, probability, Python, ML |
| Submission channel | Google Classroom (AI Fellowship 2026) |

**Status label convention (do not misread):** "Wks N complete" ≠ program finished. Do not infer "complete" before Oct 18, 2026.

---

## 2. Week-by-Week Deliverables

### Repository Context — FuseAIF2026

- This repository is not the primary coding home for each fellowship assignment; it is the organizational archive and reference hub.
- The separate private repos hold the main implementation work, notebooks, and submission artifacts for each week.
- FuseAIF2026 keeps the extracted notes, summaries, assignment index, and supporting documentation for the broader fellowship journey.

### Week 2 — Customer REST API *(no standalone project entry; CV bullet only)*

- Containerized customer REST API: FastAPI + PostgreSQL + Docker, 4-layer architecture, asyncio concurrency.
- **Instructor feedback (week unconfirmed, likely Wk 2/3/4):** monolithic single-file API structure flagged — declutter into subfolders, use separate `APIRouter` per domain (e.g. `routers/auth.py`, `routers/query.py`, `routers/results.py`) instead of flat root.
  - **Apply-forward rule:** all new FastAPI projects (fellowship or Nexus) must use `APIRouter` per domain from day one. No monolithic `main.py`. Minimum structure: `app/routers/`, `app/models/`, `app/db/`, `app/core/`.
  - Status: ⏳ not yet retroactively applied.

### Week 3 — Text-to-SQL Agentic Pipeline *(Completed — Rating 8.7/10)*

- **Stack:** Python · FastAPI · Streamlit · PostgreSQL · Docker · OpenAI API · Prompt Chaining
- Production-grade Text-to-SQL pipeline + state-based FastAPI SQL Agent over `classicmodels` PostgreSQL DB.
- Modular workflow: Planner → Generator → Validator → Executor → Summarizer, self-correction up to 3 retries.
- GPT-4o-mini prompt-chaining, rule-based SQL safety validation (blocks DML/DDL), structured JSON query logging.
- **100.0% execution success, 100.0% result accuracy** on 50-question benchmark, zero retries required.
- Streamlit chat interface, Docker/Docker Compose containerized.
- Repo: `AaradhyaDT/fuseAiF_wk3_text2sql`

### Week 4 — Telco Customer Churn & CLV ML Pipeline *(Completed — Rating 8.5/10)*

- **Stack:** Python · Scikit-learn · Pandas · NumPy · Matplotlib · Seaborn · Papermill
- End-to-end classification + regression pipeline for churn and CLV.
- Stratified 70/15/15 split; Logistic Regression / Ridge / SGD classifiers benchmarked.
- Custom threshold 0.385 → top-200 high-risk budget segment.
- Ridge Regression best for CLV (mean CLV $1,304.70); Lasso L1 paths plotted.
- Stratified 5-fold CV: ROC-AUC 0.841 ± 0.005; learning curves + leakage simulation.
- Papermill automation, full HTML report export, Graphify knowledge-graph integration.
- Repo: `AaradhyaDT/FUSE_AIF_2026_M1` (under `WK4/`)

### Week 5 — Telco Churn Tree-Based Ensemble Pipeline *(Completed — Rating 9.0/10, highest fellowship score)*

- **Stack:** Python · Scikit-learn · XGBoost · imbalanced-learn · SHAP · Joblib · Matplotlib
- Dataset: Telco Customer Churn, 7,043 rows, ~27% positive rate.
- Random Forest + XGBoost vs. naïve baseline; AUROC/Precision/Recall/F1 (accuracy trap exposed).
- `ColumnTransformer` for mixed dtypes; `ImbPipeline` (imbalanced-learn) restricts SMOTE to training folds — zero leakage.
- Grid Search / Bayesian optimization on XGBoost hyperparameters.
- SHAP global summary (Q15) + local waterfall/force plot (Q16); 2-sentence retention recommendation.
- Production serialization: full pipeline saved via `joblib` → `telco_churn_pipeline_v1.joblib`.
- Secondary regression task: `tenure` prediction — dropped `TotalCharges` (leakage column); unconstrained Decision Tree vs. regularized XGBoost Regressor; 5-fold CV learning curves show overfitting in baseline vs. generalization in XGBoost; extrapolation-bound check on tree predictions.
- Model Card (Q18) completed with real metrics.
- Repo: `AaradhyaDT/fuseAiF_wk5_telco_churn_ensembles`

### Fellowship Prep Toolkit *(Completed, Rating 6.5/10 — supplementary, not a numbered week)*

- 50-question mock exam widget + 7-tab interactive HTML cheatsheet (linear algebra, calculus, probability, Python/CS, ML).

### Week 6 — Probabilistic Models Assignment *(Completed — Rating 8.2/10)*

- **Stack:** Python · PyMC · ArviZ · pgmpy · scikit-learn · Pandas · Matplotlib · Seaborn
- Repo structure: `W6_Probabilistic_Models_Assignment.ipynb`, `W6_TaskPlan.md`, `TASK_PROGRESS.md`, `W6_Probabilistic_Models_Resource_Guide.pdf`.
- Deliverables: Bayesian estimation (MLE/MAP/full Bayes), sequential updating, Dirichlet-multinomial inference, multivariate Gaussian conditioning, probabilistic graphical models, Gaussian process regression, PyMC Bayesian logistic regression.
- Artifact: `telco_bayes_lr_v1.pkl` (Bayesian logistic regression trace).
- Portfolio entry: live on `aaradhyadtmr.github.io`.

### Week 7 — Clustering / Customer Segmentation Assignment *(Completed June 12, 2026 — Rating 8.0/10)*

- **Stack:** Python · scikit-learn · scipy · Pandas · NumPy · Matplotlib · Seaborn · NearestNeighbors
- **Dataset:** UCI Online Retail II (~500,000 transactions, `Year 2010-2011` sheet)
- **Repo:** `AaradhyaDT/fuseAiF_wk7_customer_segmentation`
- Context: market segmentation from raw unlabeled transaction data.
- Pipeline: RFM feature engineering + extended features (AvgBasketSize, AvgDaysBetweenPurchases, UniqueProducts, ReturnRate) + category spend ratios (keyword-bucketed `Description` → ≥5 categories) → outlier detection (IQR vs Z-score) → scaler choice (StandardScaler vs RobustScaler) → K-Means (Elbow + Silhouette, k-means++ vs random init) → Hierarchical (Ward/Complete/Average/Single dendrograms; fit Ward + Complete) → DBSCAN (k-distance ε estimation, ≥3 param combos, noise analysis) → validation (Silhouette / Davies-Bouldin / Calinski-Harabasz) → business narrative + executive summary → failure log (≥3 entries).
- Status: notebook executed end-to-end (S0–S9), submitted as `Week_7_Clustering_Assignment_executed.ipynb`. Repo organized: root has notebook/PDF/plots/README/LICENSE/.gitignore (raw `.xlsx` gitignored); dev artifacts archived under `misc/`.
- Submission: due June 21, 2026, via Google Classroom.
- Portfolio: live in `projects.html` (v113).

### Week 8 — Forecasting Assignment *(Completed June 27, 2026 — Rating 8.1/10)*

- **Stack:** Python · statsmodels (SARIMA/SARIMAX, Holt-Winters) · Prophet · LightGBM · TensorFlow/Keras (LSTM) · XGBoost · scikit-learn · Pandas · NumPy · Matplotlib
- **Dataset:** Monthly S&P 500 Index, 1990–2024 (420 months), nominally via `yfinance`
- **Repo:** `AaradhyaDT/fuseAiF_wk8_sp500_forecasting`
- Context: classical-to-modern forecasting comparison — 9 forecasters, then test whether an ensemble beats the best single model.
- **Sandbox constraint:** yfinance network access blocked in execution environment → seeded synthetic lognormal-walk fallback with injected −34% single-month shock (mirrors March 2020 COVID crash); fallback logic documented in Q1 cell.
- Pipeline: data prep + missing-data strategy comparison → ACF/PACF diagnostics (log returns, differenced log) → SARIMA(1,1,1)(0,1,1,12) with residual diagnostics → Holt-Winters → Prophet (component decomposition) → LightGBM (recursive, feature importance + prediction intervals) → LSTM → XGBoost (recursive) → naive/seasonal-naive baselines → MASE/RMSE comparison → error breakdowns by calendar-month and horizon → 4-model ensemble (Holt-Winters + SARIMA + LSTM + XGBoost) → Diebold-Mariano significance test → investment-memo recommendation.
- **Results:** Ensemble best overall — **MASE 2.44 / RMSE 96.7**, ahead of Holt-Winters (2.66/110.4) and SARIMA (2.70/112.4). Diebold-Mariano **p = 0.0092** (significant at 5%). Naive baseline MASE 4.06. Prophet (7.82) and MLP (24.47) worst on this series.
- Recommendation: deploy 4-model ensemble for production accuracy; keep Holt-Winters as interpretable low-latency fallback for regulatory contexts.
- **Known unresolved issue:** SARIMA residuals fail Ljung-Box at seasonal lags (12, 24) — diagnosed fix is increasing seasonal MA/AR order; not refit this cycle.
- Status: notebook executed end-to-end, 23 questions complete, 8 discussion questions answered, 5 AI-prompt critique entries logged. Repo organized: root has executed notebook/PDF/`assignment/sp500_sarima_v1.pkl`/`plots/` (12 figures)/README/LICENSE/.gitignore; dev tools under `tools/`, task docs under `docs/`, discussion logs under `misc/`.
- Submitted June 27, 2026, via Google Classroom.
- **Portfolio: NOT yet added to `projects.html` — pending trigger.**

**WK8 Class Lecture Notes** *(Complete — June 28, 2026, 17:12–19:00 NPT, presenter Susan Ghimire)*
Full notes archived separately: `PATCH_fuseWk8_forecasting_lecture_20260628_v2.md`
Topics (slides 22–69): time series ordering & lag (NLP positional analogy) · trend/seasonality/noise components (additive vs multiplicative) · exponential smoothing family (Naïve→Holt-Winters, ETS notation) · AR models (lag construction) · MA models (past errors, q) · ACF/PACF (p/q/s selection rules) · stationarity (ADF/KPSS, differencing order d) · SARIMA/auto_arima/SARIMAX (7 params, AIC, exogenous constraints) · Monte Carlo uncertainty propagation · evaluation (ME, Forecast Ratio, horizon uncertainty cone).

### Week 9 — NEU Steel Defect CNN Classifier + Hardening *(Built, syntax-validated; submission due July 9, 2026)*

- **Stack:** Python · PyTorch · torchvision · scikit-learn · Optuna · Matplotlib · NumPy · Pillow
- **Repo:** `AaradhyaDT/fuseAiF_wk9_neu_defect_cnn`
- **Notebook:** `W9_NEU_Defect_CNN_Assignment.ipynb`
- **Dataset:** NEU-DET surface defect classification; 6 classes (`crazing`, `inclusion`, `patches`, `pitted_surface`, `rolled-in_scale`, `scratches`), 1,440 train / 360 validation images, 200×200 RGB inputs.
- **Normalization:** train-set mean `[0.5049536228179932, 0.5049536228179932, 0.5049536228179932]`; std `[0.10445467382669449, 0.10445467382669449, 0.10445467382669449]`.
- **Part 0:** 2-layer `nn.Module` on flattened 120,000-dim inputs; total parameters `30,721,798`.
- **Q4 optimizer comparison:** final validation accuracy `SGD = 0.206`, `SGD + Momentum(0.9) = 0.167`, `Adam = 0.292`.
- **Q5 regularization ablation:** final validation loss `BatchNorm1d = 4.5459`, `Dropout(0.3) = 1.7918`; final validation accuracy `BatchNorm1d = 0.35`, `Dropout(0.3) = 0.167`.
- **Part A CNN:** final train/val accuracy `0.986 / 0.847` after 15 epochs; `best_model.pt` saved under `assignment/`.
- **Part B hardening:** augmentation-only + BatchNorm2d run finished at final validation accuracy `0.544`.
- **Part C tuning:** 2×2 grid best `lr = 0.01`, `batch_size = 16`, `val_acc = 0.6361111111111111`; Optuna best `lr = 0.00029380279387035364`, `batch_size = 16`, `val_acc = 0.6333333333333333`.
- **Execution note:** CPU-only run path is practical but slow; notebook documents the full-scale CPU estimate and keeps Optuna at a reduced budget for tractability.
- **Colab/Kaggle runtime path added (verified this session, July 9):** notebook now includes a Kaggle-download cell (installs `kaggle`, uploads `kaggle.json`, downloads+unzips NEU-DET, auto-detects the extracted layout, and copies it into `data/NEU-DET/{train,validation}/images/`) plus a `DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")` fix, replacing the earlier hardcoded-CPU line — both confirmed present in the uploaded `.ipynb`. Closes out the two items flagged pending in the prior Kaggle-setup session export. **Submission-status not confirmed this session** — due date (July 9, 2026) has arrived; needs a status update once actually submitted/graded.

---

## 3. CV-Ready Summary (verbatim block, as maintained)

**Fuse AI Fellow — Fusemachines AI Fellowship 2026 (Active) | 2026 – Present**
*Fusemachines*

- Admission: Passed entrance examination (March 2026) covering linear algebra, calculus, probability, Python, and ML.
- REST API: Built a containerized customer REST API: FastAPI + PostgreSQL + Docker (4-layer architecture, asyncio concurrency).
- Text-to-SQL agent: Developed a five-stage agentic pipeline (Planner → Generator → Validator → Executor → Summarizer) achieving 100% execution success and 100% accuracy on a 50-question benchmark.
- Churn & CLV modeling: End-to-end pipeline with Logistic Regression / Ridge / SGD classifiers; Stratified 5-fold CV ROC-AUC 0.841 ± 0.005; threshold-tuned for top-200 high-risk segment; Papermill automation.
- Tree-based ensemble: Random Forest + XGBoost with ImbPipeline/SMOTE (zero leakage), SHAP explainability, GridSearch tuning, and Joblib serialization.
- Probabilistic models: Bayesian estimation (MLE/MAP/full Bayes), Dirichlet-multinomial inference, Gaussian process regression, probabilistic graphical models, and Bayesian logistic regression via PyMC/ArviZ/pgmpy.
- Customer segmentation: K-Means, Hierarchical (Ward/Complete/Average/Single dendrograms), and DBSCAN on UCI Online Retail II (~500K transactions); RFM + category-ratio feature engineering; Silhouette/Davies-Bouldin/Calinski-Harabasz validation; business narrative with executive summary.
- Forecasting: Benchmarked 9 classical-to-modern forecasters (SARIMA, Holt-Winters, Prophet, LightGBM, LSTM, XGBoost) on monthly S&P 500 data; built a 4-model ensemble beating all single models (MASE 2.44), confirmed via Diebold-Mariano significance test (p = 0.0092).
- Computer vision: Built a PyTorch CNN for NEU steel defect classification with dataset-specific normalization, 15-epoch Part A training, augmentation/BatchNorm/Dropout hardening, and Optuna-based hyperparameter tuning; best grid validation accuracy reached 0.6361 and the final CNN checkpoint was saved as `best_model.pt`.

*Note: CV label still reads "(Active) | 2026 – Present" — accurate while Wk < 24/Oct 18, 2026; update to a closed date range once the fellowship formally ends.*

---

## 4. Project Ranking (fellowship entries only, from master v7 table)

| Rank | Item | Score | Status |
| --- | --- | --- | --- |
| 2 | Wk5 — Telco Tree-Based Ensemble | 9.0 | Complete |
| 3 | Wk3 — Text-to-SQL Pipeline | 8.7 | Complete |
| 4 | Wk4 — Telco Churn & CLV Pipeline | 8.5 | Complete |
| 5 | Wk6 — Probabilistic Models | 8.2 | Complete — portfolio live |
| 11 | Wk7 — Clustering | 8.0 | Complete — portfolio live (v113) |
| 12 | Wk8 — Forecasting | 8.1 | Complete — portfolio **pending** |
| 14 | Fellowship Prep Toolkit | 6.5 | Complete |
| — | Wk9 — NEU Steel Defect CNN | — | Complete; score not yet posted in the master table |

---

## 5. Dev Standards Gate — Applies to All Fellowship Repos

### 12-Factor Pre-Commit Checklist (§16 in master)

Run before every final `git commit` on any `fuseAiF_*` repo (also applies to Nexus).

| # | Factor | Check |
| --- | --- | --- | --- |
| 1 | Codebase | One repo/project, no stray local branches, `git status` clean except staged. |
| 2 | Dependencies | `requirements.txt`/`pyproject.toml` pinned and current; verify via clean-venv install. |
| 3 | Config | No hardcoded secrets/keys/paths; `.env` gitignored, `.env.example` committed. |
| 4 | Backing services | DB/API/storage paths via env vars, swappable without code change. |
| 5 | Build/Release/Run | Dockerfile separates install from runtime; build artifacts gitignored. |
| 6 | Processes | App stateless between requests; no unsafe module-level mutable state. |
| 7 | Port binding | Port from env var, not hardcoded. |
| 8 | Concurrency | No shared mutable state across `asyncio.gather`/Papermill parallel runs. |
| 9 | Disposability | Fast cold start (<5s), graceful SIGTERM shutdown, no orphaned connections. |
| 10 | Dev/prod parity | `docker-compose.yml` mirrors prod; Python version pinned. |
| 11 | Logs | No stray `print()`; `logging` module, stdout, level via env var. |
| 12 | Admin processes | Migrations/seed/fix scripts standalone under `scripts/`, documented, never in app startup. |

**Quick pre-commit sequence:**

```bash
git diff --cached | grep -iE "(api_key|password|secret|token)" && echo "⚠ SECRET DETECTED" || echo "✅ No secrets"
git diff --cached --name-only | grep "\.env$" && echo "⚠ .env STAGED — remove it" || echo "✅ .env clean"
pip freeze > /tmp/current_reqs.txt && diff requirements.txt /tmp/current_reqs.txt | head -20
pytest -q 2>/dev/null || echo "(no tests yet — add at least one smoke test)"
git status && git diff --stat --cached
```

**Per-repo compliance status:**

| Repo | Factor 2 (deps) | Factor 3 (config) | Factor 11 (logs) | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `fuseAiF_wk3_text2sql` | ✅ | ✅ | ✅ | Docker + .env pattern established |
| `fuseAiF_wk5_telco_churn_ensembles` | ✅ | N/A | ✅ | No secrets; notebook-based |
| `fuseAiF_wk7_customer_segmentation` | ✅ | N/A | ✅ | `.xlsx` gitignored |
| Future fellowship repos | — | — | — | Start from this checklist |

### Instructor Feedback Log

| Week | Feedback | Status |
| --- | --- | --- | --- |
| Wk 2/3/4 (unconfirmed exact week) | Declutter into subfolders; separate `APIRouter` per domain instead of monolithic single-file API. | ⏳ Not yet retroactively applied — apply to next API-based project. |

---

## 6. Fellowship Priority Trigger — Session Protocol (for future task planning)

**Activates on any of:** repo/filename matching `fuseAiF_*`; mention of "fellowship"/"Fusemachines"/"fuse week"/a week number in that context; a `PATCH_fuse*.md` upload; secondary triggers (CV update, portfolio HTML update, LinkedIn update).

**Order of operations when triggered:**

1. Compute current Fuse week: `floor((today − May 4 2026) / 7) + 1`, capped at 24.
2. Identify which week's repo the session concerns (filename/message).
3. Check for an uploaded `PATCH_*.md` — if present, treat as primary source of truth for that week; run patch-merge mode (read patch meta → apply facts to Projects/Fellowship history → flag conflicts → produce changelog entry).
4. If no patch file: standard session mode — offer to generate a patch summary at session end; apply the 12-Factor checklist gate before any `git commit` advice; track completion against the week's assignment scope.
5. End-of-session: summarize any new repo/notebook/deliverable in patch-ready format (what was done/built/learned, mistakes, open items) for later `PATCH_*.md` generation.

**Patch file naming:** `PATCH_fuseWkN_[topic]_YYYYMMDD.md` (e.g. `PATCH_fuseWk8_nlp_20260626.md`). Always include: source repo, period, generated-by, sections affected, what was done/built/learned, mistakes/corrections, open items, evidence pointers (commit hashes, notebook cells, key metrics).

---

## 7. Open Items / Pending Actions (fellowship-specific)

- **Repository role clarification:** this workspace should be treated as the organization archive for the fellowship work, with private assignment repos as the execution repositories.
- **Portfolio trigger — Week 8 Forecasting:** not yet added to `projects.html`. Pending.
- **Week 9 NEU Defect CNN:** notebook completed, `best_model.pt` saved under `assignment/`, and Colab/Kaggle runtime path (Kaggle-download cell + CUDA auto-detect) verified present as of July 9, 2026. **Due today (July 9, 2026) — submission not yet confirmed.**
- **Instructor feedback (APIRouter refactor):** not yet retroactively applied to any repo.
- **Nexus repo Factor 3/11 compliance:** `.env.example` needs check; `print()` statements need replacing with `logging` — flagged before next commit (Nexus, not a fellowship repo itself, but governed by the same checklist).
- **Project selection (post-Wk8):** upcoming — no domain/topic chosen yet as of last log.
- **CV status label:** still reads "(Active) | 2026 – Present" — will need a closed date range after Oct 18, 2026.

- **Portfolio trigger — Week 8 Forecasting:** not yet added to `projects.html`. Pending.
- **Week 9 NEU Defect CNN:** notebook completed, `best_model.pt` saved under `assignment/`, and Colab/Kaggle runtime path (Kaggle-download cell + CUDA auto-detect) verified present as of July 9, 2026. **Due today (July 9, 2026) — submission not yet confirmed.**
- **Instructor feedback (APIRouter refactor):** not yet retroactively applied to any repo.
- **Nexus repo Factor 3/11 compliance:** `.env.example` needs check; `print()` statements need replacing with `logging` — flagged before next commit (Nexus, not a fellowship repo itself, but governed by the same checklist).
- **Project selection (post-Wk8):** upcoming — no domain/topic chosen yet as of last log.
- **CV status label:** still reads "(Active) | 2026 – Present" — will need a closed date range after Oct 18, 2026.

---

## 8. Known Constraint Relevant to Future Fellowship Planning

**Fellowship learning gap** (last updated June 27, 2026): Tasks are submitted on time, no online class skipped — but concepts are mostly skimmed rather than deeply internalized (fatigue, or material not clicking in a single pass). Work goes in; understanding doesn't always fully land. Risk: if the final/capstone project lands in a domain only skimmed, the gap becomes visible.

**Directive carried in master profile:** pick a final project topic where something actually clicked during the weekly work, so the project forces the consolidation the weekly tasks didn't.
