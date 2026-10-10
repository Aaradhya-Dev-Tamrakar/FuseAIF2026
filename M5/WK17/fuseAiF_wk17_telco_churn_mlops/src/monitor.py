"""Evidently AI drift monitoring engine for Telco Customer Churn MLOps pipeline.

Generates Data Drift, Target Drift, and Custom Metric Test reports comparing
reference (training-time) vs current (production) datasets, with deliberately
injected synthetic drift to validate detection capability.
"""

from __future__ import annotations

import os
from pathlib import Path

import mlflow
import pandas as pd
from evidently.legacy.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.legacy.report import Report
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests import (
    TestColumnDrift,
    TestColumnValueMean,
    TestShareOfDriftedColumns,
)

from src.data import PROCESSED_DIR, TARGET_COLUMN, prepare_and_save_data
from src.train import MLFLOW_TRACKING_URI

os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

REPORTS_DIR = Path("reports")
EXPERIMENT_NAME = "TelcoChurn_Prediction_Benchmark"


def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load reference and current (drifted) datasets from processed parquet files."""
    ref_path = PROCESSED_DIR / "reference.parquet"
    curr_path = PROCESSED_DIR / "current.parquet"

    if not ref_path.exists() or not curr_path.exists():
        print("[monitor.py] Processed datasets missing, generating now...")
        prepare_and_save_data()

    ref_df = pd.read_parquet(ref_path)
    curr_df = pd.read_parquet(curr_path)

    return ref_df, curr_df


def run_data_drift_report(
    ref_df: pd.DataFrame, curr_df: pd.DataFrame
) -> Report:
    """Generate Evidently Data Drift report comparing reference vs current feature distributions.

    Verifies that injected drift in MonthlyCharges (+$28.50 shift) and Contract
    (Month-to-month skewed to 85%) is statistically detected.
    """
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref_df, current_data=curr_df)
    return report


def run_target_drift_report(
    ref_df: pd.DataFrame, curr_df: pd.DataFrame
) -> Report:
    """Generate Evidently Target Drift report analyzing churn rate distribution shift."""
    report = Report(metrics=[TargetDriftPreset()])
    report.run(reference_data=ref_df, current_data=curr_df)
    return report


def run_custom_metric_tests(
    ref_df: pd.DataFrame, curr_df: pd.DataFrame
) -> TestSuite:
    """Run custom Evidently Test Suite with domain-specific drift assertions.

    Custom tests:
    1. TestColumnValueMean on MonthlyCharges: Assert mean is within reference +/- $15.
       This INTENTIONALLY FAILS because we injected +$28.50 shift, proving test efficacy.
    2. TestColumnDrift on MonthlyCharges: Confirms statistical drift detection.
    3. TestColumnDrift on Contract: Confirms categorical skew detection.
    4. TestShareOfDriftedColumns: Assert <25% of features drifted (overall health check).
    """
    # Compute reference mean for MonthlyCharges to set bounds
    ref_mean = float(ref_df["MonthlyCharges"].mean())
    lower_bound = ref_mean - 15.0
    upper_bound = ref_mean + 15.0

    suite = TestSuite(
        tests=[
            # Custom metric: Mean MonthlyCharges must stay within $15 of reference
            # This WILL FAIL on our drifted data (+$28.50 shift) — proving test efficacy
            TestColumnValueMean(
                column_name="MonthlyCharges",
                gte=lower_bound,
                lte=upper_bound,
            ),
            # Drift detection on specifically perturbed columns
            TestColumnDrift(column_name="MonthlyCharges"),
            TestColumnDrift(column_name="Contract"),
            # Overall dataset drift health
            TestShareOfDriftedColumns(lte=0.25),
        ]
    )
    suite.run(reference_data=ref_df, current_data=curr_df)
    return suite


def save_reports_and_log_to_mlflow(
    data_drift_report: Report,
    target_drift_report: Report,
    custom_test_suite: TestSuite,
) -> dict:
    """Save HTML reports to disk and log as MLflow artifacts with drift summary metrics."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Save HTML reports
    data_drift_path = REPORTS_DIR / "data_drift_report.html"
    target_drift_path = REPORTS_DIR / "target_drift_report.html"
    custom_tests_path = REPORTS_DIR / "custom_drift_tests.html"

    data_drift_report.save_html(str(data_drift_path))
    target_drift_report.save_html(str(target_drift_path))
    custom_test_suite.save_html(str(custom_tests_path))

    print(f"[monitor.py] Saved Data Drift report to {data_drift_path}")
    print(f"[monitor.py] Saved Target Drift report to {target_drift_path}")
    print(f"[monitor.py] Saved Custom Tests report to {custom_tests_path}")

    # Extract drift summary from report JSON
    data_drift_json = data_drift_report.as_dict()
    drift_metrics = extract_drift_summary(data_drift_json)

    # Extract test suite results
    test_results = custom_test_suite.as_dict()
    test_summary = extract_test_summary(test_results)

    # Log to MLflow
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run(run_name="Evidently_Drift_Monitoring") as run:
        # Log drift metrics
        mlflow.log_metrics(drift_metrics)
        mlflow.log_metrics(test_summary)

        # Log HTML reports as artifacts
        mlflow.log_artifact(str(data_drift_path), artifact_path="evidently_reports")
        mlflow.log_artifact(str(target_drift_path), artifact_path="evidently_reports")
        mlflow.log_artifact(str(custom_tests_path), artifact_path="evidently_reports")

        # Log parameters describing monitoring configuration
        mlflow.log_params(
            {
                "monitor_type": "synthetic_drift_validation",
                "reference_size": len(load_datasets()[0]),
                "current_size": len(load_datasets()[1]),
                "injected_charge_shift": 28.50,
                "injected_contract_skew": 0.85,
                "injected_label_flip_rate": 0.08,
            }
        )

        print(f"\n[monitor.py] Logged monitoring results to MLflow run {run.info.run_id}")

    all_metrics = {**drift_metrics, **test_summary}
    return all_metrics


