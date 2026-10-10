"""Tests for the data ingestion, cleaning, splitting, and drift injection pipeline."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.data import (
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
    TARGET_COLUMN,
    build_preprocessor,
    clean_data,
    inject_synthetic_drift,
    load_raw_data,
    split_reference_current,
)


class TestLoadRawData:
    """Tests for raw CSV loading."""

    def test_load_returns_dataframe(self):
        df = load_raw_data()
        assert isinstance(df, pd.DataFrame)

    def test_load_has_expected_shape(self):
        df = load_raw_data()
        assert df.shape == (7043, 21)

    def test_load_has_churn_column(self):
        df = load_raw_data()
        assert "Churn" in df.columns

    def test_load_has_customer_id(self):
        df = load_raw_data()
        assert "customerID" in df.columns


class TestCleanData:
    """Tests for data cleaning logic."""

    @pytest.fixture
    def raw_df(self):
        return load_raw_data()

    @pytest.fixture
    def clean_df(self, raw_df):
        return clean_data(raw_df)

    def test_customer_id_dropped(self, clean_df):
        assert "customerID" not in clean_df.columns

    def test_churn_is_binary_int(self, clean_df):
        assert set(clean_df[TARGET_COLUMN].unique()).issubset({0, 1})

    def test_total_charges_is_numeric(self, clean_df):
        assert pd.api.types.is_numeric_dtype(clean_df["TotalCharges"])

    def test_no_missing_total_charges(self, clean_df):
        assert clean_df["TotalCharges"].isna().sum() == 0

    def test_churn_rate_reasonable(self, clean_df):
        rate = clean_df[TARGET_COLUMN].mean()
        assert 0.15 < rate < 0.40, f"Churn rate {rate:.2%} outside expected range"


class TestSplitData:
    """Tests for stratified train/test splitting."""

    @pytest.fixture
    def splits(self):
        df = clean_data(load_raw_data())
        return split_reference_current(df, reference_ratio=0.70, random_state=42)

    def test_split_sizes(self, splits):
        ref, curr = splits
        total = len(ref) + len(curr)
        assert total == 7043
        assert abs(len(ref) / total - 0.70) < 0.02

    def test_split_preserves_churn_ratio(self, splits):
        ref, curr = splits
        ref_rate = ref[TARGET_COLUMN].mean()
        curr_rate = curr[TARGET_COLUMN].mean()
        assert abs(ref_rate - curr_rate) < 0.05, "Stratification failed: churn rates diverged"


class TestDriftInjection:
    """Tests for synthetic drift injection correctness."""

    @pytest.fixture
    def base_and_drifted(self):
        df = clean_data(load_raw_data())
        _, curr = split_reference_current(df, random_state=42)
        drifted = inject_synthetic_drift(curr, random_state=42)
        return curr, drifted

    def test_monthly_charges_shifted_upward(self, base_and_drifted):
        original, drifted = base_and_drifted
        orig_mean = original["MonthlyCharges"].mean()
        drift_mean = drifted["MonthlyCharges"].mean()
        # Shift is +$28.50 on average
        assert drift_mean > orig_mean + 20, f"Expected significant shift, got {drift_mean - orig_mean:.2f}"

    def test_contract_skew_applied(self, base_and_drifted):
        _, drifted = base_and_drifted
        m2m_ratio = (drifted["Contract"] == "Month-to-month").mean()
        assert m2m_ratio > 0.80, f"Expected >80% Month-to-month, got {m2m_ratio:.1%}"

    def test_drifted_size_preserved(self, base_and_drifted):
        original, drifted = base_and_drifted
        assert len(drifted) == len(original)


class TestPreprocessor:
    """Tests for the sklearn ColumnTransformer preprocessor."""

    def test_preprocessor_fits(self):
        df = clean_data(load_raw_data())
        X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
        preprocessor = build_preprocessor()
        X_transformed = preprocessor.fit_transform(X)
        assert X_transformed.shape[0] == len(df)
        assert X_transformed.shape[1] > len(NUMERICAL_FEATURES)  # One-hot expands columns

    def test_numerical_features_scaled(self):
        df = clean_data(load_raw_data())
        X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
        preprocessor = build_preprocessor()
        X_transformed = preprocessor.fit_transform(X)
        # First 3 columns are numerical (scaled) — should have mean ~0
        num_means = np.abs(X_transformed[:, :3].mean(axis=0))
        assert all(m < 0.1 for m in num_means), f"Numerical columns not properly scaled: {num_means}"
