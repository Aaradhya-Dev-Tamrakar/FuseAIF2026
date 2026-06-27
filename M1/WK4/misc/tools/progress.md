# 📊 Week 4 Statistical ML: Linear Models — Task Progress Tracker
**AIF 2026 · Phase 2 · Telco Churn & CLV Modeling**

This document tracks the step-by-step progress of the Week 4 Statistical Machine Learning assignment. It details completed tasks, current blockers, and next steps to ensure a rigorous, end-to-end executed notebook submission.

---

## 📈 Overall Completion Status

- **Total Tasks:** 5 Major Blocks (19 Sub-tasks)
- **Completed:** 19 Sub-tasks (100% Complete)
- **In Progress:** 0 Sub-tasks
- **Remaining:** 0 Sub-tasks
- **Current Blocker:** **None!** The notebook has been fully populated, executed top-to-bottom without error via `papermill`, exported to HTML, and synced with the structural `graphify` knowledge graph.

---

## 🗺️ Detailed Task & Progress Matrix

| Section / Task | Description | Status | Notes |
| :--- | :--- | :---: | :--- |
| **0. Environment Setup** | Initialize virtual environment and install libraries. | **✔️ Completed** | `.venv` created, core packages installed. |
| **Block 1 — Understand the Problem** | **Task 1: Basic Inspection & Formulation (15%)** | | |
| ├── 1.1 Basic Inspection | Load data, examine shape, types, and summary statistics. | **✔️ Completed** | `df.head()`, `df.info()` verified. |
| ├── 1.2 Problem Formulation | Formulate X, y, Bernoulli distribution, and Log Loss. | **✔️ Completed** | Core assumptions & uncertainties documented. |
| ├── 1.3 Data Profiling & Fixing | Convert `TotalCharges` objects, handle nulls, map `Churn`. | **✔️ Completed** | Whitespace nulls handled; mapped to 0/1. |
| ├── 1.4 Naive Baseline | Build Dummy Classifier to illustrate the "Accuracy Trap." | **✔️ Completed** | Naive baseline accuracy calculated (~73.46%). |
| **Block 2 — Preprocessing** | **Task 2.1: Preprocessing Pipeline** | | |
| └── 2.1 Encode, Split, Scale | One-hot encode, 70/15/15 stratified split, and scale features. | **✔️ Completed** | Executed. Scaling fitted on train split only. |
| **Block 3 — Classification** | **Task 2.2-2.6: Classification Experiment (25%)** | | |
| ├── 3.1 Train Candidates | Fit Logistic Regression, Ridge, and SGD classifiers. | **✔️ Completed** | Fitted successfully on `X_train_scaled`. |
| ├── 3.2 Comparison Table | Tabulate Accuracy, Precision, Recall, F1, AUCs, Log Loss. | **✔️ Completed** | Generated and sorted metrics table. |
| ├── 3.3 ROC & PR Curves | Visualize performance on imbalanced data. | **✔️ Completed** | Plotted ROC & PR curves side-by-side. |
| ├── 3.4 Threshold Tuning | Sort probabilities and map top 200 risk segment (9.5%). | **✔️ Completed** | Target threshold derived at `0.385` for budget constraint. |
| ├── 3.5 Coef Inspection | Interpret feature weights (demographics vs. contracts). | **✔️ Completed** | Barplot generated for top predictors. |
| ├── 3.6 Batch vs. SGD | Compare convergence patterns and solver times. | **✔️ Completed** | Runtimes recorded; divergence and convergence compared. |
| **Block 4 — Regression** | **Task 3: Regression & CLV (20%)** | | |
| ├── 4.1 Target Derivation | Focus on tenure of churned customers. Plot target. | **✔️ Completed** | target distribution successfully plotted. |
| ├── 4.2 Train Regressors | Fit Linear, Ridge, Lasso, and ElasticNet. | **✔️ Completed** | MAE, RMSE, $R^2$ compared (best: Ridge Regression). |
| ├── 4.3 Residual Plots | Verify homoscedasticity assumption. | **✔️ Completed** | Residual vs. Predicted scatter plot rendered. |
| ├── 4.4 Regularization Path | Plot Lasso coefficient paths (L1 sparsity path). | **✔️ Completed** | Lasso coefficient trajectories plotted over alphas. |
| ├── 4.5 CLV Integration | Calculate value-weighted prioritization metric. | **✔️ Completed** | Derived CLV distribution plotted. Mean CLV = `$1304.70`. |
| **Block 5 — Evaluation** | **Task 4: Evaluation Integrity & Leakage (20%)** | | |
| ├── 5.1 Cross-Validation | Evaluate classifier stability using 5-fold Stratified CV. | **✔️ Completed** | Mean Stratified CV ROC-AUC = `0.841 ± 0.005`. |
| ├── 5.2 Learning Curves | Plot train vs. validation curve over training sizes. | **✔️ Completed** | Convergence learning curve diagnostic plotted. |
| ├── 5.3 Leakage Demo | Simulate cancellation flag leakage to show score inflation. | **✔️ Completed** | Leakage successfully demonstrated (AUC jumps to 0.9995). |
| **Block 6 — Production** | **Task 5: Production Commitments (20%)** | | |
| ├── 6.1 Final Test Evaluation | Run chosen production models on untouched test split. | **✔️ Completed** | Test metrics calculated (LR ROC-AUC = `0.835`, PR-AUC = `0.648`). |
| ├── 6.2 Model Card | Document hyperparameters, limitations, and monitor plan. | **✔️ Completed** | Completed full production Model Card table. |
| └── 6.3 Reflection | Write answers to the five conceptual defence questions. | **✔️ Completed** | Rigorous mathematical answers appended at final reflection. |

---

## 🏁 Delivery Artifacts Created

1. **Executed Notebook:** [W4_Linear_Models_Assignment_executed.ipynb](file:///c:/Users/Aaradhya/Downloads/_Organized/Fuse%20AI%20Fellowship/FUSE%20AIF%202026/WK4/W4_Linear_Models_Assignment_executed.ipynb) (contains full runtime outputs, plots, and analysis)
2. **HTML Deliverable:** [W4_Linear_Models_Assignment_executed.html](file:///c:/Users/Aaradhya/Downloads/_Organized/Fuse%20AI%20Fellowship/FUSE%20AIF%202026/WK4/W4_Linear_Models_Assignment_executed.html) (production-grade static review doc)
3. **Updated Knowledge Graph:** Refreshed `graphify-out/` AST index files (`graph.json`, `graph.html`, and `GRAPH_REPORT.md`)
