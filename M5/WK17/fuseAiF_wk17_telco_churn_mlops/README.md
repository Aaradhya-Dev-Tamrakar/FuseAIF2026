# Fuse AI Fellowship 2026 — Week 17 Track A: Telco Customer Churn MLOps

End-to-end production MLOps pipeline for the IBM **Telco Customer Churn** dataset (7,043 customers, binary classification), implementing reproducible environments, experiment tracking, model registry, model serving, drift monitoring, and orchestration.

## Quick Start

```bash
# Clone and set up
git clone https://github.com/AaradhyaDT/fuseAiF_wk17_telco_churn_mlops.git
cd fuseAiF_wk17_telco_churn_mlops

# Install dependencies (requires uv ≥ 0.11)
uv sync

# Run the full pipeline
uv run python -m src.data       # Data ingestion + drift injection
uv run python -m src.train      # Train 3 models + MLflow tracking + registry
uv run python -m src.monitor    # Evidently drift reports + MLflow logging
uv run python -m src.serve      # Launch FastAPI serving (port 8000)

# Verify
uv run ruff check .
uv run pytest -v

# Explore MLflow UI
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

---

## a. Environment & Reproducibility (`uv`)

This project uses **[uv](https://docs.astral.sh/uv/)** (v0.11.24) for deterministic, reproducible Python environment management.

**What `uv` solves for this project specifically:**
- **Deterministic lockfile**: `uv.lock` pins the exact resolved versions of all 142 transitive dependencies (MLflow 3.16.1, Evidently 0.7.23, scikit-learn 1.9.1, LightGBM 4.7.0, FastAPI 0.142.2, etc.), ensuring identical environments across all machines and CI runners.
- **Single-command reproduction**: `uv sync` from a clean clone installs all dependencies in <30 seconds — no `pip install -r requirements.txt` version conflicts or missing system packages.
- **Python version pinning**: `requires-python = ">=3.12,<3.13"` ensures the pipeline runs on exactly Python 3.12.x, preventing subtle behavioral differences across Python versions.

```bash
# Reproduce from clean clone (one command)
uv sync
```

The committed `uv.lock` guarantees byte-identical dependency resolution. The `pyproject.toml` declares all dependencies with minimum version constraints, and `uv.lock` resolves them to exact pinned versions.

---

## b. Experiment Tracking Strategy (`MLflow`)

### Experiment Design

**Experiment**: `TelcoChurn_Prediction_Benchmark`
**Dataset**: Telco Customer Churn (7,043 rows → 70% reference split → 80/20 train/val = 3,944 train, 986 validation)
**Evaluation Priority**: The target variable `Churn` is imbalanced (26.5% positive / 73.5% negative). **F1-Score and ROC-AUC** are prioritized over raw accuracy, because accuracy is misleading on imbalanced targets — a naive majority-class classifier achieves ~73.5% accuracy with 0% recall.

### Three Candidate Models

| # | Model Candidate | Family | Rationale |
|:-:|:---|:---|:---|
| 1 | **Logistic Regression (L2 Balanced)** | `LogisticRegression` | Linear regularized baseline prioritizing interpretability. `C=0.1, penalty='l2', class_weight='balanced'`. |
| 2 | **Random Forest (Depth-6 Balanced)** | `RandomForest` | Non-linear bagged ensemble capturing feature interactions. `n_estimators=150, max_depth=6, class_weight='balanced'`. |
| 3 | **LightGBM (Tuned Gradient Boosting)** | `LightGBM` | Gradient-boosted trees optimized for imbalanced tabular data. `n_estimators=100, lr=0.05, max_depth=4, scale_pos_weight=2.76`. |

### Side-by-Side Run Comparison (All Runs)

| Model Candidate | Family | Accuracy | Precision | Recall | **F1-Score** | **ROC-AUC** | PR-AUC | Status |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Logistic Regression (L2 Balanced) | `LogisticRegression` | 0.7211 | 0.4849 | 0.7977 | **0.6032** | **0.8367** | 0.6620 | Evaluated |
| Random Forest (Depth-6 Balanced) | `RandomForest` | 0.7150 | 0.4786 | 0.8092 | **0.6014** | **0.8344** | 0.6543 | Evaluated |
| **LightGBM (Tuned Gradient Boosting)** | `LightGBM` | **0.7292** | **0.4943** | **0.8321** | **0.6202** | **0.8404** | **0.6623** | **Selected (Production)** |

### Model Selection Justification

**Winning Candidate**: **LightGBM (Tuned Gradient Boosting)**

- **F1-Score (0.6202)** — highest across all candidates, indicating the best harmonic balance between precision and recall on this imbalanced churn task.
- **ROC-AUC (0.8404)** — highest discriminative power, meaning the model's probability ranking most effectively separates churners from non-churners across all classification thresholds.
- **Recall (0.8321)** — captures 83.2% of actual churn events. In a business context, this means only ~17% of at-risk customers would go undetected by the model.
- **Accuracy (0.7292)** — while marginally higher than the other candidates, accuracy alone is insufficient justification on this 26.5% imbalanced target (a naive majority-class classifier achieves 73.5% accuracy with zero recall).

The LightGBM model was registered as `TelcoChurnPredictor` in the MLflow Model Registry and transitioned through two stages: `None → Staging → Production`.

### Logged Artifacts

Each MLflow run includes:
- **Parameters**: All hyperparameters (`C`, `n_estimators`, `max_depth`, `learning_rate`, `scale_pos_weight`, etc.)
- **Metrics**: `accuracy`, `precision`, `recall`, `f1_score`, `roc_auc`, `pr_auc`
- **Visual artifacts**: `confusion_matrix.png`, `roc_curve.png`, `precision_recall_curve.png`
- **Model artifact**: Full scikit-learn pipeline (preprocessor + classifier) serialized via cloudpickle

### Model Registry

```
TelcoChurnPredictor v1:
  Stage transitions: None → Staging → Production
  Alias: @production
  Description: "Production TelcoChurn model selected based on highest
               F1-Score (0.6202) and ROC-AUC (0.8404). Model family: LightGBM."
