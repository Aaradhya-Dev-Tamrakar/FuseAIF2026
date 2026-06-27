# W6 — Probabilistic Models & Bayesian Inference
## Master Task Plan · Fusemachines AI Fellowship
> Continuity file for VS Code + Antigravity Agents · Last Updated: 2026-06-04

---

## QUICK REFERENCE

| Part | Topic | Qs | Self-Checks | Datasets |
|------|-------|-----|-------------|----------|
| 1 | MLE · MAP · Full Bayes | Q1–Q3 + Reflect 1 | Q1, Q3 | Telco |
| 2 | Sequential Updating · Dirichlet-Multinomial | Q4–Q7 + Reflect 2 | Q4, Q7 | Telco |
| 3 | Multivariate Gaussians | Q8–Q10 + Reflect 3 | Q8, Q9, Q10 | Telco |
| 4 | Probabilistic Graphical Models | Q11–Q13 + Reflect 4 | Q11 (partial) | Telco |
| 5 | Gaussian Process Regression | Q14–Q17 + Reflect 5 | Q14, Q15 RMSE | Mauna Loa CO₂ |
| 6 | MCMC · Bayesian Logistic Regression | Q18–Q22 + Reflect 6 | implicit | Telco |

**Submission artefacts:** executed `.ipynb` · `telco_bayes_lr_v1.pkl` · one-page reflection (PDF/MD)

---

## ENVIRONMENT SETUP

```bash
pip install pymc arviz pgmpy scikit-learn scipy statsmodels pandas numpy matplotlib seaborn
```

**Data loading (already in notebook — run this cell first):**
```python
url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
df_raw = pd.read_csv(url)
df = df_raw.copy()
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].str.strip(), errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())
df = df.drop(columns=['customerID'])
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# Mauna Loa (Part 5 only — no CSV needed)
from statsmodels.datasets import co2
df_co2 = co2.load_pandas().data.resample('ME').mean().dropna()
t = (df_co2.index - df_co2.index[0]).days.values.reshape(-1, 1) / 365.25
y = df_co2['co2'].values
```

---

## PART 1 · THE ESTIMATION TRINITY — MLE, MAP, FULL BAYES

**Business context:** Are Month-to-month customers more likely to churn than Two-year customers, and how certain are you?

---

### Q1 · Extract experimental groups `[ ]`
**Self-check:** `n_As == 40`, `n_A > 3000`, `n_B > 1000`

```python
group_A       = df[df['Contract'] == 'Month-to-month']
group_B       = df[df['Contract'] == 'Two year']
group_A_small = group_A.sample(n=40, random_state=42)
```

---

### Q2a · Compute MLE, MAP, pull table `[ ]`
**Prior:** Beta(2, 8) — encodes belief that most segments churn < 30%

```python
alpha_prior, beta_prior = 2, 8
# For each (k, n):
mle     = k / n
map_est = (alpha_prior + k - 1) / (alpha_prior + beta_prior + n - 2)
pull    = abs(map_est - mle)
```

**Expected pattern:** pull is large for Group A_small (n=40), tiny for large groups — prior dominates when data is scarce.

---

### Q2b · Plot 3 posterior PDFs `[ ]`
For each group:
- Prior PDF: `beta_dist.pdf(theta_range, alpha_prior, beta_prior)`
- Posterior parameters: `alpha_post = alpha_prior + k`, `beta_post = beta_prior + (n - k)`
- Posterior PDF: `beta_dist.pdf(theta_range, alpha_post, beta_post)`
- Vertical lines for MLE and MAP
- Shade 94% HDI using `beta_dist.ppf([0.03, 0.97], alpha_post, beta_post)` → `fill_between`

---

### Q3 · Monte Carlo P(θ_A > θ_B) `[ ]`
**Self-check:** result must be > 0.90

