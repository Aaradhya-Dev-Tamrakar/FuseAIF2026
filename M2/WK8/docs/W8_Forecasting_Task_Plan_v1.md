# W8 Forecasting — Complete Task Plan v1
**Aaradhya Dev Tamrakar · Fusemachines AI Fellowship 2026 · Wk 8/24**
**Period:** Fri Jun 27 → Sun Jun 29, 2026 (sync ~Sun Jun 29)
**Dataset:** Monthly S&P 500 (^GSPC), 1990–2024, via `yfinance`
**Repo:** `fuseAiF_wk8_sp500_forecasting` ← see naming note below
**Facilitator:** Susan Ghimire

---

## Repo Name Decision

**Recommended:** `fuseAiF_wk8_sp500_forecasting`

Rationale:
- Matches Wk7 pattern (`fuseAiF_wk7_customer_segmentation`) — prefix + week + dataset/topic slug
- `sp500` anchors the dataset explicitly (unlike Wk7 where "customer_segmentation" was the task; here the dataset *is* the identity of the work)
- `forecasting` alone is too generic; `sp500_forecasting` is unambiguous on a CV/GitHub scan

Alternative if you prefer shorter: `fuseAiF_wk8_forecasting` — simpler, still consistent.

---

## Repo Structure (mirror Wk7)

```
fuseAiF_wk8_sp500_forecasting/
├── wk8_forecasting.ipynb          ← single executed notebook (all 23 Qs)
├── wk8_forecasting.pdf            ← PDF export of executed notebook
├── sp500_sarima_v1.pkl            ← required submission artifact
├── requirements.txt               ← pinned (pip freeze after final run)
├── README.md
├── LICENSE                        ← MIT
├── .gitignore                     ← *.pkl NOT gitignored (it's a deliverable); exclude: __pycache__/, .ipynb_checkpoints/, *.pyc, .env
├── plots/                         ← all saved figures (ACF, PACF, STL, model forecasts, error breakdown, comparison table)
└── misc/                          ← task plans, debug scripts, scratch notebooks, AI prompt logs
```

---

## Master Execution Plan

### Pre-flight (30 min — do before Day 1 coding)

- [ ] `pip install yfinance statsmodels pmdarima prophet xgboost lightgbm tensorflow scikit-learn matplotlib seaborn pandas numpy`
- [ ] `pip freeze > requirements.txt` after install — pin versions now, not at the end
- [ ] Create repo on GitHub, clone, set up folder structure above
- [ ] Copy `.gitignore` from Wk7 repo; add `*.csv`, `*.xlsx`, `/misc/` is tracked (task plans belong there)
- [ ] Read Project Guide §1 (Your Role) and §4 (Submission Requirements) in full — the business framing drives every model choice

---

## Day 1 (Fri Jun 27) — Phase 0 + Phase 1 (Parts 1–2, Q1–Q10)

**Budget: ~6–7 hrs | Goal: data clean + classical models done**

### Phase 0 — Data Preparation (Q1–Q5)

**Videos first (~26 min):**
- [ ] Time Series Decomposition — ritvikmath (~13 min) ★
- [ ] ACF and PACF Explained — ritvikmath (~13 min) ★

**Q1 — DatetimeIndex setup**
```python
import yfinance as yf, pandas as pd, numpy as np

raw = yf.download('^GSPC', start='1990-01-01', end='2024-12-31',
                  interval='1mo', auto_adjust=True, progress=False)
series = raw['Close'].rename('SP500')
series.index = pd.to_datetime(series.index).tz_localize(None)
series.index.freq = 'MS'

TRAIN_END = '2019-12'
TEST_START = '2020-01'
train = series[:TRAIN_END]   # ~360 months
test  = series[TEST_START:]  # ~60 months (includes COVID crash Mar 2020: −34%)

log_train = np.log(train)
log_price  = np.log(series)
log_ret    = log_price.diff().dropna()
```
- [ ] Print `series.index.dtype`, `series.index.freq`, `len(series)` — confirm assertions pass
- [ ] Synthetic fallback: if `yf.download` fails, generate `pd.date_range('1990-01', periods=420, freq='MS')` with cumulative lognormal walk

**Q2 — Resampling**
- [ ] `.resample('QE').last()` → identify decade with highest mean quarterly return; year with largest crash
- [ ] Save output as a small summary table in a markdown cell

**Q3 — Missing data**
- [ ] Insert 5 NaN values at known indices
- [ ] Compare `ffill`, `bfill`, `interpolate(method='time')` — plot each vs original
- [ ] **Reflect:** `interpolate(method='time')` is best for smooth monthly financial series (ffill creates a plateau; bfill pulls future values backward). Write 2-sentence justification.

