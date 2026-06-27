# 🚀 Week 4 Statistical ML: Linear Models — Production Churn & CLV Pipeline
**AIF 2026 · Phase 2 Deliverables**

This directory contains a complete, verified, and rigorous statistical machine learning implementation for predicting customer churn and continuous Customer Lifetime Value (CLV) using linear model families. The solution is fully implemented, executed without errors, and documented to production-grade standards.

---

## 🗺️ Project Structure & Key Deliverables

- 📓 **[W4_Linear_Models_Assignment.ipynb](W4_Linear_Models_Assignment.ipynb):** The primary Jupyter Notebook containing the data fixes, mathematical formulations, models training, diagnostic plots, and interpretative responses.
- 🚀 **[W4_Linear_Models_Assignment_executed.ipynb](W4_Linear_Models_Assignment_executed.ipynb):** The end-to-end executed notebook containing completed runtime outputs, verified figures, and calculated parameters.
- 🌐 **[W4_Linear_Models_Assignment_executed.html](W4_Linear_Models_Assignment_executed.html):** A standalone static HTML page displaying high-resolution seaborn/matplotlib plots for ease of presentation and review.
- 📊 **[progress.md](progress.md):** The task completion matrix confirming 100% completion of all 19 sub-tasks under the Week 4 curriculum.
- 📋 **[W4_Task_Plan.md](W4_Task_Plan.md):** The original pedagogical blueprint and task criteria mapping Week 4 metrics.

---

## 📈 Key Modeling Experiments & Verification Results

### 1. Understand the Problem (Data Quality & Baseline)
* **Imputation Strategy:** Identified 11 whitespace nulls in `TotalCharges` representing new customers with 0 tenure. Replaced values with `0.0` to preserve mathematical consistency.
* **The Accuracy Trap:** Established a naive majority-class baseline classifier which achieves a misleading **73.46% accuracy** but suffers from **0% recall**—capturing zero actual churners. We explain the risk of relying solely on accuracy under severe class imbalance.

### 2. Churn Classification (Logistic Regression)
* **Candidates Evaluated:** [LogisticRegression](W4_Task_Plan.md#L168) (L2 regularized, L-BFGS solver), `RidgeClassifier` (regression closed-form), and `SGDClassifier` (stochastic gradients with log-loss).
* **Calibrated Ranking & Threshold Tuning:** Derived an operational decision threshold of **`0.385`** matching the retention team's weekly budget limit (top 9.5% risk segment).
* **Performance Summary:**
  * **Test Accuracy:** `80.42%`
  * **Test Precision:** `60.41%` (optimizes calling efficiency by catching target churners)
  * **Test Recall:** `52.53%`
  * **Test ROC-AUC:** `0.8354`
  * **Test PR-AUC:** `0.6482`
* **Convergence Diagnostics:** Full-batch L-BFGS converges cleanly and output stable parameters, whereas SGD introduces stochastic shuffling variance.

### 3. Tenure Regression & CLV Derivation
* **Target Cohort:** Modelled continuous survival tenure ($y \ge 0$) *only* for the churned cohort.
* **Model Selection:** Rigorously compared `LinearRegression`, `Ridge`, `Lasso`, and `ElasticNet`. `Ridge Regression` ($\alpha=1.0$) was chosen as the production candidate.
* **Regression Performance:** MAE: `11.16 months`, RMSE: `14.77 months`, **$R^2$ Score: `0.5483`** (explains 55% of the variance in customer longevity using billing files alone).
* **CLV Synthesis:** Synthesized continuous **Customer Lifetime Value** ($CLV = MonthlyCharges \times predicted\_tenure$) with negative predictions clipped to `0.0` to support value-weighted business prioritization.

### 4. Evaluation Integrity & Leakage Mitigation
* **Learning Curves:** Diagnostics confirm that both training and validation curves plateau at `0.84 ROC-AUC` as training size increases, indicating extremely low variance (no overfitting).
* **Leakage Demonstration:** Conducted a controlled target contamination experiment by injecting `leak = tenure * Churn`. This artificially inflated validation scores to a perfect `0.9995 ROC-AUC`. We explain why standard cross-validation is blind to leakage, demonstrating the absolute need for code reviews.

### 5. Production Model Card
A complete [Model Card](W4_Linear_Models_Assignment_executed.html#6.2-Model-Card) has been committed to the notebook, covering chosen configurations, limitations, monitoring criteria (PSI/KS tests), and retraining cadences.

---

## 🏃 Setup & Verification Instructions

### 1. Launch Virtual Environment
Navigate to the Week 4 directory and activate the local virtual environment:
```powershell
cd WK4
.\.venv\Scripts\Activate.ps1
```

### 2. Regenerate Results
The code is fully automated. You can run the entire notebook or regenerate the executed deliverables:
```powershell
# Populate the notebook programmatically with clean, complete solutions
python complete_notebook_by_index.py

# Execute the notebook top-to-bottom and compile outputs
python -m papermill W4_Linear_Models_Assignment.ipynb W4_Linear_Models_Assignment_executed.ipynb

# Convert the executed notebook to a clean static review page
jupyter nbconvert --to html W4_Linear_Models_Assignment_executed.ipynb
```

### 3. View the AST Knowledge Graph
The folder contains a structural AST-based knowledge graph in `graphify-out/` describing imports, pipelines, and functions. Update the index dynamically:
```powershell
# Update AST metadata
graphify update .
```