```python
MC_SAMPLES = 10_000
np.random.seed(42)
post_A_samples = np.random.beta(alpha_prior + k_A,  beta_prior + n_A  - k_A,  MC_SAMPLES)
post_B_samples = np.random.beta(alpha_prior + k_B,  beta_prior + n_B  - k_B,  MC_SAMPLES)
p_A_greater    = np.mean(post_A_samples > post_B_samples)
```

---

### ✍️ Reflect 1 `[ ]`
1. Prior pull for A_small >> pull for large groups because small n means data provides little information to overwhelm the prior. The formula `|MAP − MLE| = |prior_contribution / (n + prior_weight)|` shrinks as n grows.
2. For A_small: present Full Bayes posterior (HDI). MLE ignores prior; MAP gives point estimate only; Full Bayes gives the entire posterior and an honest uncertainty interval.
3. Prior becomes irrelevant when posterior mean is within 1% of MLE: solve `(α₀ + k)/(α₀ + β₀ + n) ≈ k/n` → roughly `n >> α₀ + β₀ = 10`, so ~n > 200–500 in practice.

---

## PART 2 · SEQUENTIAL BAYESIAN UPDATING & DIRICHLET-MULTINOMIAL

---

### Q4 · Implement `update_posterior()` `[ ]`
**Self-check:** alpha increments on churn, beta on no-churn

```python
def update_posterior(alpha, beta, churn_label):
    if churn_label == 1:
        return alpha + 1, beta
    else:
        return alpha, beta + 1
```

---

### Q5 · Sequential update — posterior evolution plot `[ ]`
```python
alpha_init, beta_init = 2.0, 8.0
snapshots = [1, 5, 20, 80, 200, 500]
history = {}
a, b = alpha_init, beta_init
for i, row in df_shuffled.iloc[:500].iterrows():
    n = df_shuffled.index.get_loc(i) + 1
    a, b = update_posterior(a, b, row['Churn'])
    if n in snapshots:
        history[n] = (a, b)
```
Plot: 2×3 subplots, one per snapshot. Show posterior PDF, true rate (red dashed), posterior mode (orange dash-dot).

---

### Q6 · Decision boundary P(θ > 0.25) vs n `[ ]`
```python
threshold = 0.25
MC_SAMPLES = 10_000
p_exceed = []
a, b = 2.0, 8.0
for _, row in df_shuffled.iloc[:500].iterrows():
    a, b = update_posterior(a, b, row['Churn'])
    samples = np.random.beta(a, b, MC_SAMPLES)
    p_exceed.append(np.mean(samples > threshold))
```
Compare Bayesian threshold crossing (p > 0.90) vs frequentist n from one-proportion z-test.

---

### Q7 · Dirichlet-Multinomial `[ ]`
**Self-check:** `len(posterior_alpha) == 3`, sum check passes

```python
categories  = ['Month-to-month', 'One year', 'Two year']
prior_alpha = np.array([1.0, 1.0, 1.0])
counts      = np.array([df[df['Contract']==c].shape[0] for c in categories])
posterior_alpha = prior_alpha + counts
```

**Unseen category (Biannual):** append pseudocount=1 → `posterior_alpha_4 = np.append(posterior_alpha, 1)`. Posterior mean = 1 / (posterior_alpha.sum() + 1). This shows Dirichlet assigns non-zero probability to unseen categories.

---

### ✍️ Reflect 2 `[ ]`
1. One year has fewer observations → higher variance in marginal Beta → wider credible intervals.
2. Biannual posterior = Beta(1, sum_of_others) — the prior pseudocount alone. Reveals Dirichlet treats the prior as "virtual observations."
3. Dirichlet equivalent of Beta(2,8) prior mean: encode domain knowledge as concentration parameters `α_j` such that `α_j / sum(α) = prior mean per category`. For 3 categories summing to the same total pseudo-count as Beta(2,8), use `[2, 4, 4]` (if prior belief is ~20% M2M, ~40% 1yr, ~40% 2yr).

---

## PART 3 · MULTIVARIATE GAUSSIANS

---

### Q8a · Fit 2D Gaussian `[ ]`
**Self-check:** `mu_2d.shape == (2,)`, `Sigma_2d.shape == (2,2)`, `-1 < rho < 1`