**Q4 — Stationarity (ADF + KPSS)**
```python
from statsmodels.tsa.stattools import adfuller, kpss

def stationarity_report(s, name):
    adf = adfuller(s.dropna())
    kp  = kpss(s.dropna(), regression='c', nlags='auto')
    print(f"\n{name}")
    print(f"  ADF  p={adf[1]:.4f}  {'non-stationary' if adf[1]>0.05 else 'stationary'}")
    print(f"  KPSS p={kp[1]:.4f}  {'non-stationary' if kp[1]<0.05 else 'stationary'}")

stationarity_report(log_price, 'log_price')
stationarity_report(log_ret,   'log_returns')
```
- [ ] Both ADF + KPSS on BOTH `log_price` AND `log_ret` — **do not run only ADF**
- [ ] Build stationarity table: 4 rows (2 series × 2 tests), columns: statistic / p-value / conclusion / EMH implication
- [ ] Handle expected conflict: ADF rejects unit root for log_returns → stationary; KPSS may agree. For log_price: ADF fails to reject → unit root (non-stationary); KPSS rejects stationarity. Consistent → price is random walk, returns are approx. stationary.
- [ ] **AI Prompt 0:** Paste Phase 0 prompt → verify it runs BOTH tests + explains conflicting results. Log critique note in `misc/ai_prompt_logs.md`.

**Q5 — ACF/PACF + STL**
```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import STL

fig, axes = plt.subplots(1, 2, figsize=(14,4))
plot_acf(log_ret,  lags=36, ax=axes[0], title='ACF log_returns')
plot_pacf(log_ret, lags=36, ax=axes[1], title='PACF log_returns')
plt.savefig('plots/acf_pacf_log_returns.png', dpi=150, bbox_inches='tight')

stl = STL(log_price, period=12)
res = stl.fit()
res.plot(); plt.savefig('plots/stl_decomposition.png', dpi=150, bbox_inches='tight')
```
- [ ] State whether significant lags exist in log_returns ACF/PACF (expect near-white-noise = EMH consistent)
- [ ] Note STL trend/seasonal/residual structure — residual should dominate for financial data
- [ ] **Discussion Q1 draft:** "ACF/PACF shows no statistically significant lags in log-returns, consistent with EMH. This does not make forecasting worthless — well-calibrated uncertainty intervals (prediction bands) add value for risk management and capital allocation even when point forecasts cannot beat the random walk. The question is not 'can we predict direction?' but 'can we bound the risk?'"

---

### Phase 1 — Classical Models + SARIMA (Q6–Q10)

**Videos (~25 min):**
- [ ] Holt-Winters Exponential Smoothing — Meerkat Statistics (~12 min) ★
- [ ] Coding SARIMA in Python — ritvikmath ★ (watch while doing Q8–Q10 in parallel)

**Q6 — Baselines (MASE=1.0 anchor)**
```python
def mase(y_true, y_pred, y_train, m=12):
    naive_err = np.mean(np.abs(np.diff(y_train.values, n=m)))
    return np.mean(np.abs(y_true.values - y_pred.values)) / naive_err

H = len(test)  # 60

naive_fc = train.shift(1).iloc[-H:].values         # last-value repeat
seas_naive_fc = train.shift(12).iloc[-H:].values   # same month last year

naive_mase = mase(test, pd.Series(naive_fc, index=test.index), train)
assert abs(naive_mase - 1.0) < 0.02, f"Naive MASE should be ~1.0, got {naive_mase:.3f}"
```
- [ ] Store `results = {}` dict; `results['Naive'] = naive_fc`, `results['SeasonalNaive'] = seas_naive_fc`
- [ ] These are the MASE=1.0 denominators — every other model's MASE is judged relative to this

**Q7 — Holt-Winters**
```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

hw = ExponentialSmoothing(log_train, trend='add', seasonal='add',
                          seasonal_periods=12).fit(optimized=True)
hw_fc_log = hw.forecast(H)
hw_fc = np.exp(hw_fc_log)
results['HoltWinters'] = hw_fc.values
```
- [ ] Report α (level), β (trend), γ (seasonal) from `hw.params`
- [ ] Assert `hw_mase < 1.0` — if it fails, check that `np.exp()` inverse-transform was applied before metric computation
- [ ] **Reflect:** which smoothing param dominates? β (trend) likely near-zero given near-random-walk; γ captures weak annual seasonality.

**Q8 — SARIMA identification (Box-Jenkins)**
```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pmdarima as pm

# Identify: from Q5 ACF/PACF of diff(log_train)
# Expect near-ARIMA(0,1,0) or (1,1,1)(0,1,1,12) — let ACF/PACF drive
log_train_diff = log_train.diff().dropna()
fig, axes = plt.subplots(1,2,figsize=(14,4))
plot_acf(log_train_diff,  lags=36, ax=axes[0])
plot_pacf(log_train_diff, lags=36, ax=axes[1])
plt.savefig('plots/acf_pacf_diff_logtrain.png', dpi=150, bbox_inches='tight')

# Fit manual order from visual inspection
sarima = SARIMAX(log_train, order=(1,1,1), seasonal_order=(0,1,1,12),
                 enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
print(sarima.summary())
```
- [ ] Justify chosen (p,d,q)(P,D,Q,12) in a markdown cell — reference ACF/PACF lag cutoffs
- [ ] Report AIC, BIC
- [ ] AutoARIMA cross-check: `auto = pm.auto_arima(log_train, seasonal=True, m=12, information_criterion='aic', stepwise=True)` — compare auto-selected order vs your manual pick

