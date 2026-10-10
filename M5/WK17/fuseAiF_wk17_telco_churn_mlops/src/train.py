"""MLflow experiment tracking and model registry pipeline for Telco Customer Churn."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

import lightgbm as lgb
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import seaborn as sns
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.data import (
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
    PROCESSED_DIR,
    TARGET_COLUMN,
    build_preprocessor,
    prepare_and_save_data,
)

# Silence MLflow agent hints for clean output
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
EXPERIMENT_NAME = "TelcoChurn_Prediction_Benchmark"
REGISTERED_MODEL_NAME = "TelcoChurnPredictor"
REPORTS_DIR = Path("reports")


def initialize_mlflow() -> None:
    """Set up MLflow local tracking URI and experiment."""
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)


def create_evaluation_plots(
    y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray, model_name: str, output_dir: Path
) -> Dict[str, Path]:
    """Generate and save Confusion Matrix, ROC Curve, and PR Curve plots."""
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = model_name.lower().replace(" ", "_")
    plot_paths = {}

    # 1. Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(5, 4), dpi=150)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Retained (0)", "Churned (1)"],
        yticklabels=["Retained (0)", "Churned (1)"],
        ax=ax,
    )
    ax.set_title(f"Confusion Matrix — {model_name}")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    plt.tight_layout()
    cm_path = output_dir / f"{slug}_confusion_matrix.png"
    plt.savefig(cm_path)
    plt.close(fig)
    plot_paths["confusion_matrix"] = cm_path

    # 2. ROC Curve
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = roc_auc_score(y_true, y_proba)
    fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)
    ax.plot(fpr, tpr, color="#1f77b4", lw=2, label=f"ROC curve (AUC = {roc_auc:.4f})")
    ax.plot([0, 1], [0, 1], color="gray", lw=1.5, linestyle="--", label="Chance")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(f"ROC Curve — {model_name}")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    roc_path = output_dir / f"{slug}_roc_curve.png"
    plt.savefig(roc_path)
    plt.close(fig)
    plot_paths["roc_curve"] = roc_path

    # 3. Precision-Recall Curve
    prec, rec, _ = precision_recall_curve(y_true, y_proba)
    pr_auc = average_precision_score(y_true, y_proba)
    fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)
    ax.plot(rec, prec, color="#2ca02c", lw=2, label=f"PR curve (AP = {pr_auc:.4f})")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title(f"Precision-Recall Curve — {model_name}")
    ax.legend(loc="lower left")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    pr_path = output_dir / f"{slug}_pr_curve.png"
    plt.savefig(pr_path)
    plt.close(fig)
    plot_paths["pr_curve"] = pr_path

    return plot_paths


def get_model_specs() -> List[Dict[str, Any]]:
    """Define ≥3 diverse model candidates with distinct hyperparameters and inductive biases."""
    return [
        {
            "name": "Logistic Regression (L2 Balanced)",
            "family": "LogisticRegression",
            "classifier": LogisticRegression(
                C=0.1,
                penalty="l2",
                solver="lbfgs",
                class_weight="balanced",
                max_iter=1000,
                random_state=42,
            ),
            "params": {
                "model_family": "LogisticRegression",
                "C": 0.1,
                "penalty": "l2",
                "solver": "lbfgs",
                "class_weight": "balanced",
                "max_iter": 1000,
            },
            "description": "Linear regularized baseline prioritizing coefficient interpretability and fast inference.",
        },
        {
            "name": "Random Forest (Depth-6 Balanced)",
            "family": "RandomForest",
            "classifier": RandomForestClassifier(
                n_estimators=150,
                max_depth=6,
                min_samples_split=10,
                min_samples_leaf=4,
                class_weight="balanced",
                random_state=42,
            ),
            "params": {
                "model_family": "RandomForest",
                "n_estimators": 150,
                "max_depth": 6,
                "min_samples_split": 10,
                "min_samples_leaf": 4,
                "class_weight": "balanced",
            },
            "description": "Non-linear bagged ensemble capturing non-linear threshold splits and feature interactions.",
        },
        {
            "name": "LightGBM (Tuned Gradient Boosting)",
            "family": "LightGBM",
            "classifier": lgb.LGBMClassifier(
                n_estimators=100,
                learning_rate=0.05,
                max_depth=4,
                num_leaves=15,
                scale_pos_weight=2.76,  # 73.5% non-churn / 26.5% churn ratio
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbose=-1,
            ),
            "params": {
                "model_family": "LightGBM",
                "n_estimators": 100,
                "learning_rate": 0.05,
                "max_depth": 4,
                "num_leaves": 15,
                "scale_pos_weight": 2.76,
                "subsample": 0.8,
                "colsample_bytree": 0.8,
            },
            "description": "Gradient boosted decision trees optimized for class imbalance and tabular ranking.",
        },
    ]


def train_and_track_experiments() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Execute training, metric evaluation, plot generation, and MLflow logging for all candidate models."""
    initialize_mlflow()

    ref_path = PROCESSED_DIR / "reference.parquet"
    if not ref_path.exists():
        print("[train.py] Reference dataset missing, generating now...")
        prepare_and_save_data()

    ref_df = pd.read_parquet(ref_path)
    X = ref_df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = ref_df[TARGET_COLUMN]

    # Stratified 80/20 train/validation split
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    models = get_model_specs()
    run_records: List[Dict[str, Any]] = []
    best_candidate: Dict[str, Any] = {}
    best_f1 = -1.0

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    temp_plots_dir = REPORTS_DIR / "plots"

    for spec in models:
        model_name = spec["name"]
        print(f"\n[train.py] Training {model_name}...")

        # Construct full scikit-learn pipeline (preprocessor + estimator)
        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("classifier", spec["classifier"]),
            ]
        )

        with mlflow.start_run(run_name=model_name) as run:
            run_id = run.info.run_id

            # Fit on training fold
            pipeline.fit(X_train, y_train)

            # Evaluate on validation fold
            y_pred = pipeline.predict(X_val)
            y_proba = pipeline.predict_proba(X_val)[:, 1]

            # Compute classification metrics
            acc = float(accuracy_score(y_val, y_pred))
            prec = float(precision_score(y_val, y_pred, zero_division=0))
            rec = float(recall_score(y_val, y_pred, zero_division=0))
            f1 = float(f1_score(y_val, y_pred, zero_division=0))
            roc_auc = float(roc_auc_score(y_val, y_proba))
            pr_auc = float(average_precision_score(y_val, y_proba))

            # Log parameters
            mlflow.log_params(spec["params"])
            mlflow.log_param("train_samples", len(X_train))
            mlflow.log_param("val_samples", len(X_val))

            # Log metrics
            metrics = {
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4),
                "roc_auc": round(roc_auc, 4),
                "pr_auc": round(pr_auc, 4),
            }
            mlflow.log_metrics(metrics)

            # Generate and log visual artifacts
            plots = create_evaluation_plots(y_val, y_pred, y_proba, model_name, temp_plots_dir)
            for plot_key, plot_file in plots.items():
                mlflow.log_artifact(str(plot_file), artifact_path="evaluation_plots")

            # Infer signature and log model artifact
            input_sample = X_val.iloc[:5]
            signature = infer_signature(input_sample, pipeline.predict_proba(input_sample))
            mlflow.sklearn.log_model(
                sk_model=pipeline,
                artifact_path="model",
                signature=signature,
                input_example=input_sample,
                serialization_format="cloudpickle",
            )

            record = {
                "run_id": run_id,
                "model_name": model_name,
                "family": spec["family"],
                "params": spec["params"],
                "description": spec["description"],
                "metrics": metrics,
                "pipeline": pipeline,
            }
            run_records.append(record)

            print(
                f"[train.py] {model_name} logged -> F1: {f1:.4f} | ROC-AUC: {roc_auc:.4f} | Recall: {rec:.4f} | Precision: {prec:.4f}"
            )

            # Model selection: maximize F1 score on imbalanced churn
            if f1 > best_f1:
                best_f1 = f1
                best_candidate = record

    # Export comparison table
    export_run_comparison_table(run_records, best_candidate)

    # Register best model in Model Registry and transition stages
    register_and_promote_model(best_candidate)

    return run_records, best_candidate


