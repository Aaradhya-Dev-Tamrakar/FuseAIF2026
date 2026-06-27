# W4 Task Plan — Statistical ML: Linear Models
**AIF 2026 · Phase 2 · Due: 24 May**
**Dataset:** Telco Customer Churn · 7,043 rows · 21 columns

---

## How to Work Through This

Work **top to bottom, one block at a time**. Every code cell should be followed by a markdown cell
that explains what you found and why it matters. Numbers without interpretation are not answers.

---

## Setup Cell (do this first)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, learning_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                              roc_auc_score, average_precision_score, log_loss,
                              mean_absolute_error, mean_squared_error, r2_score,
                              roc_curve, precision_recall_curve)
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
```

---

## Task 1 — Understand the Problem First
**Weight: 15% · Notebook block: Block 1**

### 1.1 Basic Inspection

**Code to write:**
- `df.head()`, `df.shape`, `df.info()`, `df.describe()`
- Check `df['TotalCharges'].dtype` — it will show `object`, not `float`
- Find the whitespace nulls: `df[df['TotalCharges'].str.strip() == '']`

**Markdown to write after:**
- What does one row represent? (one customer's subscription record)
- Why is `TotalCharges` an object? (whitespace strings `' '` are hiding as values)
- How many rows are affected? (there are 11)

---

### 1.2 Problem Formulation

**Write these in a markdown cell — your own words, not copy-paste:**

| Field | What to write |
|---|---|
| **X** | All columns except `customerID` and `Churn` — demographics, services, account info |
| **y** | `Churn` — binary: 1 = churned, 0 = stayed |
| **Distribution of y** | Bernoulli (each customer either churns or doesn't) |
| **Loss function** | Binary cross-entropy — natural for Bernoulli outcomes |
| **Hypothesis class** | Linear models — logistic regression, ridge, SGD |

**Three assumptions to state + what breaks if violated:**

1. The relationship between features and churn probability is approximately linear in log-odds
   - *Violation*: residuals will show a pattern; model systematically wrong for certain customer segments
2. Training data is representative of future customers
   - *Violation*: distribution shift — model degrades silently after deployment
3. Features are measured without systematic error
   - *Violation*: a miscoded column (e.g., wrong contract type for some rows) corrupts coefficients

**Sources of uncertainty — be specific:**
- `TotalCharges`: 11 whitespace nulls — are these new customers with no charges yet? Not random.
- `Churn` label: was churn recorded at the moment of cancellation or retroactively? Label noise possible.
- Class imbalance: 73% No / 27% Yes — accuracy will be a misleading metric.
- No timestamp column: we cannot know if behaviour patterns have shifted over time.

---

### 1.3 Data Profiling & Fixing

**Code to write:**

```python
# Fix TotalCharges
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Decide on null handling — justify in markdown
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
# OR: df.dropna(subset=['TotalCharges'], inplace=True)

# Encode target
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# Drop customerID — not a feature
df.drop(columns=['customerID'], inplace=True)
```

**Plots to make (3 histplots with kde=True):**
- `MonthlyCharges` — roughly uniform/bimodal — describe the shape
- `tenure` — bimodal (many new + many long-term customers) — describe what this means for the business
- `TotalCharges` — right-skewed — explain why (it is tenure × monthly charges, so it inherits tenure's shape)

**Markdown decision to write:**
- Why median imputation vs. dropping? (11 rows ≈ 0.15% of data; dropping is safer; median is reasonable if keeping)
- Are there impossible values? (tenure = 0 is valid for new customers; MonthlyCharges has no negatives)

---

### 1.4 Naive Baseline

**Code to write:**
```python
majority_class_accuracy = df['Churn'].value_counts(normalize=True).max()
print(f"Naive baseline accuracy: {majority_class_accuracy:.3f}")
```

**Markdown to write:**
- The naive model always predicts "No churn" → ~73.5% accuracy
- Why this is dangerous: it identifies **zero** churners — the entire point of the system
- Accuracy here rewards doing nothing; we need Recall, F1, and PR-AUC instead

---

## Task 2 — Classification Experiment
**Weight: 25% · Notebook block: Block 3**

### 2.1 Preprocessing Pipeline

**Code to write:**
```python
# Separate features
categorical_cols = df.select_dtypes(include='object').columns.tolist()
numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']