**Q9 — SARIMA diagnostics**
```python
from statsmodels.stats.diagnostic import acorr_ljungbox

lb = acorr_ljungbox(sarima.resid, lags=[6, 12, 24], return_df=True)
print(lb)  # all p > 0.05 required

sarima.plot_diagnostics(figsize=(14,8))
plt.savefig('plots/sarima_diagnostics.png', dpi=150, bbox_inches='tight')
```
- [ ] All Ljung-Box p > 0.05? If lag 12 fails (p < 0.05) → increase seasonal MA order Q (try Q=2) or add seasonal AR term P=1
- [ ] QQ-plot: residuals should track the diagonal; heavy tails acceptable for financial data — note but don't over-correct
- [ ] **AI Prompt 1:** SARIMA diagnostics prompt → verify: (1) Ljung-Box p<0.05 = re-specify, NOT ignore; (2) near-white-noise → ARIMA(0,1,0) = random walk. Log in `misc/ai_prompt_logs.md`.
- [ ] **Discussion Q3 draft:** "Ljung-Box failure at lag 12 specifically indicates unmodeled seasonal autocorrelation at the annual frequency. To fix: increase Q (seasonal MA order) from 1 to 2, or add P=1 (seasonal AR term). Verify fix by re-running Ljung-Box — all three lags (6, 12, 24) should pass."

**Q10 — SARIMA forecast + pickle**
```python
import pickle

fc_obj = sarima.get_forecast(steps=H)
sarima_fc    = np.exp(fc_obj.predicted_mean)
sarima_ci_lo = np.exp(fc_obj.conf_int().iloc[:, 0])
sarima_ci_hi = np.exp(fc_obj.conf_int().iloc[:, 1])
results['SARIMA'] = sarima_fc.values

# Save the pkl — required submission artifact
with open('sp500_sarima_v1.pkl', 'wb') as f:
    pickle.dump(sarima, f)

# Verify it reloads
with open('sp500_sarima_v1.pkl', 'rb') as f:
    sarima_loaded = pickle.load(f)
assert sarima_loaded.get_forecast(12).predicted_mean is not None, "pkl reload failed"
```
- [ ] Plot: train (last 5 years for clarity) + test (actuals) + SARIMA forecast + 95% CI; mark COVID crash (Mar 2020)
- [ ] Save to `plots/sarima_forecast.png`

**Day 1 end check:**
- [ ] Q1–Q10 all have non-None answers
- [ ] All assert cells pass
- [ ] `sp500_sarima_v1.pkl` exists and reloads
- [ ] 5 plot files in `plots/`
- [ ] `results` dict has: Naive, SeasonalNaive, HoltWinters, SARIMA

---

## Day 2 (Sat Jun 28) — Phase 2 + Phase 3 (Parts 3–5, Q11–Q18)

**Budget: ~7–8 hrs | Goal: Prophet + all ML/DL models**

### Phase 2 — Prophet + Feature Engineering (Q11–Q13)

