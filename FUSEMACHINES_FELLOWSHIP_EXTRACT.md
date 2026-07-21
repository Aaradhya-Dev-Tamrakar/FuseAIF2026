# Fusemachines AI Fellowship 2026 — Extracted Data

*Source: AARADHYA_MASTER_v137.md · Extracted July 3, 2026*
*v2 currency-check (July 8, 2026, against v143): 2 date-dependent claims corrected.*
*v3 update (July 10, 2026): Wk9 submission confirmed via Google Classroom screenshot ("Handed in," GitHub link attached, due date passed) — supersedes v143's "planning-stage, zero notebook cells built" snapshot, which predates completion. Runtime detail corrected same session: Colab T4 GPU, not Kaggle/CUDA as initially logged. Build-level metrics (accuracy figures, hyperparameters) remain user-reported, not verified against notebook/repo content itself. ~~Capstone project topic also resolved: **Ward office project, team-based** (not solo — supersedes the earlier onboarding-era solo recommendation), team includes an acquaintance of Aaradhya's, other members/full roster and technical domain-fit not yet confirmed.~~ — superseded, see v7: actual capstone is Vision Fairness & Bias Audit.*
*v4 update (July 10, 2026, same session): New **§2.5 Raw Classroom Grade Table** added — a full-gradebook screenshot surfaced 11 quiz/assignment entries never previously logged in any extract version or the master profile, several sitting underneath the numbered weekly projects already tracked in §2. Confirmed as fact by Aaradhya. Includes two unresolved flags: whether "W4: Linear Model Assignment"/"Linear Model Quiz Assignment" are the same deliverable as the tracked Week 4 project or a separate sub-item (content doesn't obviously match), and two generically-named rows ("Quiz"/"Assignment," both due 31 May) not mapped to any tracked week. Everything else in this extraction remains as confirmed in v2/v3 and is left untouched.*
*v5 update (July 11, 2026): Week 9's build-level metrics — flagged in v3/v4 as **user-reported, not independently verified** — checked directly against the executed notebook (`W9_NEU_Defect_CNN_Assignment.ipynb`, uploaded this session; 30/70 cells carry real execution output, confirming it's an actually-run notebook, not a task plan). **Four of five previously-logged figures were wrong, not just unconfirmed** — each traces to a real number in the notebook, just the wrong epoch/variant: Part A final train/val acc was logged as 0.986/0.847 (actual final, epoch 15: **0.988/0.789** — 0.986 was epoch 13's train_acc; 0.847 doesn't appear anywhere in the run); Part B was logged as a single "0.544" (actual: **three separate ablations** — aug-only 0.772, aug+BN 0.564, aug+BN+dropout(0.4) 0.592 final — 0.544 is the dropout variant's *epoch-8* reading, not its final one, and it's this last variant that was saved as `best_model.pt`); Part C grid search was logged as 0.6361 (actual: **0.6028**, config lr=0.01/batch_size=32); Part C Optuna was logged as 0.6333 (actual: **0.600**, lr≈0.0157/batch_size=42 — exact hyperparameters weren't previously on record at all). Only the from-scratch NN's 30,721,798-parameter count checked out exactly. §2 Week 9 entry rewritten below with corrected, source-verified figures; superseded numbers struck rather than silently dropped, per this tracker's own convention. New in this pass, not previously tracked: a StepLR scheduler ablation inside Part C (best grid config, without vs. with StepLR: 0.508 → 0.417 — scheduler hurt performance here). **CV was not updated this session** — stays as the July 11 version (system-facts-only Wk9 bullet, no figures), by direct instruction; this correction is tracker-only.*
*v6 update (July 21, 2026): Weeks 10 and 11 added — logged directly from cloned repo content, no `PATCH_*.md` was uploaded (§6 standard-session-mode fallback). **`fuseAiF_wk10_image_processing`**: `W10_Image_Processing_Assignment_executed.ipynb`, 17/19 code cells carry execution output; every README figure (47.3% combined-mask coverage, 96.9% custom-vs-cv2.Canny pixel agreement, 6 Hough circles, Q14 bbox) confirmed against actual notebook output, including the connected-components touching-apple separation claim verified against Q14's source code directly, not just its printed output. **`fuseAiF_wk11_vision_transformers`**: `W11_CV_Assignment_Notebook.ipynb`, 20/20 code cells carry execution counts, 19/20 carry output; every README figure (Q3 val_acc 74.1%, Q14 VAE 1,119,811 params + recon/KL trajectory, Q17 patch-embed shape (4,65,256), Q18 CLIP zero-shot 92.0%) confirmed exactly. Zero discrepancies in either week — unlike Wk9, both READMEs were accurate on first verification pass.*
*v7 update (July 21, 2026, same session): **Capstone topic superseded** — v3/v4's "Ward office project, team-based" is no longer current. Live portfolio (`projects.html`, P-018) confirms the actual capstone as **Vision Fairness & Bias Audit**: a diagnostic tool for deployed vision classifiers running a multi-demographic test matrix, flagging statistical disparities, and outputting a compliance report (detects bias, doesn't correct it); stack AIF360, Fairlearn, FairFace, UTKFace. Two-person team with **Tisha Manandhar** (github.com/tiixsha) — resolves v3/v4's "other members not yet confirmed." Progress tracked as 3 phases on-site: Feasibility & Scope (done) → Test Matrix & Detection Engine → Report & Compliance Output. In Progress, no repo README yet ("full README to follow in-repo," per site). Confirmed directly by Aaradhya as correct; Ward office was superseded, not concurrent. §7's domain-fit question is now resolved by this: capstone is squarely computer-vision, directly continuous with Wk10/Wk11's CV work (§8's "pick a topic where something clicked" directive is satisfied on its face — Aaradhya's two most recent, cleanly-verified weeks are both CV).*
*v8 update (July 21, 2026, same session): **Week 6 fully reworked and re-verified, superseding v7's stale entry.** At session start, `fuseAiF_wk6_probabilistic_models` still matched v7's logged repo structure (`W6_TaskPlan.md`, `TASK_PROGRESS.md` present) and the notebook was **not yet executed** — zero populated `execution_count`s, confirming v7's "Completed" framing described the task-plan/repo state, not a run notebook, matching the exact same gap v5 found and fixed for Wk9. `telco_bayes_lr_v1.pkl`, logged in v7 as an existing artifact, **did not exist in the repo at session start** — it was generated in Colab mid-session and pushed after. Over the session: notebook fully executed (31/31 code cells, sequential `execution_count` 1–31, zero error outputs); repo restructured (dev-tooling scaffolding — `.agents/`, `graphify-out/`, most of `misc/`, `W6_TaskPlan.md`, a stale `requirements.txt` that was actually a Jupyter-kernel dump, never the notebook's real `pymc`/`arviz`/`pgmpy` deps — removed; `docs/` consolidated); `telco_bayes_lr_v1.pkl` (345MB / 362,171,342 bytes) added via Git LFS and confirmed as a genuine LFS pointer post-push, not a raw blob; `README.md` rewritten (prior version referenced four since-deleted files and never mentioned `Reflection.md`); `Reflection.md` written (384 words, grounded in two figures pulled directly from executed-cell output); 8 vestigial answer-template placeholder lines removed from the notebook (cells 10, 20, 28, 37, 41, 48, 51, 62 — real content already existed above every one; only leftover scaffolding text was stripped). Full detail in §2 below. **Separately, resolves a flag standing since v4**: §2.5's cut-off row ("Due 5 Jun, 22:00 • Assignments," no title, top of screenshot) is this Week 6 notebook Assignment — due date/points/facilitator (100 pts, Susan Ghimire) match exactly what the assignment page itself states. Submission channel independently confirmed the same way v3 confirmed Wk9: a Google Classroom screenshot (this session) shows "Your work: Handed in," GitHub link attached. **Important caveat, unlike Wk9's clean confirmation:** that screenshot was taken *before* this session's rework — the notebook behind the "Handed in" link was still the unexecuted skeleton at screenshot time. The GitHub-link submission mechanism means the same Classroom record now points at substantially different, since-completed content; Classroom itself was not re-checked after the rework, so "Handed in" is confirmed but the grade/score is not, mirroring Wk9's still-open "score not yet posted" gap.*

