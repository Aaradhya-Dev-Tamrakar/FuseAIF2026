# MLflow Experiment Tracking — Side-by-Side Run Comparison

**Experiment**: `TelcoChurn_Prediction_Benchmark`
**Dataset**: Telco Customer Churn (7,043 rows, Reference fold: 4,930 rows, Val fold: 986 rows)
**Evaluation Criterion**: Imbalanced target `Churn` (26.5% positive). F1-Score and ROC-AUC prioritized over raw accuracy.

| Model Candidate | Family | Run ID | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Status |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Logistic Regression (L2 Balanced)** | `LogisticRegression` | `684270a1` | 0.7211 | 0.4849 | 0.7977 | **0.6032** | **0.8367** | 0.6620 | Evaluated |
| **Random Forest (Depth-6 Balanced)** | `RandomForest` | `52c7d150` | 0.7150 | 0.4786 | 0.8092 | **0.6014** | **0.8344** | 0.6543 | Evaluated |
| **LightGBM (Tuned Gradient Boosting)** | `LightGBM` | `109116de` | 0.7292 | 0.4943 | 0.8321 | **0.6202** | **0.8404** | 0.6623 | [WINNER] Selected (Production) |

### Selection Justification
- **Winning Candidate**: **LightGBM (Tuned Gradient Boosting)** (`Run ID: 109116de67b24b508e71fb168eda6e76`)
- **Quantitative Rationale**: In churn prediction, false negatives (failing to identify an at-risk customer who leaves) are financially punitive compared to false positives (sending a retention coupon to a retained customer). Accuracy (0.7292) is misleading on this imbalanced dataset (a naive majority-class classifier achieves ~73.5% accuracy with 0.0000 recall).
- **Trade-off Analysis**: LightGBM (Tuned Gradient Boosting) achieved the optimal balance of **F1-Score (0.6202)**, **ROC-AUC (0.8404)**, and high sensitivity / **Recall (0.8321)**, capturing the vast majority of churn events while maintaining calibrated precision.