**Video (~30 min):**
- [ ] Prophet — Greg Hogg (~30 min) — watch while Prophet fits (it's slow)

**Q11 — Prophet fit**
```python
from prophet import Prophet

pdf_train = log_train.reset_index()
pdf_train.columns = ['ds', 'y']
pdf_train['ds'] = pdf_train['ds'].dt.tz_localize(None)

m = Prophet(seasonality_mode='additive',
            changepoint_prior_scale=0.5).fit(pdf_train)

future = m.make_future_dataframe(periods=H, freq='MS')
fcst   = m.predict(future)
prophet_fc = np.exp(fcst['yhat'].iloc[-H:].values)
results['Prophet'] = prophet_fc

m.plot_components(fcst); plt.savefig('plots/prophet_components.png', dpi=150)
```
- [ ] Explain in markdown: changepoint_prior_scale=0.5 vs default 0.05. Default is too rigid for volatile financial data — it under-detects the structural breaks (e.g. COVID crash, 2008 GFC). Higher scale = Laplace prior allows more changepoints = more flexible trend line. Not the same as level jumps — changepoints affect slope/growth rate.
- [ ] `np.exp()` before computing metrics — working in log space for fitting, price space for evaluation
- [ ] **AI Prompt 2:** Prophet changepoint prompt → verify: changepoints = growth rate changes (not level jumps), Laplace prior mechanism, why 0.05 is too rigid for finance. Log in `misc/ai_prompt_logs.md`.

**Q12 — Prophet cross-validation**
```python
from prophet.diagnostics import cross_validation, performance_metrics

df_cv   = cross_validation(m, initial='3650 days', period='180 days', horizon='365 days')
df_perf = performance_metrics(df_cv)
print(df_perf[['horizon','rmse','mae','mape']].head(10))
```
- [ ] Report mean RMSE from `df_perf`
- [ ] Compare changepoint_prior_scale=0.05 vs 0.5 (re-fit with 0.05, compare CV RMSE) — note in markdown which performs better
- [ ] W6 GP connection: Prophet's composite kernel ≈ piecewise trend (linear GP) + Fourier seasonality (periodic GP) + noise — same decomposition as a GP with trend + periodic + white noise kernel. Write 2 sentences.

**Q13 — make_features + TimeSeriesSplit**
```python
from sklearn.model_selection import TimeSeriesSplit

def make_features(s):
    f = pd.DataFrame(index=s.index)
    for lag in [1, 2, 3, 6, 12]:
        f[f'lag_{lag}'] = s.shift(lag)
    f['roll_12_mean'] = s.rolling(12).mean()
    f['roll_12_std']  = s.rolling(12).std()
    f['month'] = s.index.month
    f['year']  = s.index.year
    f['trend'] = np.arange(len(s))
    return f.dropna()

X_full = make_features(series)
y_full = series.loc[X_full.index]

assert X_full.shape[1] == 10, f"Expected 10 features, got {X_full.shape[1]}"
print(f"Rows dropped by dropna: {len(series) - len(X_full)}")  # expect ~12

X_train = X_full.loc[:TRAIN_END]
y_train = y_full.loc[:TRAIN_END]
X_test  = X_full.loc[TEST_START:]
y_test  = y_full.loc[TEST_START:]

tscv = TimeSeriesSplit(n_splits=4, test_size=12)  # expanding window
```
- [ ] Confirm 10 features: lag_1/2/3/6/12 (5) + roll_12_mean/std (2) + month/year/trend (3) = 10
- [ ] **AI Prompt 2–3:** Walk-forward CV prompt → verify: k-fold shuffles index (future leaks into training) = economically nonsensical (2020 data predicting 2019); TimeSeriesSplit = expanding window = correct. Log in `misc/ai_prompt_logs.md`.
- [ ] **Discussion Q5 draft:** "Recursive forecasting compounds errors — each predicted value becomes a lag feature input for the next step. On a near-random-walk like S&P 500, compounding makes recursive error diverge noticeably beyond h=6 steps (roughly where autocorrelation is negligible). Direct forecasting trains one model per horizon h, so errors don't compound; however it requires 48 separate models and loses the autocorrelation information that recursive implicitly uses at short horizons (h=1–3)."

---

### Phase 3 — ML + Deep Learning (Q14–Q18)

**Video (~15 min):**
- [ ] Feature Engineering for TS — Kishan Manani (PyData) ★ — can watch at 1.5x during model training

**Q14 — LinearRegression + XGBoost walk-forward CV**
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import xgboost as xgb

lr  = LinearRegression()
xgb_model = xgb.XGBRegressor(n_estimators=200, learning_rate=0.05,
                               max_depth=4, subsample=0.8,
                               random_state=42, verbosity=0)

for model, name in [(lr, 'LinReg'), (xgb_model, 'XGBoost')]:
    fold_rmse = []
    for train_idx, val_idx in tscv.split(X_train):
        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
        model.fit(X_tr, y_tr)
        pred    = model.predict(X_val)
        log_rms = np.sqrt(mean_squared_error(np.log(y_val+1), np.log(pred+1)))
        fold_rmse.append(log_rms)
    print(f"{name} — CV log-RMSE per fold: {[f'{r:.4f}' for r in fold_rmse]}")
```
- [ ] Report per-fold log-RMSE
- [ ] Which fold had highest RMSE? It will likely be 2019 (fold 4) given COVID proximity / late-cycle volatility — note in Reflect

**Q15 — LightGBM recursive multi-step forecast**
```python
import lightgbm as lgb

lgb_model = lgb.LGBMRegressor(n_estimators=200, learning_rate=0.05,
                               num_leaves=31, random_state=42, verbose=-1)
lgb_model.fit(X_train, y_train)

# Recursive loop — history buffer append
history = list(series.values)
lgb_fc  = []

for _ in range(H):
    s_temp = pd.Series(history, index=pd.date_range('1990-01', periods=len(history), freq='MS'))
    feat   = make_features(s_temp).iloc[[-1]]
    pred   = lgb_model.predict(feat)[0]
    lgb_fc.append(pred)
    history.append(pred)           # ← CRITICAL: append, don't re-read training data

lgb_fc = np.array(lgb_fc)
results['LightGBM'] = lgb_fc
```
- [ ] Common mistake: reading lag features from original training data at each step → flat periodic forecast. Must append each prediction to `history` before computing next lag features.
- [ ] Assert `lgb_mase < 1.0` — if fails, check that features are being computed on the growing history buffer, not the original series

**Q16 — LightGBM quantile intervals**
```python
lgb_lo = lgb.LGBMRegressor(objective='quantile', alpha=0.025,
                             n_estimators=200, random_state=42, verbose=-1)
lgb_hi = lgb.LGBMRegressor(objective='quantile', alpha=0.975,
                             n_estimators=200, random_state=42, verbose=-1)
lgb_lo.fit(X_train, y_train)
lgb_hi.fit(X_train, y_train)

# Recursive forecast for both quantile models (same buffer pattern as Q15)
lgb_fc_lo = recursive_forecast(lgb_lo, history_copy, H)  # wrap Q15 pattern into a function
lgb_fc_hi = recursive_forecast(lgb_hi, history_copy, H)

# Empirical coverage
coverage = np.mean((test.values >= lgb_fc_lo) & (test.values <= lgb_fc_hi))
print(f"Empirical 95% coverage: {coverage:.1%}")
```
- [ ] Report empirical coverage — if < 95%, likely causes: (1) COVID structural break (2020 distribution differs from 2010s training) or (2) quantile models trained on training distribution that underestimates tail risk
- [ ] **Discussion Q7 draft:** "74% coverage (instead of 95%) has two possible causes. (1) Miscalibration: the training distribution (1990–2019) underestimates variance, so the 2.5th/97.5th quantile bounds are too narrow relative to the actual test distribution. (2) Distributional shift: COVID-19 changed the data-generating process in 2020 — the training prior is simply wrong for that regime. Diagnose by splitting the test set: check coverage on 2020–2021 vs 2022–2024 separately. If 2020–2021 drives the gap, it's distributional shift; if coverage is uniformly low across all years, it's miscalibration."

**Q17 — MLP**
```python
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

scaler_mlp = StandardScaler()
X_train_sc = scaler_mlp.fit_transform(X_train)  # fit on TRAIN only — never full data
X_test_sc  = scaler_mlp.transform(X_test)

mlp = MLPRegressor(hidden_layer_sizes=(128, 64, 32), max_iter=500,
                   random_state=42, early_stopping=True, validation_fraction=0.1)
mlp.fit(X_train_sc, y_train)

# Recursive forecast — use scaled features from growing buffer
mlp_fc = recursive_forecast_scaled(mlp, scaler_mlp, history_copy, H)
results['MLP'] = mlp_fc
```
- [ ] StandardScaler: fit on X_train only, transform X_test — avoid leakage
- [ ] Reflect: does it beat LinearRegression on MASE? On 360 training months, MLP may marginally improve over LR; expect similar performance.

**Q18 — LSTM**
```python
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

LOOKBACK = 12

scaler_lstm = MinMaxScaler()
log_train_scaled = scaler_lstm.fit_transform(log_train.values.reshape(-1,1))

# Build (samples, LOOKBACK, 1) 3D tensor
X_lstm, y_lstm = [], []
for i in range(LOOKBACK, len(log_train_scaled)):
    X_lstm.append(log_train_scaled[i-LOOKBACK:i, 0])
    y_lstm.append(log_train_scaled[i, 0])
X_lstm = np.array(X_lstm).reshape(-1, LOOKBACK, 1)  # 3D — mandatory
y_lstm = np.array(y_lstm)

model_lstm = Sequential([
    LSTM(64, input_shape=(LOOKBACK, 1)),
    Dense(1)
])
model_lstm.compile(optimizer='adam', loss='mse')
model_lstm.fit(X_lstm, y_lstm, epochs=50, batch_size=16,
               validation_split=0.1, verbose=0)

# Recursive forecast: predict 1 step → append → predict next → inverse_transform at end
window = list(log_train_scaled[-LOOKBACK:, 0])
lstm_fc_scaled = []
for _ in range(H):
    inp = np.array(window[-LOOKBACK:]).reshape(1, LOOKBACK, 1)
    pred = model_lstm.predict(inp, verbose=0)[0,0]
    lstm_fc_scaled.append(pred)
    window.append(pred)

lstm_fc_log = scaler_lstm.inverse_transform(
                  np.array(lstm_fc_scaled).reshape(-1,1)).flatten()
lstm_fc = np.exp(lstm_fc_log)  # back to price space
results['LSTM'] = lstm_fc
```
- [ ] Input shape must be `(samples, LOOKBACK=12, 1)` — 3D tensor
- [ ] MinMaxScaler on log_price: fit on log_train only
- [ ] Recursive loop: append each prediction to window before next step
- [ ] inverse_transform THEN np.exp() — don't reverse the order
- [ ] **AI Prompt 3:** LSTM shape prompt → verify: (samples, LOOKBACK, 1) stated, recursive loop described, inverse_transform at end. Log in `misc/ai_prompt_logs.md`.
- [ ] **Reflect on Q18:** Does LSTM outperform SARIMA with 360 training months? This is open-ended — report your actual MASE comparison. 360 months > typical 96-point airline case, so LSTM has more to learn from. Still, near-random-walk returns mean all models cluster near MASE=1.0. If LSTM MASE < SARIMA MASE, attribute to learned seasonal structure. If not, note that random-walk EMH limits the signal LSTM can extract.

**Transformer note (1–2 sentences in markdown):**
"For larger datasets or multivariate settings, Temporal Fusion Transformer (TFT via `pytorch-forecasting`) and N-BEATS / PatchTST (via `darts`) have shown strong performance on financial time series. These are not implemented here due to training infrastructure constraints, but represent the state-of-the-art direction for production-grade financial forecasting."

**Day 2 end check:**
- [ ] Q11–Q18 all complete
- [ ] `results` dict has: Naive, SeasonalNaive, HoltWinters, SARIMA, Prophet, LightGBM, MLP, LSTM
- [ ] Prophet CV table printed, coverage rate logged, LSTM MASE vs SARIMA MASE noted
- [ ] AI prompts 2, 2–3, 3 logged in `misc/ai_prompt_logs.md`

---

## Day 3 (Sun Jun 29) — Phase 4 (Parts 6–7, Q19–Q23) + Final Pass

**Budget: ~5–6 hrs | Goal: evaluation table, ensemble, DM test, memo, commit**

**Video (~12 min):**
- [ ] MASE vs RMSE — ritvikmath (~12 min) ★ — watch before Q19

### Phase 4 — Evaluation, Error Analysis, Business Output (Q19–Q23)

**Q19 — Full 7-metric comparison table**
```python
def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred)**2))