---

## 1. Program Facts

| Field | Value |
| --- | --- |
| Program | Fusemachines AI Fellowship 2026 |
| Role | Fuse AI Fellow |
| Duration | 24 weeks (6 months) |
| Start | May 4, 2026 (Wk1 Monday) |
| End | Oct 18, 2026 (Sunday) |
| Cadence | Mon–Sun weekly cycle, flips every Monday 00:00 NPT |
| Current status (as of July 21, 2026) | **Wk 12/24, ongoing.** Wk10 (Image Processing) and Wk11 (Vision Transformers) both complete and source-verified (v6) — see §2 entries below. Capstone confirmed: Vision Fairness & Bias Audit, w/ Tisha Manandhar (v7). |
| Week formula | `floor((today − May 4 2026) / 7) + 1`, capped at 24 |
| Facilitator | **Season** |
| WK8 lecture presenter | Susan Ghimire |
| WK6 assignment facilitator | Susan Ghimire (v8 — posted the Probabilistic Models notebook assignment itself, distinct from the WK8 lecture-presenter role above; both roles confirmed independently, not necessarily the same scope) |
| Admission | Passed entrance exam (March 2026): linear algebra, calculus, probability, Python, ML |
| Submission channel | Google Classroom (AI Fellowship 2026) |

**Status label convention (do not misread):** "Wks N complete" ≠ program finished. Do not infer "complete" before Oct 18, 2026.