```python
X_2d     = df[['tenure', 'MonthlyCharges']].values.astype(float)
mu_2d    = np.mean(X_2d, axis=0)
Sigma_2d = np.cov(X_2d.T)
rho      = Sigma_2d[0,1] / np.sqrt(Sigma_2d[0,0] * Sigma_2d[1,1])
```

---

### Q8b · Scatter + 1σ/2σ/3σ confidence ellipses `[ ]`
Use the provided `confidence_ellipse()` function. Call with `n_std=1, 2, 3` using different colors/alphas. Add `ax.plot(*mu_2d, 'r+', ms=15)` for the mean marker.

---

### Q9 · Conditional Gaussian P(MonthlyCharges | tenure=24) `[ ]`
**Self-check:** conditional mean within $5 of empirical mean for tenure 22–26

```python
tenure_query = 24
cond_mean = mu_2d[1] + Sigma_2d[1,0] / Sigma_2d[0,0] * (tenure_query - mu_2d[0])
cond_var  = Sigma_2d[1,1] - Sigma_2d[1,0]**2 / Sigma_2d[0,0]
cond_std  = np.sqrt(cond_var)
```

---

### Q10 · 3D Covariance + Condition Number + Marginalisation `[ ]`
**Self-check:** `kappa > 100`, `max_diff < 1e-6`

```python
X_3d           = df[['tenure','MonthlyCharges','TotalCharges']].values.astype(float)
Sigma_3d       = np.cov(X_3d.T)
kappa          = np.linalg.cond(Sigma_3d)
Sigma_marginal = Sigma_3d[:2, :2]
max_diff       = np.abs(Sigma_2d - Sigma_marginal).max()
```

---

### ✍️ Reflect 3 `[ ]`
1. High κ means TotalCharges ≈ tenure × MonthlyCharges — near-linear dependence; the matrix is nearly singular.
2. General rule: marginalise a Gaussian by simply extracting the submatrix of Σ and subvector of μ corresponding to the variables you want to keep.
3. Near-collinearity inflates coefficient variance and makes estimates unstable. Frequentist equivalent: Variance Inflation Factor (VIF).

---

## PART 4 · PROBABILISTIC GRAPHICAL MODELS

---

### Q11 · Build and fit Bayesian Network `[ ]`

```python
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.parameter_estimator import DiscreteMLE
from pgmpy.inference import VariableElimination

edges = [
    ('SeniorCitizen', 'Churn'),
    ('Contract', 'Churn'),
    ('tenure_disc', 'Churn'),
    ('InternetService', 'mc_disc'),
    ('mc_disc', 'Churn'),
]
dag = DiscreteBayesianNetwork(edges)
estimator = DiscreteMLE(model=dag, data=df_pgm[['SeniorCitizen','Contract',
    'tenure_disc','InternetService','mc_disc','Churn']].astype(str))
dag.fit(df_pgm[['SeniorCitizen','Contract','tenure_disc',
                'InternetService','mc_disc','Churn']].astype(str),
        estimator=DiscreteMLE)
```

**Forward inference:**
```python
infer = VariableElimination(dag)
result_fwd = infer.query(['Churn'], evidence={'Contract': 'Month-to-month'})
p_churn_m2m_bn = result_fwd.values[1]   # index for Churn='1'
```

**Backward inference:**
```python
result_bwd = infer.query(['Contract'], evidence={'Churn': '1'})
```

> ⚠️ `pgmpy` requires all columns as strings for DiscreteMLE. Cast with `.astype(str)`.

---

### Q12 · Structure sensitivity: two competing DAGs `[ ]`

**DAG 1 (original):** `tenure_disc → Churn` direct

```
SeniorCitizen ──────────────────────────────► Churn
Contract ───────────────────────────────────► Churn
tenure_disc ────────────────────────────────► Churn
InternetService ──► mc_disc ────────────────► Churn
```