def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def smape(y_true, y_pred):
    return np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100

def wmae(y_true, y_pred):
    w = y_true / y_true.sum()
    return np.sum(w * np.abs(y_true - y_pred))

def wmape(y_true, y_pred):
    # Σ(|e/y| × y) / Σ(y) × 100 — NOT sMAPE
    return np.sum(np.abs(y_true - y_pred)) / np.sum(np.abs(y_true)) * 100

def mase_fn(y_true, y_pred, y_train, m=12):
    naive_err = np.mean(np.abs(np.diff(y_train, n=m)))
    return np.mean(np.abs(y_true - y_pred)) / naive_err

test_arr = test.values
train_arr = train.values

rows = []
for model_name, fc in results.items():
    fc = np.array(fc)[:H]
    rows.append({
        'Model': model_name,
        'MAE':   mae(test_arr, fc),
        'RMSE':  rmse(test_arr, fc),
        'MAPE':  mape(test_arr, fc),
        'sMAPE': smape(test_arr, fc),
        'WMAE':  wmae(test_arr, fc),
        'WMAPE': wmape(test_arr, fc),
        'MASE':  mase_fn(test_arr, fc, train_arr),
    })

metrics_df = pd.DataFrame(rows).sort_values('MASE').reset_index(drop=True)
print(metrics_df.to_string(index=False))
```
- [ ] All 7 metrics for ALL models — no black-box metric library; implement each function explicitly as above
- [ ] Sort by MASE — MASE < 1.0 = beats naive random walk
- [ ] **AI Prompt 4:** WMAPE vs MAPE prompt → verify: WMAPE formula = Σ(|e/y|×y)/Σ(y)×100 = Σ|e|/Σ|y|×100; does NOT conflate with sMAPE; explains that higher index levels receive proportionally more weight. Log in `misc/ai_prompt_logs.md`.
- [ ] Note in Reflect: which model ranks differently on WMAPE vs MAPE? (Models that forecast poorly during high-index periods, e.g. 2022–2024 highs, will be penalized more on WMAPE)

**Q20 — Error by calendar month**
```python
err_by_month = pd.DataFrame({
    'month':  pd.DatetimeIndex(test.index).month,
    'error':  test.values - results['SARIMA']  # or your best model
}).groupby('month')['error'].mean()

