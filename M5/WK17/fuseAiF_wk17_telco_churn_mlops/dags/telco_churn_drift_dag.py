"""Apache Airflow DAG for scheduled Telco Customer Churn drift monitoring.

Schedule: @daily
Tasks:
  1. fetch_latest_production_batch  - Simulate fetching new production data batch
  2. run_evidently_drift_check      - Execute Evidently drift reports
  3. evaluate_drift_threshold       - Branch: if drifted features ratio > 25%, alert + trigger retrain
"""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import BranchPythonOperator, PythonOperator

default_args = {
    "owner": "aaradhya",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def fetch_latest_production_batch(**kwargs):
    """Simulate fetching the latest batch of production data.

    In a real deployment, this would pull new customer records from a data warehouse
    (e.g., BigQuery, Snowflake) or streaming pipeline (Kafka -> Delta Lake).
    For this assignment, we load the pre-generated drifted current dataset.
    """
    import pandas as pd

    current_path = "data/processed/current.parquet"
    df = pd.read_parquet(current_path)
    print(f"[DAG] Fetched production batch: {len(df)} rows")
    kwargs["ti"].xcom_push(key="batch_size", value=len(df))
    return len(df)


def run_evidently_drift_check(**kwargs):
    """Execute the full Evidently drift monitoring pipeline and return drift metrics."""
    from src.monitor import run_monitoring_pipeline

    metrics = run_monitoring_pipeline()
    share_drifted = metrics.get("share_of_drifted_columns", 0.0)
    kwargs["ti"].xcom_push(key="share_drifted", value=share_drifted)
    kwargs["ti"].xcom_push(key="drift_metrics", value=metrics)
    return share_drifted


def evaluate_drift_threshold(**kwargs):
    """Branch task: decide whether to alert/retrain or log clean status.

    If >25% of features have drifted, route to alert_and_trigger_retrain.
    Otherwise, route to log_clean_status.
    """
    share_drifted = kwargs["ti"].xcom_pull(
        task_ids="run_evidently_drift_check", key="share_drifted"
    )

    if share_drifted is not None and float(share_drifted) > 0.25:
        print(
            f"[DAG] DRIFT DETECTED: {float(share_drifted):.1%} features drifted (> 25% threshold)"
        )
        return "alert_and_trigger_retrain"
    else:
        print(f"[DAG] No significant drift: {float(share_drifted or 0):.1%} features drifted")
        return "log_clean_status"


def alert_and_trigger_retrain(**kwargs):
    """Send alert notification and trigger model retraining pipeline.

    In production, this would:
    - Send Slack/PagerDuty/email alert to ML engineering team
    - Trigger an Airflow sub-DAG or external CI/CD pipeline for retraining
    - Log the retraining trigger event to MLflow
    """
    metrics = kwargs["ti"].xcom_pull(
        task_ids="run_evidently_drift_check", key="drift_metrics"
    )
    share = metrics.get("share_of_drifted_columns", 0) if metrics else 0

    print("=" * 60)
    print("DRIFT ALERT: Model retraining recommended")
    print(f"  Share of drifted features: {float(share):.1%}")
    print("  Action: Triggering retraining pipeline...")
    print("  Channels: [Slack #ml-alerts] [PagerDuty] [MLflow Event]")
    print("=" * 60)


def log_clean_status(**kwargs):
    """Log that no significant drift was detected."""
    print("[DAG] Model monitoring passed: No significant drift detected. Model remains healthy.")


with DAG(
    dag_id="telco_churn_drift_monitoring",
    default_args=default_args,
    description="Scheduled drift monitoring for Telco Customer Churn prediction model",
    schedule="@daily",
    start_date=datetime(2026, 10, 1),
    catchup=False,
    tags=["mlops", "drift-monitoring", "telco-churn"],
) as dag:

    t1 = PythonOperator(
        task_id="fetch_latest_production_batch",
        python_callable=fetch_latest_production_batch,
    )

    t2 = PythonOperator(
        task_id="run_evidently_drift_check",
        python_callable=run_evidently_drift_check,
    )

    t3 = BranchPythonOperator(
        task_id="evaluate_drift_threshold",
        python_callable=evaluate_drift_threshold,
    )

    t4_alert = PythonOperator(
        task_id="alert_and_trigger_retrain",
        python_callable=alert_and_trigger_retrain,
    )

    t4_clean = PythonOperator(
        task_id="log_clean_status",
        python_callable=log_clean_status,
    )

    t1 >> t2 >> t3
    t3 >> [t4_alert, t4_clean]
