# 📋 Week 5 Project Tasks Checklist

This checklist tracks the implementation progress for the **Fusemachines AI Fellowship Week 5 Project on Tree-Based Models & Ensembles**.

---

## 🚀 Tasks Roadmap

### 📦 Stage 1: Setup & Data Preparation
- [x] Load Dataset & Initial EDA
- [x] Fix Data Quality Issues (Handle whitespace in `TotalCharges` dynamically)
- [x] Define Target & Features (Drop non-predictive features)
- [x] Train-Test Split (80/20 stratified split)

### 🛠️ Stage 2: Pipeline Architecture
- [x] Setup `ColumnTransformer` (Median imputation + scaling for numeric; Mode imputation + OHE for categorical)
- [x] Build Class Balancing Pipelines (`ImbPipeline` with SMOTE to prevent data leakage during Cross-Validation)

### 📈 Stage 3: Modeling & Evaluation (Classification)
- [x] Implement mathematical calculations from scratch: Gini Impurity, Shannon Entropy, and Information Gain
- [x] Recreate the `bootstrap_sample` logic from scratch to build custom bagging mechanics
- [x] Train Naïve Baseline Decision Tree Classifier
- [x] Evaluate baseline performance (Confusion Matrix, Precision, Recall, F1, AUROC)
- [x] Train and evaluate Ensemble Models (Random Forest and XGBoost Classifier)
- [x] Systematic Hyperparameter Tuning for XGBoost Classifier via Grid Search CV

### 🌲 Stage 4: Explainability (SHAP)
- [x] Extract and process XGBoost features for SHAP Explainer
- [x] Generate Global Explanations (SHAP Summary Plot)
- [x] Generate Local Explanations (Waterfall & Force Plots for individual customers)
- [x] Document key business insights from feature importances

### 📉 Stage 5: Regression & Learning Curves
- [x] Build target `y_reg` (`tenure`) and feature matrix `X_reg` (dropping leakage variables `tenure` and `TotalCharges`)
- [x] Train baseline `DecisionTreeRegressor` and evaluate metrics (RMSE, MAE, R²)
- [x] Train regularized `XGBRegressor` and compare performances
- [x] Plot Learning Curves using `learning_curve` cross-validation to analyze Bias-Variance tradeoffs
- [x] Verify tree model predictions are strictly bounded by training range outputs (extrapolation check)

### 📦 Stage 6: Production Serialization
- [x] Fit final classification pipeline on the complete training set
- [x] Save pipeline to disk as `telco_churn_pipeline_v1.joblib`
- [x] Verify reload and production inference on testing data