---

## 2. Week-by-Week Deliverables

### Week 2 — Customer REST API *(no standalone project entry; CV bullet only)*

- Containerized customer REST API: FastAPI + PostgreSQL + Docker, 4-layer architecture, asyncio concurrency.
- **Instructor feedback (week unconfirmed, likely Wk 2/3/4):** monolithic single-file API structure flagged — declutter into subfolders, use separate `APIRouter` per domain (e.g. `routers/auth.py`, `routers/query.py`, `routers/results.py`) instead of flat root.
  - **Apply-forward rule:** all new FastAPI projects (fellowship or Nexus) must use `APIRouter` per domain from day one. No monolithic `main.py`. Minimum structure: `app/routers/`, `app/models/`, `app/db/`, `app/core/`.
  - Status: ⏳ not yet retroactively applied.
- **Score (added v4, source: Classroom screenshot July 10, 2026):** "Wk2 Problem Set: Software Development Concepts" — **75/100**, due May 19. See §2.5 for full raw Classroom grade table.

### Week 3 — Text-to-SQL Agentic Pipeline *(Completed — Rating 8.7/10)*

- **Stack:** Python · FastAPI · Streamlit · PostgreSQL · Docker · OpenAI API · Prompt Chaining
- Production-grade Text-to-SQL pipeline + state-based FastAPI SQL Agent over `classicmodels` PostgreSQL DB.
- Modular workflow: Planner → Generator → Validator → Executor → Summarizer, self-correction up to 3 retries.
- GPT-4o-mini prompt-chaining, rule-based SQL safety validation (blocks DML/DDL), structured JSON query logging.
- **100.0% execution success, 100.0% result accuracy** on 50-question benchmark, zero retries required.
- Streamlit chat interface, Docker/Docker Compose containerized.
- Repo: `AaradhyaDT/fuseAiF_wk3_text2sql`

### Week 4 — Telco Customer Churn & CLV ML Pipeline *(Completed — Rating 8.5/10)*

- **Stack:** Python · Scikit-learn · Pandas · NumPy · Matplotlib · Seaborn · Papermill
- End-to-end classification + regression pipeline for churn and CLV.
- Stratified 70/15/15 split; Logistic Regression / Ridge / SGD classifiers benchmarked.
- Custom threshold 0.385 → top-200 high-risk budget segment.
- Ridge Regression best for CLV (mean CLV $1,304.70); Lasso L1 paths plotted.
- Stratified 5-fold CV: ROC-AUC 0.841 ± 0.005; learning curves + leakage simulation.
- Papermill automation, full HTML report export, Graphify knowledge-graph integration.
- Repo: `AaradhyaDT/FUSE_AIF_2026_M1` (under `WK4/`)