```

---

## c. Monitoring & Drift Strategy (`Evidently AI`)

### Reference vs. Current Setup

| Dataset | Description | Size | MonthlyCharges Mean | Month-to-month % | Churn Rate |
|:---|:---|:---:|:---:|:---:|:---:|
| **Reference** | Training-time baseline (70% stratified split, clean) | 4,930 rows | $64.95 | 54.8% | 26.5% |
| **Current** | Simulated production data (30% split + synthetic drift) | 2,113 rows | $92.78 | 85.0% | 37.5% |

### Synthetic Drift Injections

Three deliberate perturbations simulate realistic production data shifts:

1. **Numeric Shift**: `MonthlyCharges += $28.50` (with Gaussian jitter) — simulates pricing revisions or inflation.
2. **Categorical Skew**: `Contract == 'Month-to-month'` oversampled to 85% (from baseline 55%) — simulates customer behavior shift toward flexible contracts.
3. **Label/Concept Drift**: 8% of churn labels flipped in the high-charge bracket — simulates evolving churn patterns.

### Drift Detection Results

**Data Drift Report**: 4/20 columns flagged as statistically drifted (20.0% share).

| Feature | Drift Detected | Statistical Score | Interpretation |
|:---|:---:|:---:|:---|
| `MonthlyCharges` | **Yes** | 0.9203 (Wasserstein) | +$28.50 shift correctly detected |
| `Contract` | **Yes** | 0.2365 (Jensen-Shannon) | Month-to-month oversample correctly detected |
| `Churn` (target) | No | — | 8% label flip was too subtle for statistical significance at this sample size |

**Custom Metric Test Results**: 1/4 passed, 3 failed (intentional).

| Test | Status | Explanation |
|:---|:---:|:---|
| `TestColumnValueMean(MonthlyCharges, ±$15)` | **FAIL** | Mean shifted +$27.83 exceeds $15 tolerance — **intentional failure proving test efficacy** |
| `TestColumnDrift(MonthlyCharges)` | **FAIL** | Confirmed significant distributional shift |
| `TestColumnDrift(Contract)` | **FAIL** | Confirmed categorical distribution skew |
| `TestShareOfDriftedColumns(≤25%)` | **PASS** | 20% of columns drifted, within overall health threshold |

### Production Implication

If this drift were detected in a real production pipeline, the recommended actions would be:
1. **Alert** the ML engineering team via Airflow/PagerDuty/Slack.
2. **Investigate root cause**: Is the pricing revision intentional (business-driven) or a data pipeline bug?
3. **Trigger model retraining** on the new data distribution to prevent prediction accuracy degradation.
4. **Monitor** the retrained model's performance on a holdout set before promoting to Production.

All three HTML reports (`data_drift_report.html`, `target_drift_report.html`, `custom_drift_tests.html`) are saved to `reports/` and logged as MLflow artifacts.

---

## d. Orchestration — Airflow Drift DAG

### DAG: `telco_churn_drift_monitoring`

```
Schedule: @daily
Start Date: 2026-10-01