err_by_month.plot(kind='bar')
plt.title('Mean Forecast Error by Calendar Month')
plt.savefig('plots/error_by_month.png', dpi=150, bbox_inches='tight')
```
- [ ] Compute for your best model by MASE
- [ ] Which month shows highest negative bias? (March likely, due to COVID 2020 crash)
- [ ] Does March 2020 distort the monthly aggregates? Yes — note that 60-month test set only has 1 March 2020, so that one observation heavily influences the March aggregate. Mention in Reflect.

**Q21 — Error by horizon h=1..H**
```python
# Compare two best models by MASE
best_models = metrics_df['Model'].iloc[:2].tolist()

plt.figure(figsize=(12,5))
for m_name in best_models:
    fc = np.array(results[m_name])[:H]
    horizon_mae = [mae(test.values[:h], fc[:h]) for h in range(1, H+1)]
    plt.plot(range(1, H+1), horizon_mae, label=m_name)
plt.xlabel('Forecast Horizon (months)')
plt.ylabel('MAE')
plt.legend()
plt.title('Accuracy by Forecast Horizon')
plt.savefig('plots/error_by_horizon.png', dpi=150, bbox_inches='tight')
```
- [ ] At which horizon does accuracy collapse? Expect divergence beyond h=6–12 for most models; SARIMA may degrade faster than LightGBM at long horizons
- [ ] **Discussion Q5 refinement:** tie this to actual h-collapse observation

**Q22 — Ensemble + Diebold-Mariano + pickle verify**
```python
# Simple ensemble: average of top 4 models by MASE
top4 = metrics_df['Model'].iloc[:4].tolist()
ensemble_fc = np.mean([np.array(results[m])[:H] for m in top4], axis=0)
results['Ensemble'] = ensemble_fc

# Check pairwise residual correlation — ensemble benefit ∝ de-correlation
residuals = {m: test.values - np.array(results[m])[:H] for m in top4}
corr_df = pd.DataFrame(residuals).corr()
print("Pairwise residual correlations:\n", corr_df)  # lower = more benefit from ensemble

# Diebold-Mariano test: best single vs ensemble
from scipy import stats

best_single = metrics_df['Model'].iloc[0]
e1 = (test.values - np.array(results[best_single])[:H])**2
e2 = (test.values - ensemble_fc)**2
dm_diff = e1 - e2
dm_stat, dm_p = stats.ttest_1samp(dm_diff, 0)
print(f"Diebold-Mariano: stat={dm_stat:.3f}, p={dm_p:.4f}")
print("Conclusion:", "Ensemble significantly better (p<0.05)" if dm_p < 0.05 else
      f"No significant difference (p={dm_p:.3f}) — improvement not statistically robust")

# Pickle verify
with open('sp500_sarima_v1.pkl', 'rb') as f:
    sarima_loaded = pickle.load(f)