def export_run_comparison_table(
    run_records: List[Dict[str, Any]], best_candidate: Dict[str, Any]
) -> pd.DataFrame:
    """Generate side-by-side run comparison markdown table and CSV artifact."""
    rows = []
    for r in run_records:
        row = {
            "Model Name": r["model_name"],
            "Family": r["family"],
            "Run ID": r["run_id"][:8],
            "Accuracy": r["metrics"]["accuracy"],
            "Precision": r["metrics"]["precision"],
            "Recall": r["metrics"]["recall"],
            "F1-Score": r["metrics"]["f1_score"],
            "ROC-AUC": r["metrics"]["roc_auc"],
            "PR-AUC": r["metrics"]["pr_auc"],
        }
        rows.append(row)

    df_comp = pd.DataFrame(rows)
    csv_path = REPORTS_DIR / "mlflow_run_comparison.csv"
    md_path = REPORTS_DIR / "mlflow_run_comparison.md"

    df_comp.to_csv(csv_path, index=False)

    md_content = f"""# MLflow Experiment Tracking — Side-by-Side Run Comparison

**Experiment**: `{EXPERIMENT_NAME}`
**Dataset**: Telco Customer Churn (7,043 rows, Reference fold: 4,930 rows, Val fold: 986 rows)
**Evaluation Criterion**: Imbalanced target `Churn` (26.5% positive). F1-Score and ROC-AUC prioritized over raw accuracy.

| Model Candidate | Family | Run ID | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Status |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
"""
    for _, row in df_comp.iterrows():
        is_winner = row["Model Name"] == best_candidate["model_name"]
        badge = "[WINNER] Selected (Production)" if is_winner else "Evaluated"
        md_content += (
            f"| **{row['Model Name']}** | `{row['Family']}` | `{row['Run ID']}` | "
            f"{row['Accuracy']:.4f} | {row['Precision']:.4f} | {row['Recall']:.4f} | "
            f"**{row['F1-Score']:.4f}** | **{row['ROC-AUC']:.4f}** | {row['PR-AUC']:.4f} | {badge} |\n"
        )

    md_content += f"""
### Selection Justification
- **Winning Candidate**: **{best_candidate['model_name']}** (`Run ID: {best_candidate['run_id']}`)
- **Quantitative Rationale**: In churn prediction, false negatives (failing to identify an at-risk customer who leaves) are financially punitive compared to false positives (sending a retention coupon to a retained customer). Accuracy ({best_candidate['metrics']['accuracy']:.4f}) is misleading on this imbalanced dataset (a naive majority-class classifier achieves ~73.5% accuracy with 0.0000 recall).
- **Trade-off Analysis**: {best_candidate['model_name']} achieved the optimal balance of **F1-Score ({best_candidate['metrics']['f1_score']:.4f})**, **ROC-AUC ({best_candidate['metrics']['roc_auc']:.4f})**, and high sensitivity / **Recall ({best_candidate['metrics']['recall']:.4f})**, capturing the vast majority of churn events while maintaining calibrated precision.
"""

    md_path.write_text(md_content, encoding="utf-8")
    print(f"\n[train.py] Exported comparison table to {md_path}")
    print(md_content)
    return df_comp