fetch_latest_production_batch  →  run_evidently_drift_check  →  evaluate_drift_threshold
                                                                       │
                                                           ┌───────────┴───────────┐
                                                           │                       │
                                                  alert_and_trigger_retrain   log_clean_status
                                                  (if drifted > 25%)         (if healthy)
```

**Task Details**:
- `fetch_latest_production_batch`: Loads the latest production data batch (in production: from BigQuery/Snowflake/Kafka).
- `run_evidently_drift_check`: Executes the full Evidently monitoring pipeline (Data Drift + Target Drift + Custom Tests).
- `evaluate_drift_threshold`: Branching task — if >25% of features have drifted, routes to alert/retrain; otherwise logs clean status.
- `alert_and_trigger_retrain`: Sends alert notifications (Slack, PagerDuty) and triggers the retraining pipeline.
- `log_clean_status`: Records that the model is healthy and no action is needed.

---

## Project Structure

```
fuseAiF_wk17_telco_churn_mlops/
├── pyproject.toml          # uv project definition + dependencies
├── uv.lock                 # Deterministic lockfile (142 packages)
├── README.md               # This file
├── data/
│   ├── raw/                # Original Telco Churn CSV (7,043 rows)
│   └── processed/          # reference.parquet + current.parquet (drifted)
├── src/
│   ├── __init__.py
│   ├── data.py             # Data ingestion, cleaning, splitting, drift injection
│   ├── train.py            # MLflow experiment tracking (3 models) + registry
│   ├── monitor.py          # Evidently AI drift monitoring + custom tests
│   └── serve.py            # FastAPI model serving (/health, /predict)
├── dags/
│   └── telco_churn_drift_dag.py  # Airflow daily drift monitoring DAG
├── tests/
│   ├── test_data.py        # 16 tests: data pipeline verification
│   └── test_serve.py       # 5 tests: API endpoint verification
├── reports/
│   ├── mlflow_run_comparison.md   # Side-by-side run comparison table
│   ├── mlflow_run_comparison.csv  # Comparison data (CSV)
│   ├── data_drift_report.html     # Evidently Data Drift report
│   ├── target_drift_report.html   # Evidently Target Drift report
│   └── custom_drift_tests.html    # Evidently Custom Tests report
└── mlruns/                 # MLflow artifact store (auto-generated)
```

## Verification

```bash
# Lint: 0 errors
uv run ruff check .

# Tests: 21/21 passing
uv run pytest -v

# MLflow UI: inspect runs, compare metrics, view registered models
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```