### Week 5 — Telco Churn Tree-Based Ensemble Pipeline *(Completed — Rating 9.0/10, highest fellowship score)*

- **Stack:** Python · Scikit-learn · XGBoost · imbalanced-learn · SHAP · Joblib · Matplotlib
- Dataset: Telco Customer Churn, 7,043 rows, ~27% positive rate.
- Random Forest + XGBoost vs. naïve baseline; AUROC/Precision/Recall/F1 (accuracy trap exposed).
- `ColumnTransformer` for mixed dtypes; `ImbPipeline` (imbalanced-learn) restricts SMOTE to training folds — zero leakage.
- Grid Search / Bayesian optimization on XGBoost hyperparameters.
- SHAP global summary (Q15) + local waterfall/force plot (Q16); 2-sentence retention recommendation.
- Production serialization: full pipeline saved via `joblib` → `telco_churn_pipeline_v1.joblib`.
- Secondary regression task: `tenure` prediction — dropped `TotalCharges` (leakage column); unconstrained Decision Tree vs. regularized XGBoost Regressor; 5-fold CV learning curves show overfitting in baseline vs. generalization in XGBoost; extrapolation-bound check on tree predictions.
- Model Card (Q18) completed with real metrics.
- Repo: `AaradhyaDT/fuseAiF_wk5_telco_churn_ensembles`

### Fellowship Prep Toolkit *(Completed, Rating 6.5/10 — supplementary, not a numbered week)*

- 50-question mock exam widget + 7-tab interactive HTML cheatsheet (linear algebra, calculus, probability, Python/CS, ML).

### Week 6 — Probabilistic Models & Bayesian Inference *(Rating 8.2/10 predates this session — see caveat below; notebook fully executed and repo restructured, source-verified July 21, 2026, v8)*

**⚠ Provenance note (v8):** the same execution/repo-state gap v5 found for Wk9 applied here — v7's "Completed" entry described a repo with `W6_TaskPlan.md`/`TASK_PROGRESS.md` still present and a notebook with zero populated `execution_count`s, i.e. task-plan/scaffolding state, not a run. `telco_bayes_lr_v1.pkl`, logged in v7 as an existing artifact, was not actually in the repo yet. Both gaps closed this session.