def extract_drift_summary(report_dict: dict) -> dict:
    """Extract key drift metrics from Evidently Data Drift report JSON."""
    metrics = {}
    try:
        for result in report_dict.get("metrics", []):
            metric_result = result.get("result", {})
            # DataDriftTable or DatasetDrift metric
            if "share_of_drifted_columns" in metric_result:
                metrics["share_of_drifted_columns"] = float(
                    metric_result["share_of_drifted_columns"]
                )
                metrics["number_of_drifted_columns"] = int(
                    metric_result["number_of_drifted_columns"]
                )
                metrics["number_of_columns"] = int(
                    metric_result["number_of_columns"]
                )
                metrics["dataset_drift"] = int(metric_result.get("dataset_drift", False))
            # Individual column drift
            drift_by_column = metric_result.get("drift_by_columns", {})
            for col_name, col_data in drift_by_column.items():
                if col_name in ("MonthlyCharges", "Contract", "Churn"):
                    drift_detected = col_data.get("drift_detected", False)
                    metrics[f"drift_detected_{col_name}"] = int(drift_detected)
                    if "drift_score" in col_data:
                        metrics[f"drift_score_{col_name}"] = round(
                            float(col_data["drift_score"]), 6
                        )
    except Exception as e:
        print(f"[monitor.py] Warning: Could not fully parse drift report: {e}")

    return metrics


def extract_test_summary(test_dict: dict) -> dict:
    """Extract pass/fail summary from Evidently Test Suite JSON."""
    metrics = {}
    try:
        tests = test_dict.get("tests", [])
        total = len(tests)
        passed = sum(1 for t in tests if t.get("status", "") == "SUCCESS")
        failed = total - passed

        metrics["custom_tests_total"] = total
        metrics["custom_tests_passed"] = passed
        metrics["custom_tests_failed"] = failed
        metrics["custom_tests_pass_rate"] = round(passed / total, 4) if total > 0 else 0.0
    except Exception as e:
        print(f"[monitor.py] Warning: Could not parse test suite results: {e}")

    return metrics