**DAG 2 (colleague's):** `Contract → tenure_disc → Churn` (mediated)

```
SeniorCitizen ──────────────────────────────► Churn
Contract ──────────────────────────────────► tenure_disc ──► Churn
InternetService ──► mc_disc ────────────────► Churn
```

**E where models agree:** observing `tenure_disc` directly (d-separates Contract's indirect path in DAG 2 when tenure is known).

**E where models disagree:** observing `Contract` only (without tenure) — DAG 1 and DAG 2 give different posterior P(Churn) because DAG 2 routes the effect through tenure.

**Causal story:** W5 SHAP showed tenure and contract are both high-importance features with partially overlapping effects → DAG 1 is likely more consistent since SHAP treats them as independent contributors.

---

### Q13 · Markov Random Field `[ ]`

```python
from pgmpy.models import DiscreteMarkovNetwork
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference import BeliefPropagation

mrf_edges = [('Contract','Churn'), ('tenure_disc','Churn'),
             ('mc_disc','Churn'), ('SeniorCitizen','Churn')]
mrf = DiscreteMarkovNetwork(mrf_edges)

# Build pairwise factors from empirical joint frequencies
# For each edge (A,B): factor values = empirical joint counts / total
# Add with mrf.add_factors(factor_AB, ...)
# mrf.check_model()

bp = BeliefPropagation(mrf)
marg_churn = bp.query(variables=['Churn'], show_progress=False)
```

> ⚠️ MRF factors must cover all variables. If `check_model()` raises, verify every variable appears in at least one factor.

---

### ✍️ Reflect 4 `[ ]`
1. Two reasons for BN vs empirical discrepancy: (a) continuous variables discretised → information loss; (b) DAG encodes an indirect path via `mc_disc` that mediates some of the Contract effect instead of routing it directly.
2. Explaining away: knowing a customer churned makes month-to-month contracts more probable — the backward inference "explains" the churn observation by attributing it to contract type.
3. BN supports causal queries (interventional: "what if we force Contract = Two year?") via do-calculus; MRF cannot. Choose MRF when you care only about correlation/density estimation and have no causal assumptions to encode, or when the variable relationships are genuinely symmetric.

---

## PART 5 · GAUSSIAN PROCESS REGRESSION — MAUNA LOA CO₂

---

### Q14 · Load Mauna Loa `[ ]`
**Self-check:** ~521 observations, CO₂ range ~313–369 ppm

```python
from statsmodels.datasets import co2
df_co2 = co2.load_pandas().data.resample('ME').mean().dropna()
t      = (df_co2.index - df_co2.index[0]).days.values.reshape(-1, 1) / 365.25
y      = df_co2['co2'].values
```

---

### Q15 · Kernel design rationale (fill table BEFORE coding) `[ ]`

| Signal | Description | Kernel | Justification |
|--------|-------------|--------|---------------|
| Trend | Slow linear rise ~1.5 ppm/yr | `DotProduct(sigma_0=0.0, sigma_0_bounds='fixed')` | Linear growth by construction; avoids mean-reversion that RBF trend causes during extrapolation |
| Seasonal | Sharp annual cycle | `RBF(...) * ExpSineSquared(..., periodicity=1.0, periodicity_bounds='fixed')` | RBF modulates amplitude; ExpSineSquared enforces 1-year period |
| Noise | Measurement + short-term variability | `WhiteKernel(...)` | IID noise diagonal |

```python
from sklearn.gaussian_process.kernels import RBF, ExpSineSquared, WhiteKernel, DotProduct

k_trend    = DotProduct(sigma_0=0.0, sigma_0_bounds='fixed')
k_seasonal = RBF(length_scale=1.0) * ExpSineSquared(length_scale=1.0,
                                                      periodicity=1.0,
                                                      periodicity_bounds='fixed')
k_noise    = WhiteKernel(noise_level=0.1)
kernel     = k_trend + k_seasonal + k_noise

gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10,
                               normalize_y=True, random_state=42)
gp.fit(t_train, y_train)
```

**Self-check:** RMSE < 4.5 ppm on test set (1994–2001).

---

### Q16 · Gap experiment `[ ]`

```python
gap_lo, gap_hi = 15.0, 17.0
mask     = ~((t_train.flatten() >= gap_lo) & (t_train.flatten() <= gap_hi))
t_gap_tr = t_train[mask]
y_gap_tr = y_train[mask]

gp_gap = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=3,
                                   normalize_y=True, random_state=42)
gp_gap.fit(t_gap_tr, y_gap_tr)
```

**Expected result:** band width inside gap >> outside gap (typically 5–15× inflation). GP uncertainty grows when interpolating over a data void.

---

### Q17 · Extrapolation and confidence boundary `[ ]`

```python
t_last   = float(t_train.max())
t_extrap = np.linspace(t_last, t_last + 15, 500).reshape(-1, 1)
y_ex, y_ex_std = gp.predict(t_extrap, return_std=True)

for years in [5, 10, 15]:
    idx = np.argmin(np.abs(t_extrap.flatten() - (t_last + years)))
    bw  = 4 * y_ex_std[idx]
    print(f"+{years}yr: 95% band = ±{bw/2:.2f} ppm  (width = {bw:.2f} ppm)")

band_widths = 4 * y_ex_std
exceed_idx  = np.where(band_widths > 5.0)[0]
if len(exceed_idx):
    t_boundary = t_extrap.flatten()[exceed_idx[0]] - t_last
    print(f"Confidence boundary: +{t_boundary:.1f} years")
```

---

### ✍️ Reflect 5 `[ ]` (exactly two sentences)
A GP's extrapolation uncertainty grows continuously beyond the training window because the posterior variance reverts to the prior when no data constrains it, producing credible bands that widen with distance from observed data. A `DecisionTreeRegressor(max_depth=None)` is fundamentally different: it can only predict values within `[min(y_train), max(y_train)]` — it flat-lines at the last leaf's mean, which was confirmed in the W5 assignment where tree models failed to extrapolate rising CO₂ trends and plateaued at the training ceiling.

---

## PART 6 · MCMC — BAYESIAN LOGISTIC REGRESSION

---

### Q18 · Feature scaling rationale + model spec `[ ]`

**Pre-run answer (fill in notebook):** NUTS uses gradient information to propose moves. If `tenure` (0–72) and `MonthlyCharges` ($18–$118) have very different scales, their corresponding coefficients live in a posterior geometry with very different curvatures. NUTS's single step-size can't simultaneously be optimal for a flat dimension and a narrow one → either divergences in one direction or tiny steps everywhere → very low ESS. Scaling makes the posterior geometry isotropic.

```python
with pm.Model() as bayes_lr:
    intercept = pm.Normal('intercept', mu=0, sigma=5)
    beta      = pm.Normal('beta', mu=0, sigma=2, shape=n_features)
    mu        = pm.Deterministic('mu', pm.math.sigmoid(
                    intercept + pm.math.dot(X_tr_scaled, beta)))
    y_obs     = pm.Bernoulli('y_obs', p=mu, observed=y_tr_mc)

    idata = pm.sample(draws=2000, tune=1000, chains=4,
                      target_accept=0.90, random_seed=42,
                      return_inferencedata=True)
```

> ⚠️ PyMC v5 syntax: `return_inferencedata=True` is default. If you get a deprecation warning, drop that argument.

---

### Q19 · Convergence diagnostics `[ ]`

```python
az.plot_trace(idata, var_names=['intercept', 'beta'])
plt.tight_layout(); plt.show()

summary = az.summary(idata, var_names=['intercept','beta'], round_to=3)
print(summary)

# Flag bad parameters
flagged = summary[(summary['r_hat'] > 1.01) | (summary['ess_bulk'] < 400)]
print("Flagged:\n", flagged)
```

**Good trace:** "fuzzy caterpillar" — chains mix, no drift, uniform density.
**Bad signs:** R̂ > 1.01 (chains not mixing), ESS < 400 (high autocorrelation).

---

### Q20 · Prior sensitivity check `[ ]`

```python
contract_idx = next((i for i,c in enumerate(feature_cols) if 'Month-to-month' in c), 0)

# (tight prior model already in notebook — run as-is)
samples_orig  = idata.posterior['beta'].values[:,:,contract_idx].flatten()
samples_tight = idata_tight.posterior['beta'].values[:,:,contract_idx].flatten()

fig, ax = plt.subplots(figsize=(10,4))
ax.hist(samples_orig,  bins=60, alpha=0.6, density=True, label='β ~ N(0,2)')
ax.hist(samples_tight, bins=60, alpha=0.6, density=True, label='β ~ N(0,0.5)')
ax.set_xlabel('β_Contract_Month-to-month'); ax.legend()
plt.tight_layout(); plt.show()
```

**Interpretation:** If posteriors nearly overlap → data dominates, model is prior-robust. If tight prior pulls mean toward 0 significantly → n too small to overwhelm prior.

---

### Q21 · Posterior analysis + frequentist comparison `[ ]`

```python
beta_post = idata.posterior['beta'].values[:,:,contract_idx].flatten()
hdi_94    = az.hdi(beta_post, hdi_prob=0.94)
post_mean = beta_post.mean()
post_std  = beta_post.std()

lr_freq  = LogisticRegression(C=1e6, max_iter=1000)
lr_freq.fit(X_tr_scaled, y_tr_mc)
coef_freq = lr_freq.coef_[0][contract_idx]
```

**Key philosophical difference:**
- Bayesian 94% HDI: P(β ∈ [lo, hi] | data) = 0.94 — a direct probability statement about the parameter.
- Frequentist 94% CI: if we repeated this experiment many times, 94% of such intervals would contain the true β — a statement about the procedure, not about this specific interval.

---

### Q22 · Save MCMC trace `[ ]`

```python
import pickle
save_path = 'telco_bayes_lr_v1.pkl'
pickle.dump(idata, open(save_path, 'wb'))
print(f"✅ MCMC trace saved to '{save_path}'")
```

---

### ✍️ Reflect 6 `[ ]`
1. **R̂** measures between-chain vs within-chain variance; R̂ ≈ 1.0 means chains converged to the same distribution. **ESS** measures how many independent samples the correlated chain is worth. R̂ = 1.38 with ESS = 55 means: chains haven't mixed (some got stuck in a different region) and you effectively have only 55 independent draws — posterior estimates are unreliable and HDIs are too narrow.
2. If posteriors from N(0,2) and N(0,0.5) are similar, data is informative enough to overwhelm both priors. Prior becomes irrelevant when n is large enough that the likelihood dominates: roughly `n > (σ_prior / SE_MLE)²`, which for logistic regression typically means a few hundred observations per coefficient.
3. Both intervals may have similar widths numerically, but the Bayesian HDI supports the statement "there is a 94% probability this parameter lies in this interval given the data observed," while the frequentist CI only supports "94% of intervals constructed this way cover the true parameter" — you cannot make a probability statement about a specific frequentist interval.

---

## SUBMISSION CHECKLIST

### Part 1 (Estimation Trinity)
- [ ] Q1: `n_As==40`, `n_A>3000`, `n_B>1000` — SELF-CHECK passes
- [ ] Q2: MLE/MAP/pull table printed; 3 posterior plots with HDI shading
- [ ] Q3: `p_A_greater > 0.90` — SELF-CHECK passes
- [ ] Reflect 1: All 3 questions answered

### Part 2 (Sequential Updating)
- [ ] Q4: `update_posterior()` — SELF-CHECK passes
- [ ] Q5: Sequential update run; 6-panel evolution plotted
- [ ] Q6: P(θ > 0.25) vs n plotted; Bayesian & frequentist thresholds annotated
- [ ] Q7: Dirichlet posterior — SELF-CHECK passes; marginal Betas plotted; 4th unseen category added
- [ ] Reflect 2: All 3 questions answered

### Part 3 (Multivariate Gaussians)
- [ ] Q8: μ, Σ, ρ — SELF-CHECK passes; scatter + 1σ/2σ/3σ ellipses plotted
- [ ] Q9: Conditional mean/std — SELF-CHECK passes
- [ ] Q10: κ > 100; marginalisation verified — SELF-CHECK passes
- [ ] Reflect 3: All 3 questions answered

### Part 4 (PGMs)
- [ ] Q11: BN fitted; forward P(Churn|Contract=M2M); backward P(Contract|Churn=1)
- [ ] Q12: Two DAGs drawn; agree/disagree E identified; SHAP alignment noted
- [ ] Q13: MRF built with BeliefPropagation; P(Churn) compared to BN and empirical
- [ ] Reflect 4: All 3 questions answered

### Part 5 (GP Regression)
- [ ] Q14: Mauna Loa loaded — SELF-CHECK passes
- [ ] Q15: Kernel table filled **before** coding; GP fitted; RMSE < 4.5 ppm
- [ ] Q16: Gap experiment; band widths inside/outside; inflation ratio printed
- [ ] Q17: Extrapolation plot; +5/+10/+15yr band widths; confidence boundary identified
- [ ] Reflect 5: Exactly 2 sentences comparing GP vs tree extrapolation

### Part 6 (MCMC)
- [ ] Q18: Scaling rationale written; model specified; 4-chain sampling run
- [ ] Q19: Trace plots; R̂ and ESS table; flagged parameters identified
- [ ] Q20: Prior sensitivity comparison plotted; robustness judgment stated
- [ ] Q21: 94% HDI computed; frequentist MLE compared; interpretation difference stated
- [ ] Q22: `telco_bayes_lr_v1.pkl` saved

### Submission Artefacts
- [ ] Fully executed `.ipynb` with all outputs visible
- [ ] `telco_bayes_lr_v1.pkl`
- [ ] One-page reflection: "Give one concrete example where the fully Bayesian answer changed a decision you would have made using only the MLE. Explain the mechanism."

---

## KNOWN GOTCHAS

| Issue | Fix |
|-------|-----|
| `pgmpy` DiscreteMLE needs string data | Cast all columns: `.astype(str)` |
| PyMC v5: `return_inferencedata` deprecated | Drop the argument (it's True by default) |
| seaborn RGB color cycle breaks `az.plot_trace` | The notebook's color-fix cell handles this — run it |
| `np.linalg.cond` on near-singular Sigma_3d may warn | Expected — kappa >> 100 is the correct result |
| GP with RBF trend fails RMSE check | Use `DotProduct` for the trend (linear extrapolation, not mean-reverting) |
| `ExpSineSquared` periodicity unstable if not fixed | Always set `periodicity_bounds='fixed'` at 1.0 year |
| `update_posterior` loop uses `.iterrows()` — slow for 500 rows | Acceptable here; no optimization needed |
| `az.hdi()` expects 1D array | Flatten: `idata.posterior['beta'].values[:,:,idx].flatten()` |

---

## REFERENCE FORMULAS

```
Beta posterior update:    Beta(α + k,  β + n - k)
MAP estimate:             (α + k - 1) / (α + β + n - 2)
MLE:                      k / n
Posterior mean:           (α + k) / (α + β + n)

Conditional Gaussian:
  μ_{1|2} = μ₁ + Σ₁₂ Σ₂₂⁻¹ (x₂ − μ₂)
  σ²_{1|2} = Σ₁₁ − Σ₁₂ Σ₂₂⁻¹ Σ₂₁

Dirichlet posterior:      Dir(α + counts)
Marginal of Dir:          Beta(αⱼ,  Σα − αⱼ)

Condition number:         κ(Σ) = λ_max / λ_min
```

---

*"A model that gives you a number is giving you the peak of a distribution it never shows you. Probabilistic models make the full distribution explicit."*

---
**Week 6 · Fusemachines AI Fellowship 2026 · Facilitator: Susan Ghimire**