- **Stack (confirmed):** Python · PyMC · ArviZ · pgmpy · scikit-learn · statsmodels · Pandas · NumPy · Matplotlib · Seaborn
- **Repo (confirmed, restructured):** `AaradhyaDT/fuseAiF_wk6_probabilistic_models`, notebook `W6_Probabilistic_Models_Assignment.ipynb` — 64 cells, **31/31 code cells executed, sequential `execution_count` 1–31, zero error outputs.**
- **Current repo structure:** `README.md` (rewritten this session — prior version referenced `W6_TaskPlan.md`/`TASK_PROGRESS.md`/`requirements.txt`, all since deleted, and never mentioned `Reflection.md`), `Reflection.md` (new), `W6_Probabilistic_Models_Assignment.ipynb`, `telco_bayes_lr_v1.pkl` (Git LFS), `docs/W6_Probabilistic_Models_Resource_Guide.pdf`, `docs/GIT_LFS_GUIDE.md`, plus `.gitattributes`/`.gitignore`/`LICENSE`/`CHANGELOG.md`. **Removed:** `.agents/`, `graphify-out/`, most of `misc/`, `W6_TaskPlan.md`, `requirements.txt` — the last of these was a stale Jupyter-kernel environment dump (`ipykernel`, `jedi`, `traitlets`...) that never actually matched the notebook's real dependencies (`pymc`/`arviz`/`pgmpy` never appeared in it); the notebook installs its own deps from its setup cell, so no `requirements.txt` is needed.
- **Part 1 — MLE/MAP/full posterior (Beta(2,8) prior), confirmed:** Group A (M2M, large) n=3875, k=1655, rate 0.4271 → MLE 0.4271 / MAP 0.4265, pull 0.0006. **Group A_small (n=40)** k=15, rate 0.3750 → MLE 0.3750 / MAP 0.3333, **pull 0.0417 — ~70× larger than the large-group pulls**, directly demonstrating why the assignment's small-segment framing (a 40-customer contract tier) needs the full posterior, not a bare MLE. Group B (2yr, large) n=1695, k=48, rate 0.0283 → MLE 0.0283 / MAP 0.0288, pull 0.0005. Monte Carlo (10,000 samples, seed 42): **P(θ_A > θ_B) = 1.0000.**
- **Part 6 — Bayesian logistic regression, PyMC/NUTS, confirmed:** features scaled before sampling; priors `Normal(0,2)` on β / `Normal(0,5)` on intercept, no `pm.Flat()`; **R̂ 1.000–1.001 across all 6 parameters, bulk-ESS 5,021–7,238** (both convergence thresholds cleared); trace plot rendered with populated axes. Q21 (Bayesian vs. frequentist): posterior mean **1.2932** (sd 0.1068), 94% HDI **[1.0845, 1.4920]**, vs. frequentist MLE **1.2927** — near-identical point estimates, but only the HDI supports a direct probability statement about this specific interval.
- **Artifact:** `telco_bayes_lr_v1.pkl` — **345MB (362,171,342 bytes exact)**, PyMC `InferenceData` trace (4 chains × 2,000 draws), generated in Colab mid-session (did not exist in the repo at session start), pushed via **Git LFS** and confirmed post-push as a genuine 134-byte LFS pointer (`oid sha256:6b56735f...`), not a raw blob — would otherwise have hard-failed the push at GitHub's 100MB cap. A reload-integrity check (`pickle.load()` round-trip, chain/draw-count asserts) was added to the notebook's save cell and passes: 4 chains × 2,000 draws intact.
- **Reflection.md (new):** 384 words. Grounded in the two figures above — Group A_small's outsized MAP/MLE pull as the concrete "MLE-only decision would have been wrong" case tied to the assignment's own VP small-segment framing, and the HDI-vs-frequentist-CI interpretation gap from Q21.
- **Notebook hygiene:** 8 vestigial answer-template placeholder lines removed (cells 10, 20, 28, 37, 41, 48, 51, 62) — every one had real, substantive content already written above it; only leftover `> *Your answer:* Completed with...`-style scaffolding text and two bare empty prompts were stripped. Zero placeholder markers remain anywhere in the notebook post-cleanup.
- **Submission (confirmed, with caveat):** Google Classroom shows **"Handed in,"** GitHub repo link attached, assignment posted by **Susan Ghimire**, 100 pts, due **5 Jun, 22:00**. Screenshot is from this session but **predates the rework above** — the notebook behind the link was still unexecuted at screenshot time. Classroom was not re-checked after the rework; grade/score not yet posted or confirmed. This also resolves a flag standing since §2.5/v4 — see below.
- Deliverables covered (topic list, unchanged from v7, still accurate): Bayesian estimation (MLE/MAP/full Bayes), sequential updating, Dirichlet-multinomial inference, multivariate Gaussian conditioning, probabilistic graphical models (Bayesian Network + MRF), Gaussian process regression, PyMC Bayesian logistic regression.
- Portfolio entry: live on `aaradhyadtmr.github.io` (not re-verified this session).

### Week 7 — Clustering / Customer Segmentation Assignment *(Completed June 12, 2026 — Rating 8.0/10)*

