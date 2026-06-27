# Week 5: Tree-Based Models & Ensembles

This repository contains the complete implementation of the **Week 5 Assignment: Tree-Based Models & Ensembles** for the Fusemachines AI Fellowship. The project focuses on predicting customer churn for a telecommunications firm using machine learning classification models, as well as predicting customer tenure using regression architectures.

---

## 📁 Repository Structure

```tree
WK5/
├── W5_Tree-Based Models & Ensembles_Assignment.ipynb   # Fully implemented & executed Jupyter notebook
├── W5_Project_Guide.md                                 # Official assignment guidelines & requirements
├── telco_churn_pipeline_v1.joblib                     # Serialized production pipeline (preprocessors + SMOTE + tuned classifier)
└── README.md                                           # This project documentation
```

---

## 🚀 Key Topics & Implementations

### 1. Mathematical Foundations from Scratch
- **Gini Impurity & Shannon Entropy:** Custom mathematical functions implemented from scratch to calculate split criteria.
- **Information Gain:** Recursive split quality calculation based on parent and child node distributions.
- **Bootstrap Sampling:** Reimplemented bagging mechanics (`bootstrap_sample`) from scratch to build custom ensemble intuition.

### 2. Preventing SMOTE Data Leakage
- **The Leakage Trap:** Applying oversampling (SMOTE) on the entire dataset prior to cross-validation leaks information from validation folds into training folds, yielding over-optimistic evaluation metrics.
- **The Solution:** Leveraged `imblearn.pipeline.Pipeline` (`ImbPipeline`) instead of `sklearn.pipeline.Pipeline`. This encapsulates SMOTE inside the cross-validation loops, ensuring oversampling is **only** performed on training folds.

### 3. Classification Modeling & Hyperparameter Tuning
- Built and evaluated:
  - Naïve Baseline Decision Tree
  - Random Forest Classifier
  - Regularized Gradient Boosted Trees (XGBoost)
- Optimized classification metrics (`AUROC`, `F1-Score`, `Precision`, and `Recall`).
- Conducted hyperparameter tuning for XGBoost using systematically managed cross-validation grids.

### 4. Regression & Learning Curves
- **Tenure Prediction:** Trained a baseline `DecisionTreeRegressor` and a regularized `XGBRegressor` to predict customer `tenure`.
- **Leakage Elimination:** Excluded `TotalCharges` and `tenure` (target) from the regression feature matrix since `TotalCharges` dynamically correlates with `MonthlyCharges * tenure`.
- **Learning Curves:** Computed training and validation curves via `learning_curve` with cross-validation to analyze overfitting tendencies. An unconstrained decision tree demonstrated a Train RMSE $\approx 0$, highlighting extreme high variance, while the regularized XGBoost model showed superior generalization behavior.
- **Extrapolation Check:** Asserted that tree-based model outputs are strictly bounded by training-range maximums (tree structures cannot extrapolate trends outside training leaf values).

### 5. Explainable AI (SHAP)
- Analyzed the model using SHAP (SHapley Additive exPlanations) to explain individual and global predictions.
- Generated global summary plots highlighting how contract types (`Month-to-month`), internet services (`Fiber optic`), and tenure lengths govern churn probabilities.
- Rendered local force and waterfall plots explaining specific customer predictions.

---

## 🛠️ Setup & Execution

### Prerequisites
Make sure you have a Python environment configured with the required dependencies:

```bash
pip install numpy pandas scikit-learn imbalanced-learn xgboost shap joblib matplotlib seaborn jupyter
```

### Executing the Assignment
To open the notebook locally and inspect the completed workflows:
```bash
jupyter notebook W5_Tree-Based Models_&_Ensembles_Assignment.ipynb
```

---

## 🏆 Production-Ready Artifact
The final model is exported to **`telco_churn_pipeline_v1.joblib`**. This artifact packages the entire pipeline end-to-end:
1. **`ColumnTransformer`** (Imputers, scaling, and one-hot encoding).
2. **SMOTE** (Oversampler).
3. **Optimized XGBoost Classifier**.

To load and make predictions in production:
```python
import joblib

# Load pipeline
pipeline = joblib.load("telco_churn_pipeline_v1.joblib")

# Predict on new customer data
predictions = pipeline.predict(new_customer_dataframe)
```