def print_drift_interpretation(metrics: dict) -> None:
    """Print human-readable interpretation of drift monitoring results."""
    print("\n" + "=" * 80)
    print("DRIFT MONITORING INTERPRETATION")
    print("=" * 80)

    n_drifted = metrics.get("number_of_drifted_columns", "?")
    n_total = metrics.get("number_of_columns", "?")
    share = metrics.get("share_of_drifted_columns", 0)
    print(f"\n[Dataset Drift] {n_drifted}/{n_total} columns drifted ({share:.1%})")

    mc_drift = metrics.get("drift_detected_MonthlyCharges", "?")
    mc_score = metrics.get("drift_score_MonthlyCharges", "?")
    print(f"  - MonthlyCharges: drift_detected={mc_drift}, p-value/score={mc_score}")
    print(f"    Interpretation: +$28.50 shift was {'correctly flagged' if mc_drift else 'NOT detected (unexpected)'}.")

    ct_drift = metrics.get("drift_detected_Contract", "?")
    ct_score = metrics.get("drift_score_Contract", "?")
    print(f"  - Contract: drift_detected={ct_drift}, p-value/score={ct_score}")
    print(f"    Interpretation: Month-to-month oversample to 85% was {'correctly flagged' if ct_drift else 'NOT detected (unexpected)'}.")

    ch_drift = metrics.get("drift_detected_Churn", "?")
    print(f"  - Churn (target): drift_detected={ch_drift}")
    print(f"    Interpretation: 8% label flip in high-charge bracket {'shifted target distribution' if ch_drift else 'did not significantly shift target'}.")

    tests_passed = metrics.get("custom_tests_passed", "?")
    tests_total = metrics.get("custom_tests_total", "?")
    tests_failed = metrics.get("custom_tests_failed", "?")
    print(f"\n[Custom Tests] {tests_passed}/{tests_total} passed, {tests_failed} failed")
    print("  - TestColumnValueMean(MonthlyCharges): Expected FAIL (mean shifted +$28.50 > $15 threshold)")
    print("    This intentional failure PROVES the custom test is effective at catching production drift.")

    print("\n[Production Implication]")
    print("  If this drift were detected in a real production pipeline, the recommended action would be:")
    print("  1. Alert the ML engineering team via Airflow/PagerDuty.")
    print("  2. Investigate root cause: pricing revisions or contract distribution shift?")
    print("  3. Trigger model retraining on the new data distribution to prevent performance degradation.")
    print("=" * 80)


def run_monitoring_pipeline() -> dict:
    """Execute the full Evidently drift monitoring pipeline."""
    print("[monitor.py] Loading reference and current datasets...")
    ref_df, curr_df = load_datasets()

    print(f"[monitor.py] Reference: {len(ref_df)} rows, Current: {len(curr_df)} rows")
    print(f"[monitor.py] Reference MonthlyCharges mean: ${ref_df['MonthlyCharges'].mean():.2f}")
    print(f"[monitor.py] Current MonthlyCharges mean:   ${curr_df['MonthlyCharges'].mean():.2f}")
    print(
        f"[monitor.py] Reference Month-to-month %: {(ref_df['Contract'] == 'Month-to-month').mean():.1%}"
    )
    print(
        f"[monitor.py] Current Month-to-month %:   {(curr_df['Contract'] == 'Month-to-month').mean():.1%}"
    )
    print(f"[monitor.py] Reference Churn rate: {ref_df[TARGET_COLUMN].mean():.1%}")
    print(f"[monitor.py] Current Churn rate:   {curr_df[TARGET_COLUMN].mean():.1%}")

    print("\n[monitor.py] Generating Data Drift report...")
    data_drift = run_data_drift_report(ref_df, curr_df)

    print("[monitor.py] Generating Target Drift report...")
    target_drift = run_target_drift_report(ref_df, curr_df)

    print("[monitor.py] Running Custom Metric Tests...")
    custom_tests = run_custom_metric_tests(ref_df, curr_df)

    print("[monitor.py] Saving reports and logging to MLflow...")
    metrics = save_reports_and_log_to_mlflow(data_drift, target_drift, custom_tests)

    print_drift_interpretation(metrics)

    return metrics


if __name__ == "__main__":
    run_monitoring_pipeline()