# Encode categoricals — use get_dummies or LabelEncoder; justify your choice
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Split BEFORE scaling — no leakage
X = df_encoded.drop(columns=['Churn'])
y = df_encoded['Churn']

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
X_val, X_test, y_val, y_test = X_temp[:len(X_temp)//2], X_temp[len(X_temp)//2:], \
                                 y_temp[:len(y_temp)//2], y_temp[len(y_temp)//2:]

# Scale AFTER splitting — fit only on train
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
```

**Markdown:** Explain why you use `stratify=y` (preserve 27/73 ratio in each split). Explain why scaler is fit only on X_train (fitting on full data leaks val/test distribution into training).

---

### 2.2 Train Three Classifiers

For each model: train → predict on val → record metrics.

**Models:**
```python
models = {
    'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
    'RidgeClassifier':    RidgeClassifier(),
    'SGDClassifier':      SGDClassifier(loss='log_loss', max_iter=1000, random_state=42)
}
```

**Build a comparison table with these columns:**
`Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC | Log Loss`

**Note on RidgeClassifier:** It doesn't have `predict_proba` by default. Use `decision_function` scores for ROC-AUC, or use `CalibratedClassifierCV` to get probabilities. Mention this limitation.

---

### 2.3 ROC and Precision-Recall Curves (best model only)

**Code to write:**
```python
# ROC curve
fpr, tpr, thresholds_roc = roc_curve(y_val, best_model.predict_proba(X_val_scaled)[:,1])
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate'); plt.ylabel('True Positive Rate'); plt.title('ROC Curve')

# PR curve
precision, recall, thresholds_pr = precision_recall_curve(y_val, best_model.predict_proba(X_val_scaled)[:,1])
plt.plot(recall, precision)
plt.xlabel('Recall'); plt.ylabel('Precision'); plt.title('Precision-Recall Curve')
```

**Threshold decision — the 200-customer budget constraint:**
```python
# Total val+test customers = ~2,113
# 200 / 2113 ≈ 9.5% of customers can be called
# Find threshold where predicted positives ≈ 200

probs = best_model.predict_proba(X_val_scaled)[:,1]
threshold = np.percentile(probs, 90)  # top 10% most likely to churn
print(f"Threshold for top 200: {threshold:.3f}")
```

**Markdown to write:** Explain the trade-off — a higher threshold means fewer calls but higher precision; lower threshold means more recall but wasted calls. What matters more to the retention team?

---

### 2.4 Coefficient Inspection

```python
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train_scaled, y_train)

coef_df = pd.DataFrame({'feature': X_train.columns, 'coefficient': lr_model.coef_[0]})
coef_df = coef_df.reindex(coef_df['coefficient'].abs().sort_values(ascending=False).index)
coef_df.head(15).plot(kind='bar', x='feature', y='coefficient')
```

**Markdown to write:**
- Which features have the largest positive coefficient? (likely `Contract_Two year` negative — long contracts reduce churn; `tenure` negative)
- Do the signs make business sense? Discuss at least 3 features.
- If anything surprises you, say so and hypothesize why.

---

### 2.5 Batch vs Stochastic Gradient Descent Comparison

**Code to write:**
```python
lr_batch = LogisticRegression(solver='lbfgs', max_iter=1000)    # batch GD approximation
lr_sgd   = SGDClassifier(loss='log_loss', max_iter=1000, random_state=42)  # true SGD

# Train both, compare val metrics and training time using time.time()
import time
```

**Markdown to write:**
- Do they reach similar F1/AUC? (usually yes, with enough iterations)
- Which is faster on 7K rows? (SGD is faster on large data; on 7K the difference is small)
- When to prefer SGD? (large datasets, online learning, mini-batch streaming data)

---

## Task 3 — Regression Experiment
**Weight: 20% · Notebook block: Block 4**

### Choose your regression target

**Recommended: tenure as survival time** (most interpretable for the business)

```python
# Use only churned customers for tenure prediction — they have a definite end date
churn_df = df_encoded[df_encoded['Churn'] == 1].copy()
X_reg = churn_df.drop(columns=['Churn', 'tenure'])
y_reg = churn_df['tenure']

# Or for CLV (all customers):
# y_reg = df_encoded['MonthlyCharges'] * df_encoded['tenure']
```

**Justify your target choice in markdown** — tenure is observable, meaningful, and not derived from the model's own predictions.

---

### 3.1 Train Regression Models

```python
reg_models = {
    'LinearRegression': LinearRegression(),
    'Ridge':            Ridge(alpha=1.0),
    'Lasso':            Lasso(alpha=0.1),
    'ElasticNet':       ElasticNet(alpha=0.1, l1_ratio=0.5)
}
```

**Comparison table:** `Model | MAE | RMSE | R²`

**Interpret each metric in context:**
- MAE = average error in months of tenure prediction
- RMSE = penalises large errors more — a customer off by 24 months is much worse than one off by 2
- R² = fraction of variance in tenure explained by the features (0.55 means 45% of variance is still unexplained — what could cause this?)

---

### 3.2 Residual Plot

```python
y_pred_val = best_reg.predict(X_val_reg_scaled)
residuals = y_val_reg - y_pred_val
plt.scatter(y_pred_val, residuals, alpha=0.4)
plt.axhline(0, color='red')
plt.xlabel('Predicted tenure'); plt.ylabel('Residual'); plt.title('Residual Plot')
```

**What to look for:**
- Random scatter around zero = good fit
- Fan shape (heteroscedasticity) = variance increases with predicted value — common in tenure data
- Curve = missing non-linear relationship

---

### 3.3 Regularization Paths

```python
# Lasso regularization path
from sklearn.linear_model import lasso_path
alphas, coefs, _ = lasso_path(X_train_reg_scaled, y_train_reg)
# Plot: x-axis = log(alpha), y-axis = coefficient value, one line per feature
```

**Markdown to write (key conceptual question):**
- **Why does L1 (Lasso) produce sparse solutions?** — Geometrically, the L1 constraint is a diamond shape; the loss contours tend to hit the diamond at a corner where some coefficients are exactly zero. L2 (Ridge) is a circle — loss contours hit the boundary at a smooth point, so coefficients shrink toward zero but rarely reach it.
- Which features survive at high regularization? These are the most robust predictors of tenure.

---

### 3.4 CLV Business Value

**Code (if using CLV as target):**
```python
df_encoded['CLV'] = df_encoded['MonthlyCharges'] * df_encoded['tenure']
```

**Markdown to write:**
- Binary churn prediction says: "This customer will leave" — treat everyone the same
- CLV says: "This customer will leave AND they're worth $1,200 vs $80" — prioritise calls accordingly
- The retention team's 200-call budget should target **high-probability churners with high CLV**, not just probability alone

---

## Task 4 — Evaluation Integrity
**Weight: 20% · Notebook block: Block 5**

### 4.1 Data Split Justification

**Markdown to write:**
- Explain 70/15/15 train/val/test split (or your chosen ratio)
- Why `stratify=y`? (class imbalance — without it, a split might have 20% churn in train but 35% in test)
- Leakage check: confirm scaler is fit only on train; target encoding (if any) done inside CV folds

---

### 4.2 K-Fold Cross-Validation

```python
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(best_model_pipeline, X_train_scaled, y_train, cv=cv, scoring='average_precision')
print(f"CV PR-AUC: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
print(f"Holdout Val PR-AUC: {val_prauc:.3f}")
```

**Markdown:** Do they match? If CV > holdout, model may be overfitting to the specific val split. If CV < holdout, the val set might be unusually easy.

---

### 4.3 Learning Curves

```python
train_sizes, train_scores, val_scores = learning_curve(
    best_model, X_train_scaled, y_train,
    cv=5, scoring='f1', train_sizes=np.linspace(0.1, 1.0, 10)
)
# Plot training score and CV score vs training set size
```

**Markdown — diagnose and prescribe:**

| Symptom | Diagnosis | Fix |
|---|---|---|
| Both curves low | Underfitting | More features, polynomial features, less regularization |
| Train high, val low, gap large | Overfitting | More data, more regularization, simpler model |
| Curves converge and are high | Well-generalised | Ready to ship |

---

### 4.4 Deliberate Leakage Demo

**This is a controlled experiment — document before and after.**

```python
# Step 1: Record clean metrics (already done above)

# Step 2: Create a leakage feature — a noisy version of the target
np.random.seed(42)
X_train_leak = X_train_scaled.copy()
X_val_leak   = X_val_scaled.copy()
# Add column that is 90% correlated with the true label
leakage = y_train.values * 0.9 + np.random.normal(0, 0.1, len(y_train))
X_train_leak = np.hstack([X_train_leak, leakage.reshape(-1,1)])

# Also leak into val (simulating a future-knowing feature, e.g., cancellation_request_flag)
leakage_val = y_val.values * 0.9 + np.random.normal(0, 0.1, len(y_val))
X_val_leak = np.hstack([X_val_leak, leakage_val.reshape(-1,1)])

# Step 3: Retrain and compare
# Step 4: Check if the leakage column dominates the coefficients
# Step 5: Remove it and confirm metrics drop back to baseline
# Step 6: Summary table: Before / With Leakage / After Removal
```

**Markdown to write:**
- What happened to ROC-AUC and PR-AUC with the leakage feature? (should jump dramatically)
- Why is this catastrophic in production? (the feature is derived from the outcome — it won't exist when you predict on new customers)
- Could CV alone detect this? (No — if the leakage feature is in your feature matrix before the split, CV will also see it and report inflated scores)

---

## Task 5 — Production Decision
**Weight: 20% · Notebook block: Block 6**

### 5.1 Final Test Set Evaluation

**Code to write:** Run your chosen model on `X_test_scaled` — the held-out set you have not touched until now.

```python
# Only run this cell after all model selection decisions are made
test_metrics = {
    'Accuracy':  accuracy_score(y_test, y_pred_test),
    'Precision': precision_score(y_test, y_pred_test),
    'Recall':    recall_score(y_test, y_pred_test),
    'F1':        f1_score(y_test, y_pred_test),
    'ROC-AUC':   roc_auc_score(y_test, y_proba_test),
    'PR-AUC':    average_precision_score(y_test, y_proba_test),
}
```

**Markdown:** Do test metrics match val metrics? A large drop means you overfit to the validation set during model selection.

---

### 5.2 Model Card (fill every field)

```markdown
## Model Card — Production Churn Model

| Field | Answer |
|---|---|
| Chosen Classification Model | e.g. LogisticRegression, C=1.0, solver=lbfgs |
| Chosen Regression Model | e.g. Ridge, alpha=1.0 |
| Classification Metrics (test) | Precision: _ Recall: _ F1: _ PR-AUC: _ |
| Regression Metrics (test) | MAE: _ months RMSE: _ months R²: _ |
| Deployment Threshold | e.g. 0.38 |
| Threshold Justification | Maximises recall within 200-call budget constraint |
| Known Limitations | Class imbalance; no temporal features; linear boundary assumption |
| What Could Go Wrong | Distribution shift (new pricing tiers); leakage if cancellation flags added later |
| Monitoring Plan | Track precision/recall weekly; retrain if F1 drops >5% over 4-week window |
| Are Linear Models Sufficient? | Based on learning curves: [your answer with evidence] |
| Evidence | [cite your CV scores, learning curve diagnosis, coefficient analysis] |
```

---

### 5.3 Final Reflection (in notebook)

Write answers to all five reflection questions in a markdown cell. Key ones to prepare for session defence:

1. **Which classifier performed best and why?** — Don't just say "LR had higher PR-AUC." Say why it makes sense (well-calibrated probabilities, sufficient features, no major non-linearities).
2. **Why not just report accuracy?** — 73.5% accuracy from predicting all-No; a model that catches no churners looks great on accuracy.
3. **What did the Lasso path show?** — Which features zeroed out first? Those are the least predictive of tenure/CLV.
4. **How big was the AUC inflation from leakage?** — Report the actual numbers.
5. **Would a non-linear model do better?** — Look at your learning curves: if they plateau with a gap, likely yes.

---

## Submission Checklist

- [ ] All 5 tasks labelled with markdown headers matching block names
- [ ] Every code cell has a comment explaining what it does and why
- [ ] Every output (table, plot, metric) has a written interpretation below it
- [ ] All plots have titles, axis labels, and legends
- [ ] Descriptive variable names (`X_train_scaled` not `x1`)
- [ ] Model card fully filled — no empty fields
- [ ] Notebook runs top-to-bottom without errors
- [ ] Final reflection answered in your own words
- [ ] Submit as single `.ipynb` file

---

## Conceptual Things to Know Cold (you will be asked)

| Question | What to know |
|---|---|
| Why cross-entropy for binary classification? | Bernoulli target → MLE derivation leads directly to cross-entropy |
| Why does L1 give sparse solutions? | Diamond-shaped constraint; loss contours hit corners where coordinates = 0 |
| What is PR-AUC vs ROC-AUC? | PR-AUC more informative when positive class is rare; ROC-AUC inflated by TN count |
| What is the difference between batch GD and SGD? | Batch uses full dataset per update (stable, slow); SGD uses one sample (noisy, fast) |
| What does R² = 0.55 mean? | The model explains 55% of variance in tenure; 45% comes from factors not in the data |
| What is leakage? | A feature available at training time that would not be available at prediction time |
| Why stratify the split? | Class imbalance — preserves 27/73 ratio in each split so metrics are reliable |

---

## Implementation Plan

### Goal
Prepare a self-contained development environment under `WK4`, fill the notebook `W4_Linear_Models_Assignment.ipynb` with runnable code, execute it end-to-end, and generate a complete `graphify-out` directory for local visualization.

### Notes / Risks
- This plan may create a new Python virtual environment in `WK4/.venv`.
- The notebook will be populated and may overwrite the skeleton version. The original is still tracked by Git and can be reverted if needed.

### Open Questions
- Preferred Python version: e.g. `3.10` or `3.11`?
- Should package versions be pinned (`scikit-learn==1.5`) or left on latest stable releases?
- Should the executed notebook also be exported as HTML (`W4_Linear_Models_Assignment.html`)?

### Proposed Workspace Setup
1. Create a local virtual environment in `WK4`:
   - `python -m venv .venv`
   - activate with `.\.venv\Scripts\Activate.ps1`
2. Install required libraries in `.venv`:
   ```powershell
   pip install --upgrade pip
   pip install pandas numpy scikit-learn matplotlib seaborn jupyter nbconvert papermill
   ```
3. Populate the notebook automatically with model code, metrics, plots, and markdown explanations.
4. Execute the notebook end-to-end:
   ```powershell
   python -m papermill W4_Linear_Models_Assignment.ipynb W4_Linear_Models_Assignment_executed.ipynb
   ```
5. Optionally convert the executed notebook to HTML for review:
   ```powershell
   jupyter nbconvert --to html W4_Linear_Models_Assignment_executed.ipynb
   ```
6. Build the Graphify knowledge graph:
   ```powershell
   graphify update .
   ```
7. Serve the Graphify output locally to verify:
   ```powershell
   cmd /C "python -m http.server 8080 --directory graphify-out"
   ```

### Verification Plan
- Confirm required packages are installed inside `.venv`.
- Run the notebook with no errors and validate that final metrics appear.
- Verify `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.html` are generated.
- Open the local Graphify visualizer and confirm the graph loads correctly.

### Next Step
- Await approval for Python version and package pinning.
- Then execute the setup, notebook population, notebook run, and Graphify build inside `WK4` only.
