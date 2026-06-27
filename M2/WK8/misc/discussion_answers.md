# W8 Forecasting — Discussion Answers (compiled)

**Aaradhya Dev Tamrakar · Fusemachines AI Fellowship 2026 · Wk 8/24**

All answers below cite actual values produced by the executed notebook
(`W8_Forecasting_Assignment.ipynb`), run against the synthetic fallback S&P 500
series (yfinance network access blocked in this environment; see notebook Q1
cell for the documented fallback).

---

### Discussion Q1 — Does near-white-noise ACF make forecasting worthless?

ACF/PACF of log-returns show no statistically significant lags outside the 95%
band (Q5), consistent with the Efficient Market Hypothesis. This does not make
forecasting worthless — well-calibrated uncertainty intervals (prediction bands)
add value for risk management and capital allocation even when point forecasts
cannot beat the random walk. The question is not "can we predict direction?"
but "can we bound the risk?"

---

### Discussion Q2 — Communicating the COVID tail event to an investment committee

A SARIMA model trained on pre-crash data extrapolates the long-run upward
trend, predicting positive or flat returns going into the shock month. Our
test set includes a single-month −34% structural break (synthetic, modeled on
March 2020); SARIMA's point forecast for that month does not anticipate it —
this is not a model failure but a tail event outside the training
distribution by definition. A quant analyst should communicate this to the
investment committee using scenario ranges and conditional forecasts ("if no
regime change, the model projects X; however, macro tail risks are not
quantifiable within this framework") and should always provide the model's
uncertainty intervals rather than point forecasts alone.

---

### Discussion Q3 — Diagnosing the Ljung-Box failure

Our SARIMA(1,1,1)(0,1,1,12) residuals **failed** Ljung-Box at lags 12 and 24
(p ≈ 0.0000 at both) while passing at lag 6 (p = 0.9645). Failure specifically
at the annual-frequency lags (12, 24) indicates unmodeled seasonal
autocorrelation. To fix: increase Q (seasonal MA order) from 1 to 2, or add
P=1 (seasonal AR term), then re-fit and re-run Ljung-Box — all three lags (6,
12, 24) should pass once the seasonal structure is properly captured. We did
not refit within this submission cycle; this is logged as a known follow-up
rather than silently ignored, per the task plan's "document order adjustment
if any failed" requirement.

---

### Discussion Q4 — Does a small MASE gap matter without significance testing?

Our top three single models scored MASE = 2.6556 (Holt-Winters), 2.6971
(SARIMA), and 2.78 (LSTM) — a gap of roughly 0.04–0.12 MASE units between the
leaders. A MASE gap that small does not "count" on its own without a
significance test. We ran a Diebold-Mariano test between the best single model
(Holt-Winters) and a 4-model ensemble: DM stat = 2.69, **p = 0.0092**, which
*does* reject the null of equal predictive accuracy at the 5% level — so in
this case the ensemble's improvement (MASE 2.44 vs 2.66) is unlikely to be
pure noise. The general caution still applies for the single-model gaps above:
with only 60 test months and high serial autocorrelation in financial returns,
small MASE differences between individual models are exactly the kind of gap
that can disappear on the next 60-month window. The investment risk of acting
on an untested gap: committing capital allocation to a model chosen by chance.

---

### Discussion Q5 — Recursive vs direct multi-step forecasting

Recursive forecasting (used by XGBoost, LightGBM, MLP, and LSTM in this
notebook) compounds errors — each predicted value becomes a lag-feature input
for the next step. On a near-random-walk series like the S&P 500, this
compounding shows up directly in our Q21 horizon-error plot: MAE grows with
horizon and the gap between models narrows as h increases, because all
recursive forecasters converge toward the same long-run drift once the
short-horizon autocorrelation information is exhausted (roughly by h=12, the
1-year mark, in our results). Direct forecasting trains one model per horizon
h, so errors don't compound; however it requires H separate models (60 in our
case) and loses the autocorrelation information that recursive implicitly
uses at short horizons (h=1–3).

---

### Discussion Q6 — Hierarchical reconciliation (Bottom-Up / Top-Down / MinT)

**Bottom-Up:** forecast each constituent stock, then sum → better stock-level
accuracy, but aggregation compounds errors at the portfolio level.
**Top-Down:** forecast the S&P 500 index, then disaggregate by market-cap
weights → better portfolio-level accuracy, but weak at individual stock level.
**MinT (Minimum Trace) reconciliation** projects all base forecasts onto the
coherent subspace using a GLS estimator that minimizes total forecast
variance — producing forecasts that are both internally consistent and closer
to optimal at every level of the hierarchy. This notebook only forecasts the
aggregate index, so hierarchical reconciliation is noted here as a conceptual
extension rather than implemented.

---

### Discussion Q7 — Diagnosing poor prediction-interval coverage

Our LightGBM quantile-regression 95% prediction interval achieved only
**15.0% empirical coverage** (Q16) — far below the 95% target, and a more
extreme shortfall than the 74% example in the original task draft, which only
sharpens the diagnostic urgency. Two possible causes: (1) **Miscalibration** —
the training distribution (pre-2020) underestimates the variance actually
realized in the test period, so the 2.5th/97.5th quantile bounds are too
narrow relative to the test distribution. (2) **Distributional shift** — the
embedded crash month changes the data-generating process for 2020 onward; the
training-period prior is simply wrong for that regime. Diagnose by splitting
the test set and checking coverage on the crash year vs the remaining years
separately: if the crash year drives the bulk of the gap, it's distributional
shift; if coverage is uniformly low across all years, it's miscalibration. The
size of our shortfall (15% vs an expected ≈95%) suggests both effects are
likely present, with miscalibration of the LightGBM quantile loss being the
dominant driver since per-month coverage failures appear in non-crash months
too.

---

### Discussion Q8 — Non-accuracy criteria for model selection (regulated context)

With near-identical accuracy among the top models (Holt-Winters 2.6556,
SARIMA 2.6971, LSTM 2.78 MASE) in a monthly equity-allocation context with
regulatory reporting requirements: (1) **Regulatory explainability** —
highest priority; Holt-Winters and SARIMA produce interpretable parameters
(smoothing weights; ARIMA coefficients) and formal confidence intervals that
satisfy model-documentation standards expected by investment committees and
regulators, whereas LSTM and the ML ensemble members are comparatively opaque.
(2) **Refit latency** — monthly data means the model must refit on a routine
cycle; Holt-Winters and SARIMA refit in well under a second to a few seconds
on this dataset size, versus materially longer training time for LightGBM,
XGBoost, and especially the LSTM. (3) **Structural break robustness** — the
model should flag when a crash-like regime is recognized as out-of-distribution
rather than extrapolating silently; none of our models do this natively, which
is why we recommend pairing any deployed model with explicit, well-calibrated
prediction intervals (Q16) rather than relying on point forecasts. On these
criteria, Holt-Winters is the strongest single-model choice for a regulated
deployment, even though the 4-model ensemble edges it out on pure accuracy.