- **Stack:** Python · scikit-learn · scipy · Pandas · NumPy · Matplotlib · Seaborn · NearestNeighbors
- **Dataset:** UCI Online Retail II (~500,000 transactions, `Year 2010-2011` sheet)
- **Repo:** `AaradhyaDT/fuseAiF_wk7_customer_segmentation`
- Context: market segmentation from raw unlabeled transaction data.
- Pipeline: RFM feature engineering + extended features (AvgBasketSize, AvgDaysBetweenPurchases, UniqueProducts, ReturnRate) + category spend ratios (keyword-bucketed `Description` → ≥5 categories) → outlier detection (IQR vs Z-score) → scaler choice (StandardScaler vs RobustScaler) → K-Means (Elbow + Silhouette, k-means++ vs random init) → Hierarchical (Ward/Complete/Average/Single dendrograms; fit Ward + Complete) → DBSCAN (k-distance ε estimation, ≥3 param combos, noise analysis) → validation (Silhouette / Davies-Bouldin / Calinski-Harabasz) → business narrative + executive summary → failure log (≥3 entries).
- Status: notebook executed end-to-end (S0–S9), submitted as `Week_7_Clustering_Assignment_executed.ipynb`. Repo organized: root has notebook/PDF/plots/README/LICENSE/.gitignore (raw `.xlsx` gitignored); dev artifacts archived under `misc/`.
- Submission: due June 21, 2026, via Google Classroom.
- Portfolio: live in `projects.html` (v113).

### Week 8 — Forecasting Assignment *(Completed June 27, 2026 — Rating 8.1/10)*

- **Stack:** Python · statsmodels (SARIMA/SARIMAX, Holt-Winters) · Prophet · LightGBM · TensorFlow/Keras (LSTM) · XGBoost · scikit-learn · Pandas · NumPy · Matplotlib
- **Dataset:** Monthly S&P 500 Index, 1990–2024 (420 months), nominally via `yfinance`
- **Repo:** `AaradhyaDT/fuseAiF_wk8_sp500_forecasting`
- Context: classical-to-modern forecasting comparison — 9 forecasters, then test whether an ensemble beats the best single model.
- **Sandbox constraint:** yfinance network access blocked in execution environment → seeded synthetic lognormal-walk fallback with injected −34% single-month shock (mirrors March 2020 COVID crash); fallback logic documented in Q1 cell.
- Pipeline: data prep + missing-data strategy comparison → ACF/PACF diagnostics (log returns, differenced log) → SARIMA(1,1,1)(0,1,1,12) with residual diagnostics → Holt-Winters → Prophet (component decomposition) → LightGBM (recursive, feature importance + prediction intervals) → LSTM → XGBoost (recursive) → naive/seasonal-naive baselines → MASE/RMSE comparison → error breakdowns by calendar-month and horizon → 4-model ensemble (Holt-Winters + SARIMA + LSTM + XGBoost) → Diebold-Mariano significance test → investment-memo recommendation.
- **Results:** Ensemble best overall — **MASE 2.44 / RMSE 96.7**, ahead of Holt-Winters (2.66/110.4) and SARIMA (2.70/112.4). Diebold-Mariano **p = 0.0092** (significant at 5%). Naive baseline MASE 4.06. Prophet (7.82) and MLP (24.47) worst on this series.
- Recommendation: deploy 4-model ensemble for production accuracy; keep Holt-Winters as interpretable low-latency fallback for regulatory contexts.
- **Known unresolved issue:** SARIMA residuals fail Ljung-Box at seasonal lags (12, 24) — diagnosed fix is increasing seasonal MA/AR order; not refit this cycle.
- Status: notebook executed end-to-end, 23 questions complete, 8 discussion questions answered, 5 AI-prompt critique entries logged. Repo organized: root has executed notebook/PDF/`assignment/sp500_sarima_v1.pkl`/`plots/` (12 figures)/README/LICENSE/.gitignore; dev tools under `tools/`, task docs under `docs/`, discussion logs under `misc/`.
- Submitted June 27, 2026, via Google Classroom.
- **Portfolio: NOT yet added to `projects.html` — pending trigger.**

**WK8 Class Lecture Notes** *(Complete — June 28, 2026, 17:12–19:00 NPT, presenter Susan Ghimire)*
Full notes archived separately: `PATCH_fuseWk8_forecasting_lecture_20260628_v2.md`
Topics (slides 22–69): time series ordering & lag (NLP positional analogy) · trend/seasonality/noise components (additive vs multiplicative) · exponential smoothing family (Naïve→Holt-Winters, ETS notation) · AR models (lag construction) · MA models (past errors, q) · ACF/PACF (p/q/s selection rules) · stationarity (ADF/KPSS, differencing order d) · SARIMA/auto_arima/SARIMAX (7 params, AIC, exogenous constraints) · Monte Carlo uncertainty propagation · evaluation (ME, Forecast Ratio, horizon uncertainty cone).