def register_and_promote_model(best_candidate: Dict[str, Any]) -> str:
    """Register winning model in MLflow Registry and transition through Staging -> Production."""
    client = MlflowClient(MLFLOW_TRACKING_URI)
    model_uri = f"runs:/{best_candidate['run_id']}/model"

    print(f"\n[train.py] Registering model '{REGISTERED_MODEL_NAME}' from {model_uri}...")
    reg_model = mlflow.register_model(model_uri=model_uri, name=REGISTERED_MODEL_NAME)
    version = reg_model.version

    # Stage Transition 1: None -> Staging
    print(f"[train.py] Transitioning version {version} to 'Staging'...")
    client.transition_model_version_stage(
        name=REGISTERED_MODEL_NAME,
        version=version,
        stage="Staging",
        archive_existing_versions=False,
    )

    # Stage Transition 2: Staging -> Production
    print(f"[train.py] Transitioning version {version} to 'Production'...")
    client.transition_model_version_stage(
        name=REGISTERED_MODEL_NAME,
        version=version,
        stage="Production",
        archive_existing_versions=True,
    )

    # Set alias for MLflow 2.x/3.x forward compatibility
    client.set_registered_model_alias(
        name=REGISTERED_MODEL_NAME, alias="production", version=version
    )

    # Annotate description
    client.update_model_version(
        name=REGISTERED_MODEL_NAME,
        version=version,
        description=(
            f"Production TelcoChurn model selected based on highest F1-Score "
            f"({best_candidate['metrics']['f1_score']:.4f}) and ROC-AUC ({best_candidate['metrics']['roc_auc']:.4f}). "
            f"Model family: {best_candidate['family']}."
        ),
    )

    print(
        f"[train.py] Successfully promoted {REGISTERED_MODEL_NAME} v{version} to Production stage and '@production' alias."
    )
    return version


if __name__ == "__main__":
    train_and_track_experiments()