fc_check = sarima_loaded.get_forecast(12)
assert fc_check is not None
print("pkl reload + 12-step forecast: OK")
```
- [ ] Report DM p-value AND explicit conclusion about statistical significance given the COVID test period
- [ ] Note: even 60 test months with high serial autocorrelation → effective sample size much smaller → DM will often be non-significant. This is the expected outcome — the CIO needs this framed correctly.
- [ ] Hierarchical TS note (3 sentences in markdown): "Hierarchical forecasting addresses portfolios of related series. Bottom-Up aggregates stock-level forecasts to the index level — preserves stock accuracy but aggregation can compound errors. Top-Down disaggregates the index forecast to individual stocks — better index-level accuracy but weak at the stock level. MinT (Optimal Reconciliation) finds the coherent forecasts closest to the base forecasts in the mean-squared sense, outperforming both on average."

**Q23 — Investment Recommendation Memo (200 words)**

Write the memo AFTER completing Q22 so you have real numbers to cite. Template:

> **TO:** Chief Investment Officer
> **FROM:** [Name], Quantitative Analyst
> **RE:** S&P 500 12-Month Forecasting Model Recommendation
>
> **Question 1: Does any model beat the random-walk baseline with statistical significance?**
> [Cite best MASE here, e.g. "Our best model (LightGBM) achieved MASE=0.88, marginally outperforming the naïve benchmark."] However, the Diebold-Mariano test returns p=[value], indicating this improvement is [not statistically significant / statistically significant at the 5% level] once autocorrelation-corrected inference is applied. The COVID-19 structural break in March 2020 (−34% realized vs +[X]% forecast) demonstrates that tail risk from regime changes cannot be captured by any historical-data model. Per the Efficient Market Hypothesis, near-white-noise log-returns mean MASE ≈ 1.0 is the expected outcome, not a failure.
>
> **Question 2: Which model to deploy?**
> We recommend [SARIMA / LightGBM based on your results] for production monthly equity allocation. Key selection criteria beyond MASE: (1) **Regulatory explainability** — SARIMA coefficients and confidence intervals are directly interpretable for regulator-facing model documentation; (2) **Refit latency** — SARIMA refits on new monthly data in seconds; (3) **Structural break robustness** — the model's confidence intervals explicitly flag uncertainty rather than projecting false precision. Any production deployment must include a COVID-2020 caveat: the 12-month forecast should be used for scenario framing and risk bounds, not as a directional point prediction.

- [ ] Replace all brackets with actual numbers from Q22 output
- [ ] Word count: 180–220 words (Project Guide says ≤200 words; ±10% is acceptable if all required elements are present)

---

## Discussion Questions — Full Draft (all 8)

Complete these as you go; compile into `misc/discussion_answers.md` by end of Day 3.

| Q | Draft anchor |
|---|---|
| Q1 | Random walk + MASE≈1.0 + value of uncertainty bands — drafted Day 1 Q5 |
| Q2 | COVID break = not a model failure; quant analyst communicates via scenario bands + tail risk disclosure — write after Q10 |
| Q3 | Ljung-Box lag 12 failure → increase Q; drafted Day 1 Q9 |
| Q4 | MASE gap doesn't count without DM p<0.05; investment risk of acting on non-significant gap — write after Q22 |
| Q5 | Recursive vs direct horizon degradation — drafted Day 2 Q13 |
| Q6 | Bottom-Up vs Top-Down vs MinT — write after Q22 hierarchical note |
| Q7 | 74% coverage: miscalibration vs distributional shift — drafted Day 2 Q16 |
| Q8 | 3 non-accuracy criteria for MASE-tied models: explainability, refit latency, structural break robustness — write after Q23 |

**Discussion Q2 draft:** "A SARIMA model trained on 1990–2019 data will extrapolate the long-run upward trend — predicting positive returns in 2020. The March 2020 −34% observation is not a model failure; it is a tail event outside the training distribution by definition. A quant analyst should communicate to the investment committee using scenario ranges and conditional forecasts ('if no regime change, the model projects X; however, macro tail risks are not quantifiable within this framework') and should always provide the model's uncertainty intervals rather than point forecasts."

**Discussion Q4 draft:** "A MASE gap of 0.87 vs 0.91 does not 'count' without statistical significance. With DM p=0.18, we cannot reject the null of equal predictive accuracy — the observed gap is consistent with random chance given the small effective sample size (60 months with high serial autocorrelation). The investment risk of acting on this gap: if the performance difference disappears on the next 60-month window (2025–2029), we have committed capital allocation to a model chosen by noise."

**Discussion Q6 draft:** "Bottom-Up: forecast each of the 50 stocks, then sum → better stock-level accuracy, but aggregation compounds errors at the portfolio level. Top-Down: forecast the S&P 500 index, then disaggregate by market cap weights → better portfolio-level accuracy, but weak at individual stock level. MinT (Minimum Trace) reconciliation projects all base forecasts onto the coherent subspace using a GLS estimator that minimizes total forecast variance — producing forecasts that are both internally consistent and closer to optimal at every level of the hierarchy."

**Discussion Q8 draft:** "For near-identical MASE (0.88/0.89/0.90) in a monthly equity allocation context with regulatory reporting requirements: (1) Regulatory explainability — highest priority; SARIMA produces interpretable coefficients and formal confidence intervals that satisfy regulator model documentation standards (MIFID II, FRTB); (2) Refit latency — monthly data means the model must refit on a 24-hour cycle; SARIMA refits in seconds vs XGBoost's minutes on 360+ rows; (3) Structural break robustness — model should flag when the COVID regime is recognized as out-of-distribution rather than extrapolating silently. LightGBM fails criterion (1) without additional explainability tooling (e.g. SHAP)."

---

## AI Prompt Critique Log Template

Create `misc/ai_prompt_logs.md` and add one entry per prompt:

```markdown
## Phase 0 — Stationarity (Jun 27)
**What it got right:** Ran ADF + KPSS on both series; correctly explained stochastic trend for prices and near-stationarity for returns.
**What it got wrong / needed push-back:** [e.g. "Initially only ran ADF — had to ask why KPSS was missing. After push-back, correctly added KPSS and explained conflicting-result interpretation."]
**Verdict:** [Useful / Partially useful / Misleading]