### Week 9 — NEU Steel Defect CNN Classifier *(Submitted July 9, 2026, "Handed in" — confirmed via Google Classroom screenshot, July 10; build metrics source-verified against the executed notebook, July 11)*

**⚠ Provenance note:** as of v143 (written before submission), master profile status was "planning-stage, task plan complete, zero notebook cells built." Submission itself is **source-verified** — Google Classroom shows "Handed in" with GitHub link `AaradhyaDT/fuseAiF_wk9_neu_defect_cnn` attached, due date passed. Assignment context also verified from the same screenshot: instructor Rakshya Lama Moktan, posted July 1, 100 pts, due July 9 20:45 NPT, SmartForge Manufacturing defect-classification scenario, NEU Surface Defect Database (Kaggle-hosted dataset, 1,800 grayscale 200×200 images, 6 classes, 300/class), loaded via `torchvision.datasets.ImageFolder`. **Build-level metrics below are now source-verified** against `W9_NEU_Defect_CNN_Assignment.ipynb` directly (uploaded July 11) — 30 of 70 cells carry real execution output. ~~Previously flagged as user-reported/unverified~~ — superseded; see v5 changelog note above for what changed and why.

- **Stack (confirmed):** Python · PyTorch · torchvision · scikit-learn · Optuna · Matplotlib · NumPy · Pillow
- **Repo (confirmed):** `AaradhyaDT/fuseAiF_wk9_neu_defect_cnn`, notebook `W9_NEU_Defect_CNN_Assignment.ipynb`
- **Dataset:** NEU-DET surface defect classification, 6 classes (crazing, inclusion, patches, pitted surface, rolled-in scale, scratches), 1,440 train / 360 val, 200×200 RGB.
- **Part 0 — from-scratch 2-layer NN:** 30,721,798 params (Linear(120000→256)→ReLU→Linear(256→6)). Confirmed correct as originally logged.
- **Part A — CNN classifier (confirmed, 15 epochs):** ~~final train/val accuracy 0.986/0.847~~ → **final train_acc 0.988 / val_acc 0.789** (epoch 15 exactly; 0.986 was epoch 13's train_acc, 0.847 does not appear anywhere in the run). Classification report on the 360-image validation set confirms 0.789 overall accuracy (macro F1 0.779); weakest class is `scratches` (recall 0.450), strongest is `inclusion` (F1 0.862).
- **Part B — hardening (confirmed, 15 epochs each, three separate ablations, not one figure):**
  - Augmentation only: final val_acc **0.772**
  - - BatchNorm2d: final val_acc **0.564**
  - - BatchNorm2d + Dropout(0.4): final val_acc **0.592** — ~~previously logged as 0.544~~ (that was this variant's epoch-8 reading, not its final one)
  - `best_model.pt` saved from the **BN+Dropout(0.4) variant** (0.592) — not the highest-val-acc checkpoint in Part B (that's aug-only at 0.772); the notebook's own comment calls it "best-performing," which appears to mean "final hardened model," not top accuracy.
- **Part C — hyperparameter tuning (confirmed):**
  - Grid search (lr ∈ {0.001, 0.01} × batch_size ∈ {16, 32}, 15 epochs each): best config **lr=0.01, batch_size=32 → val_acc 0.6028** — ~~previously logged as 0.6361~~
  - StepLR ablation on the best grid config *(not previously tracked)*: without StepLR val_acc 0.508, with StepLR val_acc 0.417 — scheduler hurt performance here.
  - Optuna (best trial): **lr≈0.0157, batch_size=42 → val_acc 0.600** — ~~previously logged as 0.6333, hyperparameters not previously recorded~~
- **Runtime (corrected July 10):** all cells run and finalized in **Google Colab, T4 GPU runtime** — not Kaggle/CUDA-auto-detect as an earlier session note stated; that detail is superseded.
- **Confirmed independently:** submitted on time, July 9, 2026, "Handed in" status, GitHub link attached, all build-level metrics above verified against actual notebook output. **Still not confirmed:** exact Classroom score/grading (not yet posted).

### Week 10 — Image Processing / FreshTrack CV Pipeline *(Source-verified July 21, 2026 — repo-verified, submission/grading status not yet confirmed)*

- **Stack (confirmed):** Python · OpenCV · NumPy · Matplotlib · kagglehub
- **Repo (confirmed):** `AaradhyaDT/fuseAiF_wk10_image_processing`, notebook `W10_Image_Processing_Assignment_executed.ipynb` — 17/19 code cells carry execution output.
- **Dataset:** Fruits-360 via kagglehub, mapped to 6 required classes (red_apple, green_apple, banana, strawberry, orange, lime) + 3 instructor-provided images (morphology.png, chessboard.png, mixed_fruit_bowl.jpeg).
- **Part A — Color Space & Fruit Segmentation (confirmed):** BGR/RGB channel-order explanation; per-fruit HSV `inRange()` masks; multi-class segmentation on the bowl image — combined mask covers **47.3%** of the image (only apple/banana/orange present in that bowl; strawberry/green_apple/lime absent from the scene, not a masking failure).

> **Note:** Wk10 Part B onward, Wk11 full entry, §2.5, §3, §4, §5, §6 unchanged from v7 — omitted here for length; carried forward as-is except the two edits below.

---

## 2.5 Raw Classroom Grade Table — Flags

**Flag resolved (v8):** the cut-off row noted below since v4 ("Rows above 'Probabilistic Models Quiz'... partially visible header text 'Due 5 Jun, 22:00 • Assignments' with no title") is **the Week 6 notebook Assignment itself** — due date, points (100), and facilitator (Susan Ghimire) all match the assignment page exactly (see §2, Week 6, "Submission" bullet). Score not visible in the original truncated screenshot; not resolved by this session's later Classroom screenshot either, since that one only showed the "Your work" submission panel, not the gradebook row. The row directly below it in the table ("Probabilistic Models Quiz | 5 Jun, 22:00 | Quiz | Handed in") remains a **separate** graded item — the quiz component, distinct from the notebook assignment.

**Remaining flags, unchanged from v4:**

- "W4: Linear Model Assignment" (88/100) and "Linear Model Quiz Assignment" (23/25), both due 28 May — same due date as the tracked §2 Week 4 project, but content doesn't obviously match; not confirmed as the same or a separate deliverable.
- Two unlabeled rows ("Quiz" and "Assignment," both due 31 May, 09:44) — not mapped to any tracked week.
- No score column exists for "Handed in"-only rows.

*(Full raw grade table unchanged from v7 — not reproduced here.)*

---

## 4. Project Ranking — Week 6 row updated

| Rank | Item | Score | Status |
| --- | --- | --- | --- |
| 5 | Wk6 — Probabilistic Models & Bayesian Inference | 8.2 | Rating predates this session; **notebook fully executed + repo restructured, source-verified July 21, 2026 (v8)**; Classroom "Handed in" confirmed but pre-rework, score not yet posted |

*(All other rows unchanged from v7 — not reproduced here.)*

---

## 7. Open Items / Pending Actions — new item (v8)

- **Wk6 Classroom re-check (new, v8):** submission channel confirmed "Handed in" via screenshot, but that screenshot predates this session's rework (notebook was unexecuted at the time it was taken). Classroom has not been re-checked against the reworked repo/notebook. Score not yet posted.

*(All other open items — portfolio triggers for Wk8/10/11, APIRouter refactor, Nexus compliance, CV status label, Wk9/10/11 grading verification, capstone domain-fit — unchanged from v7, not reproduced here.)*

---

**Note on this v8 extract:** to keep this update focused on what actually changed, §2 Wk10 (Part B onward)/Wk11, §3 (CV Summary), §5 (Dev Standards Gate), §6 (Session Protocol), and §8 (Known Constraint) are **carried forward verbatim from v7** and were not reproduced in full above — merge this file's Week 6/§2.5/§4/§7 edits into the v7 base rather than treating this as a standalone replacement.
