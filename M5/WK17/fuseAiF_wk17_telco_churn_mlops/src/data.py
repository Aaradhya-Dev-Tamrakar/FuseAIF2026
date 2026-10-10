"""Data ingestion, cleaning, splitting, preprocessing, and synthetic drift injection for Telco Customer Churn."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RAW_DATA_PATH = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
PROCESSED_DIR = Path("data/processed")

NUMERICAL_FEATURES = ["tenure", "MonthlyCharges", "TotalCharges"]
CATEGORICAL_FEATURES = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]
TARGET_COLUMN = "Churn"


def load_raw_data(filepath: str | Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load raw Telco Customer Churn CSV dataset."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found at {path.resolve()}")
    df = pd.read_csv(path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw dataframe: handle missing TotalCharges, encode Churn, drop identifiers."""
    df_clean = df.copy()

    # Drop customerID identifier
    if "customerID" in df_clean.columns:
        df_clean = df_clean.drop(columns=["customerID"])

    # Coerce TotalCharges whitespace to NaN and impute 0 for tenure == 0
    if "TotalCharges" in df_clean.columns:
        df_clean["TotalCharges"] = pd.to_numeric(
            df_clean["TotalCharges"].astype(str).str.strip(), errors="coerce"
        )
        df_clean["TotalCharges"] = df_clean["TotalCharges"].fillna(0.0)

    # Encode target to integer binary (1 for Yes, 0 for No)
    if TARGET_COLUMN in df_clean.columns:
        if not pd.api.types.is_numeric_dtype(df_clean[TARGET_COLUMN]):
            df_clean[TARGET_COLUMN] = (
                df_clean[TARGET_COLUMN].astype(str).str.strip().map({"Yes": 1, "No": 0}).fillna(0).astype(int)
            )
        else:
            df_clean[TARGET_COLUMN] = df_clean[TARGET_COLUMN].astype(int)

    # Ensure SeniorCitizen is treated as int
    if "SeniorCitizen" in df_clean.columns:
        df_clean["SeniorCitizen"] = df_clean["SeniorCitizen"].astype(int)

    return df_clean


def split_reference_current(
    df: pd.DataFrame, reference_ratio: float = 0.70, random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Perform stratified split into Reference (training-time baseline) and Current (production stream)."""
    stratify_col = df[TARGET_COLUMN] if TARGET_COLUMN in df.columns else None
    ref_df, curr_df = train_test_split(
        df,
        train_size=reference_ratio,
        random_state=random_state,
        stratify=stratify_col,
    )
    return ref_df.reset_index(drop=True), curr_df.reset_index(drop=True)


def inject_synthetic_drift(
    current_df: pd.DataFrame,
    charge_shift: float = 28.50,
    month_to_month_target_ratio: float = 0.85,
    label_flip_rate: float = 0.08,
    random_state: int = 42,
) -> pd.DataFrame:
    """Inject deliberate synthetic drift into the incoming production dataset.

    Perturbations:
    1. Numeric Shift: Add constant offset +$28.50 to MonthlyCharges (simulating pricing revisions/inflation).
    2. Categorical Skew: Resample Contract so 'Month-to-month' reaches ~85% frequency (simulating customer shift).
    3. Concept/Target Drift: Flip 8% of churn labels in the high-charge bracket.
    """
    rng = np.random.default_rng(random_state)
    drifted = current_df.copy()

    # 1. Numeric Drift: Shift MonthlyCharges
    if "MonthlyCharges" in drifted.columns:
        # Add shift with slight Gaussian jitter around the mean shift
        jitter = rng.normal(loc=0.0, scale=2.5, size=len(drifted))
        drifted["MonthlyCharges"] = np.round(
            np.clip(drifted["MonthlyCharges"] + charge_shift + jitter, a_min=18.0, a_max=180.0),
            2,
        )

    # 2. Categorical Skew: Oversample 'Month-to-month'
    if "Contract" in drifted.columns:
        m2m_mask = drifted["Contract"] == "Month-to-month"
        non_m2m_mask = ~m2m_mask

        m2m_rows = drifted[m2m_mask]
        non_m2m_rows = drifted[non_m2m_mask]

        target_total = len(drifted)
        target_m2m_count = int(target_total * month_to_month_target_ratio)
        target_non_m2m_count = target_total - target_m2m_count

        resampled_m2m = m2m_rows.sample(
            n=target_m2m_count, replace=True, random_state=random_state
        )
        resampled_non_m2m = non_m2m_rows.sample(
            n=min(target_non_m2m_count, len(non_m2m_rows)),
            replace=(target_non_m2m_count > len(non_m2m_rows)),
            random_state=random_state,
        )

        drifted = (
            pd.concat([resampled_m2m, resampled_non_m2m], ignore_index=True)
            .sample(frac=1.0, random_state=random_state)
            .reset_index(drop=True)
        )

    # 3. Label/Concept Drift: Flip labels for 8% of high-monthly-charge customers
    if TARGET_COLUMN in drifted.columns and "MonthlyCharges" in drifted.columns:
        high_charge_indices = drifted[drifted["MonthlyCharges"] > 75.0].index
        flip_size = int(len(high_charge_indices) * label_flip_rate)
        flip_indices = rng.choice(high_charge_indices, size=flip_size, replace=False)
        drifted.loc[flip_indices, TARGET_COLUMN] = 1 - drifted.loc[flip_indices, TARGET_COLUMN]

    return drifted


def build_preprocessor() -> ColumnTransformer:
    """Construct standard ColumnTransformer for Telco churn tabular features."""
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                NUMERICAL_FEATURES,
            ),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )
    return preprocessor


def prepare_and_save_data(
    raw_path: str | Path = RAW_DATA_PATH,
    output_dir: str | Path = PROCESSED_DIR,
    inject_drift: bool = True,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Run full data preparation workflow and save reference & current sets."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df_raw = load_raw_data(raw_path)
    df_clean = clean_data(df_raw)

    ref_df, curr_df = split_reference_current(
        df_clean, reference_ratio=0.70, random_state=random_state
    )

    if inject_drift:
        curr_df = inject_synthetic_drift(curr_df, random_state=random_state)

    # Save to parquet and csv
    ref_df.to_parquet(out_dir / "reference.parquet", index=False)
    ref_df.to_csv(out_dir / "reference.csv", index=False)

    curr_df.to_parquet(out_dir / "current.parquet", index=False)
    curr_df.to_csv(out_dir / "current.csv", index=False)

    print(
        f"[data.py] Saved reference dataset ({len(ref_df)} rows) and current dataset ({len(curr_df)} rows) to {out_dir}"
    )
    return ref_df, curr_df


if __name__ == "__main__":
    prepare_and_save_data()
