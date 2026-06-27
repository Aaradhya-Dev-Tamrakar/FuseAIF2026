# W8 Forecasting — AI Prompt Critique Log

**Aaradhya Dev Tamrakar · Fusemachines AI Fellowship 2026 · Wk 8/24**

One entry per AI-assisted prompt used while building the notebook, per the
task plan's critique-log requirement.

---

## Phase 0 — Stationarity (Jun 27)
**What it got right:** Ran ADF + KPSS on both `log_series` and `log_returns`
(Q4) and correctly explained the standard interpretation: log-prices show a
unit root (ADF fails to reject, KPSS rejects stationarity) while log-returns
are consistent with stationarity — matching the textbook stochastic-trend
story for asset prices vs near-stationary returns.
**What it got wrong / needed push-back:** Initial draft only ran ADF on
log-returns and skipped KPSS entirely on the grounds that "ADF is sufficient
for return series." Pushed back since the task plan explicitly requires both
tests on both series to surface the case where ADF and KPSS could disagree;
after push-back, KPSS was added for both series.
**Verdict:** Useful (after one correction).

## Phase 1 — SARIMA diagnostics (Jun 27)
**What it got right:** Correctly flagged that a Ljung-Box p-value < 0.05
means the SARIMA order must be re-specified, not ignored — and that for
near-white-noise log-returns, ARIMA(0,1,0) is the random-walk-equivalent
order (no AR or MA terms beyond the single difference).
**What it got wrong / needed push-back:** In our actual run, Ljung-Box failed
at lags 12 and 24 (p≈0.0000) on the fitted SARIMA(1,1,1)(0,1,1,12) — annual
seasonal lags specifically. The initial suggestion was to simply "increase
the AR order p" generically; pushed back to confirm the *seasonal* MA/AR
terms (P, Q) are the correct lever for a failure concentrated at multiples of
12, not the non-seasonal order. Final answer correctly recommended Q→2 or
P→1, which is logged here as the recommended next step (not yet refit in this
submission cycle — see Discussion Q3).
**Verdict:** Partially useful (correct framework, needed redirect to the
seasonal-specific fix).

## Phase 2 — Prophet changepoints (Jun 27)
**What it got right:** Explained that Prophet's changepoints model growth-rate
changes (slope changes in the piecewise-linear trend), not instantaneous level
jumps, and that the changepoint magnitudes follow a Laplace(0, τ) prior where
`changepoint_prior_scale` sets τ — larger values place more probability mass
on large rate changes, i.e. a more flexible trend.
**What it got wrong / needed push-back:** Initially described
`changepoint_prior_scale=0.05` (Prophet's library default) as "usually fine
for any series." Pushed back given financial data has frequent regime shifts;
the model correctly revised its answer to explain why 0.05 is too rigid for
finance and why our notebook's choice of 0.5 better accommodates abrupt
regime changes like a crash month, at the cost of a noisier-looking trend fit.
**Verdict:** Useful (after push-back on the default-value framing).

## Phase 2–3 — Walk-forward CV (Jun 28)
**What it got right:** Correctly explained that standard `KFold` shuffles
the time index, so a fold could end up training on 2020 data to predict 2019
— future information leaking into the past — which is economically
nonsensical for a financial series. `TimeSeriesSplit` (used in Q14) avoids
this by always expanding the training window forward in time.
**What it got wrong / needed push-back:** First explanation was correct but
generic; asked it to state explicitly which of our four folds (2016, 2017,
2018, 2019 validation years) would be most exposed to this leakage under
plain `KFold`, to ground the explanation in our actual fold structure rather
than an abstract example.
**Verdict:** Useful (after asking for fold-specific grounding).

## Phase 3 — LSTM shape (Jun 28)
**What it got right:** Stated the correct 3D input shape `(samples,
LOOKBACK, 1)` for the Keras LSTM, described the recursive forecasting loop
(append the scaled prediction, not the raw log price, to the window buffer),
and confirmed `inverse_transform` must be applied only once at the end, after
collecting all H scaled predictions — not per-step.
**What it got wrong / needed push-back:** An early draft of the recursive
loop appended the unscaled log-price prediction to the scaled window buffer,
which would have silently corrupted every subsequent step's input scale.
Pushed back after noticing the buffer mixed scaled and unscaled values; the
corrected version (used in the final Q18 cell) appends `pred_sc` — the
still-scaled prediction — consistently.
**Verdict:** Partially useful (caught a subtle scale-mixing bug only on
review).

## Phase 4 — WMAPE vs MAPE (Jun 29)
**What it got right:** Gave the correct WMAPE formula —
`Σ(|e|/y × y) / Σ(y) × 100`, which simplifies to `Σ|e| / Σ(y) × 100` — and
correctly distinguished it from sMAPE (which uses `(|a|+|p|)/2` in the
denominator per-point rather than weighting by the actual value level).
**What it got wrong / needed push-back:** Initially conflated WMAPE with
sMAPE in one sentence, describing them as "two names for the same metric."
Pushed back since our `compute_metrics()` helper computes both separately and
they diverge in our results (e.g. for MLP: MAPE=88.08% vs WMAPE=88.36% —
close but not identical, confirming they are genuinely different
weightings); the model corrected itself and explained that WMAPE weights
errors by the price level, so periods with higher index values (post-2015,
after the S&P roughly tripled from its 1990s base) receive proportionally
more influence on the aggregate score than an unweighted MAPE would give them.
**Verdict:** Useful (after correcting the WMAPE/sMAPE conflation).
