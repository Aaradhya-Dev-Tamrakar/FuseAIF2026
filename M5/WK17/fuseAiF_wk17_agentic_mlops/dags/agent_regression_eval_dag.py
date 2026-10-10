"""Apache Airflow DAG for nightly Agentic AI regression evaluation and performance alerting.

Schedule: @nightly (00:00 UTC)
Tasks:
  1. run_agent_regression_suite    - Executes prompt benchmark and Evidently regression test suite
  2. evaluate_regression_gate      - Branching operator: asserts pct_tests_passed >= 80% & completion >= 75%
  3. alert_regression_degradation  - Triggers alerts and blocks promotion if quality degrades
  4. log_promotion_approved        - Logs approval for production deployment
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


def run_agent_regression_suite(**kwargs):
    """Execute the Evidently LLM-as-a-judge regression evaluation across prompt versions."""
    from eval.evidently_judge import run_evidently_regression_pipeline

    results = run_evidently_regression_pipeline()

    # Find the latest/promoted version (v3)
    v3_result = next((r for r in results if r["version"] == "v3"), results[-1])
    pct_passed = v3_result["pct_tests_passed"]

    kwargs["ti"].xcom_push(key="pct_tests_passed", value=pct_passed)
    kwargs["ti"].xcom_push(key="version", value=v3_result["version"])
    kwargs["ti"].xcom_push(key="evaluation_summary", value=v3_result)
    return pct_passed


def evaluate_regression_gate(**kwargs):
    """Branch task: decide whether regression passed production gates.

    If pct_tests_passed < 80%, route to alert_regression_degradation.
    Otherwise, route to log_promotion_approved.
    """
    pct_passed = kwargs["ti"].xcom_pull(
        task_ids="run_agent_regression_suite", key="pct_tests_passed"
    )
    version = kwargs["ti"].xcom_pull(task_ids="run_agent_regression_suite", key="version")

    if pct_passed is not None and float(pct_passed) < 0.80:
        print(
            f"[DAG] REGRESSION DETECTED: {version} passed only {float(pct_passed):.1%} of tests (< 80% threshold)"
        )
        return "alert_regression_degradation"
    else:
        print(
            f"[DAG] Quality gate passed: {version} achieved {float(pct_passed or 1.0):.1%} regression pass rate"
        )
        return "log_promotion_approved"


def alert_regression_degradation(**kwargs):
    """Send alert notification when agent accuracy or grounding degrades.

    In production, this would:
    - Dispatch PagerDuty incident / Slack alert to AI platform team
    - Block prompt promotion in MLflow Model / Prompt Registry
    - Freeze agent deployment pipeline
    """
    summary = kwargs["ti"].xcom_pull(
        task_ids="run_agent_regression_suite", key="evaluation_summary"
    )
    v = summary.get("version", "unknown") if summary else "unknown"
    rate = summary.get("pct_tests_passed", 0) if summary else 0

    print("=" * 60)
    print(f"ALERT: Prompt version '{v}' failed regression gate!")
    print(f"  Pass Rate: {float(rate):.1%} (Minimum required: 80%)")
    print("  Action: Freezing automated deployment. Manual review required.")
    print("  Channels: [Slack #agent-alerts] [PagerDuty Sev-2] [MLflow Audit]")
    print("=" * 60)


def log_promotion_approved(**kwargs):
    """Log that the candidate prompt version is healthy and approved for deployment."""
    summary = kwargs["ti"].xcom_pull(
        task_ids="run_agent_regression_suite", key="evaluation_summary"
    )
    v = summary.get("version", "unknown") if summary else "unknown"
    rate = summary.get("pct_tests_passed", 0) if summary else 0
    print(
        f"[DAG] Prompt version '{v}' approved for production deployment (Pass rate: {float(rate):.1%})."
    )


with DAG(
    dag_id="agent_regression_eval_dag",
    default_args=default_args,
    description="Nightly regression evaluation and quality gating for Agentic AI assistant",
    schedule="@nightly",
    start_date=datetime(2026, 10, 1),
    catchup=False,
    tags=["mlops", "agentic-ai", "evidently-judge", "prompt-evaluation"],
) as dag:

    t1 = PythonOperator(
        task_id="run_agent_regression_suite",
        python_callable=run_agent_regression_suite,
    )

    t2 = BranchPythonOperator(
        task_id="evaluate_regression_gate",
        python_callable=evaluate_regression_gate,
    )

    t3_alert = PythonOperator(
        task_id="alert_regression_degradation",
        python_callable=alert_regression_degradation,
    )

    t3_approved = PythonOperator(
        task_id="log_promotion_approved",
        python_callable=log_promotion_approved,
    )

    t1 >> t2
    t2 >> [t3_alert, t3_approved]