## Phase 1 — SARIMA diagnostics (Jun 27)
...
## Phase 2 — Changepoints (Jun 28)
...
## Phase 2–3 — Walk-forward CV (Jun 28)
...
## Phase 3 — LSTM shape (Jun 28)
...
## Phase 4 — WMAPE vs MAPE (Jun 29)
...
```

---

## Final Deliverable Checklist (before sync)

### Notebook quality
- [ ] Restart & Run All — zero errors, zero NameError, zero None remaining
- [ ] All 23 questions answered (Q1–Q23)
- [ ] All SELF-CHECK assert cells pass
- [ ] Q4 stationarity table: ADF + KPSS for both raw prices AND log-returns, with EMH conclusion
- [ ] Q9 Ljung-Box: p-values at lags 6, 12, 24 printed; order adjustment documented if any failed
- [ ] Q19 metrics table: all 7 metrics, all models, sorted by MASE
- [ ] Q22 DM test: p-value + explicit statistical significance conclusion in COVID context
- [ ] Q23 memo: no [brackets]; actual MASE + DM p-value cited
- [ ] All ✍ Reflect cells contain specific numbers — no generic answers

### Files
- [ ] `sp500_sarima_v1.pkl` — exists, reloads, produces 12-step forecast
- [ ] `plots/` — at least 8 saved figures: ACF/PACF, STL, SARIMA diagnostics, SARIMA forecast, Prophet components, error by month, error by horizon, one model comparison figure
- [ ] `wk8_forecasting.pdf` — PDF export of fully executed notebook (File → Download As → PDF, or `jupyter nbconvert`)
- [ ] `requirements.txt` — pinned (`pip freeze > requirements.txt`)
- [ ] `README.md` — update with repo name, dataset, week, submission date, key results (best MASE, DM p-value)
- [ ] `misc/ai_prompt_logs.md` — 5 entries, one per AI prompt
- [ ] `misc/discussion_answers.md` — all 8 discussion answers compiled
- [ ] `.gitignore` — includes: `__pycache__/`, `.ipynb_checkpoints/`, `*.pyc`, `.env`

### 12-Factor pre-commit checklist (§16)
- [ ] No hardcoded paths or secrets in committed code
- [ ] No `print()` debug left — only `print()` calls that are pedagogically intentional in the notebook
- [ ] `requirements.txt` pinned and current
- [ ] `sp500_sarima_v1.pkl` NOT gitignored (it's a required submission artifact)

### Commit sequence
```bash
git add wk8_forecasting.ipynb wk8_forecasting.pdf sp500_sarima_v1.pkl requirements.txt README.md plots/ misc/
git status  # verify no .env staged
git commit -m "feat: W8 forecasting — S0-S4 complete, all 23 Qs answered, 8 models, MASE table, DM test, investment memo"
git push origin main
```

---

## Fallback Priority (if 3-day budget breaks)

**Must have (do not cut):**
- S0: ADF + KPSS + ACF/PACF + STL
- S1: SARIMA + Ljung-Box + QQ-plot + `sp500_sarima_v1.pkl`
- S4: all 7 metrics + MASE comparison table
- Q1, Q3, Q4, Q8 discussion answers
- Investment memo (Q23)

**Cut first:**
- Prophet cross-validation depth (Q12 — fit Prophet, skip full CV comparison between 0.05/0.5)
- MLP (Q17) — mention it, implement minimally, note MASE
- Hierarchical extension note (Q22 — keep to 2 sentences)
- Ensemble de-correlation analysis (pairwise residual correlation)
- Error by horizon plot (Q21 — report number, skip plot)

---

## Master Profile Update Trigger (post-completion)

When notebook is committed:
1. Log W8 as **Complete** in Fellowship progress table (mirrors Wk7 v93 pattern)
2. New skills to add to §Skills & Stack:
   - Time Series: SARIMA (Box-Jenkins), Holt-Winters Triple ES, Prophet (Fourier seasonality, changepoints), ADF + KPSS stationarity tests, STL decomposition
   - Advanced ML: LightGBM quantile regression (prediction intervals), walk-forward CV (TimeSeriesSplit), recursive multi-step forecasting
   - Deep Learning: Keras LSTM (3D input, MinMaxScaler, recursive forecast)
   - Evaluation: MASE, WMAPE, Diebold-Mariano test, Hierarchical TS (Bottom-Up/Top-Down/MinT overview)
3. Add W8 project entry to `projects.html` (matches Wk7 entry style)
4. Bump MASTER version
