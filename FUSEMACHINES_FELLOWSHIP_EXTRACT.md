# Fusemachines AI Fellowship 2026 — Extracted Data

*Source: AARADHYA_MASTER_v137.md · Extracted July 3, 2026*
*v2 currency-check (July 8, 2026, against v143): 2 date-dependent claims corrected.*
*v3 update (July 10, 2026): Wk9 submission confirmed via Google Classroom screenshot ("Handed in," GitHub link attached, due date passed) — supersedes v143's "planning-stage, zero notebook cells built" snapshot, which predates completion. Runtime detail corrected same session: Colab T4 GPU, not Kaggle/CUDA as initially logged. Build-level metrics (accuracy figures, hyperparameters) remain user-reported, not verified against notebook/repo content itself. ~~Capstone project topic also resolved: **Ward office project, team-based** (not solo — supersedes the earlier onboarding-era solo recommendation), team includes an acquaintance of Aaradhya's, other members/full roster and technical domain-fit not yet confirmed.~~ — superseded, see v7: actual capstone is Vision Fairness & Bias Audit.*
*v4 update (July 10, 2026, same session): New **§2.5 Raw Classroom Grade Table** added — a full-gradebook screenshot surfaced 11 quiz/assignment entries never previously logged in any extract version or the master profile, several sitting underneath the numbered weekly projects already tracked in §2. Confirmed as fact by Aaradhya. Includes two unresolved flags: whether "W4: Linear Model Assignment"/"Linear Model Quiz Assignment" are the same deliverable as the tracked Week 4 project or a separate sub-item (content doesn't obviously match), and two generically-named rows ("Quiz"/"Assignment," both due 31 May) not mapped to any tracked week. Everything else in this extraction remains as confirmed in v2/v3 and is left untouched.*
*v5 update (July 11, 2026): Week 9's build-level metrics — flagged in v3/v4 as **user-reported, not independently verified** — checked directly against the executed notebook (`W9_NEU_Defect_CNN_Assignment.ipynb`, uploaded this session; 30/70 cells carry real execution output, confirming it's an actually-run notebook, not a task plan). **Four of five previously-logged figures were wrong, not just unconfirmed** — each traces to a real number in the notebook, just the wrong epoch/variant: Part A final train/val acc was logged as 0.986/0.847 (actual final, epoch 15: **0.988/0.789** — 0.986 was epoch 13's train_acc; 0.847 doesn't appear anywhere in the run); Part B was logged as a single "0.544" (actual: **three separate ablations** — aug-only 0.772, aug+BN 0.564, aug+BN+dropout(0.4) 0.592 final — 0.544 is the dropout variant's *epoch-8* reading, not its final one, and it's this last variant that was saved as `best_model.pt`); Part C grid search was logged as 0.6361 (actual: **0.6028**, config lr=0.01/batch_size=32); Part C Optuna was logged as 0.6333 (actual: **0.600**, lr≈0.0157/batch_size=42 — exact hyperparameters weren't previously on record at all). Only the from-scratch NN's 30,721,798-parameter count checked out exactly. §2 Week 9 entry rewritten below with corrected, source-verified figures; superseded numbers struck rather than silently dropped, per this tracker's own convention. New in this pass, not previously tracked: a StepLR scheduler ablation inside Part C (best grid config, without vs. with StepLR: 0.508 → 0.417 — scheduler hurt performance here). **CV was not updated this session** — stays as the July 11 version (system-facts-only Wk9 bullet, no figures), by direct instruction; this correction is tracker-only.*
*v6 update (July 21, 2026): Weeks 10 and 11 added — logged directly from cloned repo content, no `PATCH_*.md` was uploaded (§6 standard-session-mode fallback). **`fuseAiF_wk10_image_processing`**: `W10_Image_Processing_Assignment_executed.ipynb`, 17/19 code cells carry execution output; every README figure (47.3% combined-mask coverage, 96.9% custom-vs-cv2.Canny pixel agreement, 6 Hough circles, Q14 bbox) confirmed against actual notebook output, including the connected-components touching-apple separation claim verified against Q14's source code directly, not just its printed output. **`fuseAiF_wk11_vision_transformers`**: `W11_CV_Assignment_Notebook.ipynb`, 20/20 code cells carry execution counts, 19/20 carry output; every README figure (Q3 val_acc 74.1%, Q14 VAE 1,119,811 params + recon/KL trajectory, Q17 patch-embed shape (4,65,256), Q18 CLIP zero-shot 92.0%) confirmed exactly. Zero discrepancies in either week — unlike Wk9, both READMEs were accurate on first verification pass.*
*v7 update (July 21, 2026, same session): **Capstone topic superseded** — v3/v4's "Ward office project, team-based" is no longer current. Live portfolio (`projects.html`, P-018) confirms the actual capstone as **Vision Fairness & Bias Audit**: a diagnostic tool for deployed vision classifiers running a multi-demographic test matrix, flagging statistical disparities, and outputting a compliance report (detects bias, doesn't correct it); stack AIF360, Fairlearn, FairFace, UTKFace. Two-person team with **Tisha Manandhar** (github.com/tiixsha) — resolves v3/v4's "other members not yet confirmed." Progress tracked as 3 phases on-site: Feasibility & Scope (done) → Test Matrix & Detection Engine → Report & Compliance Output. In Progress, no repo README yet ("full README to follow in-repo," per site). Confirmed directly by Aaradhya as correct; Ward office was superseded, not concurrent. §7's domain-fit question is now resolved by this: capstone is squarely computer-vision, directly continuous with Wk10/Wk11's CV work (§8's "pick a topic where something clicked" directive is satisfied on its face — Aaradhya's two most recent, cleanly-verified weeks are both CV). Struck rather than deleted below, per this tracker's convention.*

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

### Week 6 — Probabilistic Models Assignment *(Completed — Rating 8.2/10 — source-verified July 21, 2026)*

- **Stack:** Python · PyMC · ArviZ · pgmpy · scikit-learn · Pandas · Matplotlib · Seaborn
- Repo structure: `W6_Probabilistic_Models_Assignment.ipynb`, `W6_TaskPlan.md`, `TASK_PROGRESS.md`, `W6_Probabilistic_Models_Resource_Guide.pdf`.
- Deliverables: Bayesian estimation (MLE/MAP/full Bayes), sequential updating, Dirichlet-multinomial inference, multivariate Gaussian conditioning, probabilistic graphical models, Gaussian process regression, PyMC Bayesian logistic regression.
- Artifact: `telco_bayes_lr_v1.pkl` (Bayesian logistic regression trace).
- **Verification note (v7):** an earlier pull from the `FuseAIF2026` monorepo archive showed only 8/31 code cells executed (`execution_count: null` from the sequential-updating step onward), with the repo's own `TASK_PROGRESS.md` stating execution was still pending — that copy was stale. The standalone submission repo `AaradhyaDT/fuseAiF_wk6_probabilistic_models` confirms 31/31 code cells fully executed, and the pickle-save cell's real output confirms `telco_bayes_lr_v1.pkl` genuinely exists (4 chains × 2000 draws, reload-verified). Site card (P-008) and this entry are both accurate; no changes needed to either.
- Portfolio entry: live on `aaradhyadtmr.github.io`.

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
- **Part B — Morphology & Denoising (confirmed):** erosion/dilation/opening/closing/gradient on `morphology.png` (thin cursive stroke — erosion nearly erases it, dilation thickens substantially, opening/closing near-inert since there are no small specks/holes to remove); Gaussian/median/bilateral filter comparison on injected noise (median best for salt-and-pepper, bilateral best edge-preservation on Gaussian noise).
- **Part C — Edge Detection (confirmed):** Canny implemented from scratch (Sobel gradient → non-max suppression → double threshold → hysteresis); custom-vs-`cv2.Canny()` pixel agreement **96.9%**, remaining divergence attributed to `cv2.Canny()`'s internal Sobel aperture/L2gradient defaults and 8-connectivity hysteresis queues.
- **Part D — Feature Detection (confirmed):** Harris corner detection with threshold sweep on `chessboard.png`; Hough circle transform on the bowl image, tuned for real (not synthetic-default) parameters — **6 circles detected**; full single-fruit pipeline (Q14) — HSV mask → morphological open/close → distance-transform + `connectedComponents` peak-separation for touching same-color fruit (verified against Q14's actual source: the raw HSV mask alone returns one blob spanning all 5 apples; distance-transform peaks + component labeling recovers individual fruit centers) → Canny on the isolated mask → bounding box. Output saved and confirmed: `q14_pipeline_red_apple_1.jpg`, bbox x=698 y=379 w=286 h=315.
- **Known handling detail:** notebook normalizes the uploaded `mixed_fruit_bowl.jpeg` filename to `mixed_bowl.jpg` mid-run to resolve a dataset-naming mismatch — confirmed present in the executed run, not a bug.
- **Not yet confirmed:** Classroom submission status/date, grading score. Repo/notebook content is source-verified; submission tracking is not.

### Week 11 — Computer Vision with Deep Learning / Vision Transformers *(Complete — repo-verified July 21, 2026; presenter Susan Ghimire per project guide, consistent with Wk8; submission/grading status not yet confirmed)*

- **Stack (confirmed):** Python · PyTorch · torchvision · timm · onnxruntime · onnxscript · CLIP (`openai/CLIP`)
- **Repo (confirmed):** `AaradhyaDT/fuseAiF_wk11_vision_transformers`, notebook `W11_CV_Assignment_Notebook.ipynb` — 20/20 code cells carry execution counts, 19/20 carry output (Run 4, per README; confirmed as a genuine executed run, not a task plan).
- **Business scenario (from project guide):** Computer Vision Engineer at QuickVision AI, replacing a ~45%-accuracy HSV baseline across 500 warehouse cameras; deliverable spans 5 modules answering two questions — best model family for reliable classification, and how to onboard a new product type with zero labelled images.
- **Module 1 — CNN Classification (Q1–Q5, confirmed):** ResNet-50 transfer learning, 20,490 trainable / 23,528,522 total params (0.087% trainable) — final val_acc **74.1%** (epoch 3 of 3; train 56.7%→73.0%→77.5%, val 69.7%→74.1%→74.1%). GradCAM implemented (Q4).
- **Module 2 — Object Detection (Q6–Q9, confirmed):** IoU from scratch (matches expected 0.13/0.0/1.0 reference cases); NMS from scratch (kept indices [0,3], matches expected); Faster R-CNN — bus.jpg 5 detections, people.jpg 3 detections.
- **Module 3 — Segmentation (Q10–Q13, confirmed):** DeepLabv3+ — bus.jpg → background/bus/car/person, people.jpg → background/person; pixel accuracy 1.0 (perfect synthetic mask) / 0.37 (random, ~expected 0.33); mIoU 1.0 (perfect) / matching random-baseline expectation.
- **Module 4 — Generative / VAE (Q14–Q16, confirmed):** 1,119,811 params; 3-epoch trajectory — recon loss 170.7→123.2→87.5, KL 45.8→276.6→267.9. Latent-space interpolation visualized (Q15).
- **Module 5 — ViT + Deployment (Q17–Q20, confirmed):** patch embedding output shape (4, 65, 256) matching expected, 64 patches = (32/4)²; CLIP zero-shot **92.0%** on 200-image test slice — real run, not the scaffold's fallback stub; ONNX export 94.2 MB, verified with onnxruntime; final comparison table + deployment memo.
- **Notable result (confirmed, flagged in own README):** CLIP zero-shot (92.0%) outscored the fine-tuned ResNet-50 (74.1%) on this test slice — reverse of the typical zero-shot/supervised ordering. Memo's phased-deployment recommendation is driven by latency/explainability, not an assumed accuracy edge.
- **Bugs found and fixed during execution (confirmed from README, consistent with a real debugging pass rather than a clean-first-try log):** Q4 GradCAM — `RuntimeError` on `.numpy()` from a grad-tracked tensor, fixed with `.detach()`; Q10 DeepLabv3+ — `TypeError` from a retained batch dimension in the argmax'd mask, fixed with `.squeeze(0)`; Q18 CLIP — silently fell to the scaffold's `acc_clip = 0.65` stub because `openai-clip` wasn't installed (masked `ImportError`), fixed by adding an install cell; corrected result is the real 92.0% above, not the stub value.
- **Not yet confirmed:** Classroom submission status/date, grading score. Repo/notebook content is source-verified; submission tracking is not.

---

## 2.5 Raw Classroom Grade Table *(new, added v4 — July 10, 2026, source: Google Classroom "Your work" screenshot, chronological/reverse order as shown)*

**Provenance:** This table reflects the Classroom gradebook directly — smaller-grained quizzes and problem sets, several of which sit *underneath* the larger numbered weekly projects already tracked in §2 above. None of these entries previously existed in any extract version or the master profile; they are wholly new as of this session, confirmed as fact by Aaradhya. Where a Classroom item name doesn't obviously map to a §2 project name (e.g. "W4: Linear Model Assignment" vs. the tracked "Week 4 — Telco Customer Churn & CLV ML Pipeline"), that's flagged rather than silently merged — these may be distinct graded sub-items within the same week rather than the same deliverable under a different name.

| Item | Due | Type | Score / Status |
| --- | --- | --- | --- |
| Wk1: Data Wrangling Problem | 4 May, 23:59 | Assignments | **100/100** |
| Data Wrangling (Quiz) | 4 May | Quiz | Handed in |
| Wk2 Problem Set: Software Development Concepts | 19 May | Assignments | **75/100** |
| Agentic Software Development Quiz | 10 May | Quiz | Handed in |
| Week3_Problem_Set_GenAI | 20 May | Assignments | **100/100** |
| Gen AI Quiz Assignment | 18 May, 23:59 | Quiz | **31/34** |
| Linear Model Quiz Assignment | 28 May | Quiz | **23/25** |
| W4: Linear Model Assignment | 28 May | Assignments | **88/100** |
| Quiz | 31 May, 09:44 | Quiz | Handed in — **done late** |
| Assignment | 31 May, 09:44 | Assignments | Handed in |
| Probabilistic Models Quiz | 5 Jun, 22:00 | Quiz | Handed in |

**Flags, not resolved:**

- **"W4: Linear Model Assignment" (88/100) and "Linear Model Quiz Assignment" (23/25), both due 28 May** — same due date as the tracked §2 Week 4 project (Telco Churn & CLV Pipeline), but "Linear Model" doesn't match that project's content. Likely a separate, smaller Week 4 graded item (e.g. a foundational linear-regression exercise preceding the full churn/CLV pipeline) rather than the same deliverable — **not confirmed**, flagged for clarification rather than assumed.
- **Two unlabeled rows ("Quiz" and "Assignment," both due 31 May, 09:44)** — generic Classroom names, no week/topic identifiable from the screenshot alone. "Quiz" marked **done late**. Not mapped to any tracked week.
- **Rows above "Probabilistic Models Quiz" in the screenshot were cut off** (partially visible header text "Due 5 Jun, 22:00 • Assignments" with no title) — table starts from the first fully-visible row; anything above the Wk6 boundary in Classroom's list is not captured here.
- **No score column exists for "Handed in"-only rows** — Classroom either hasn't graded them yet or they're pass/fail-style items; not assumed to be perfect scores.

---

## 3. CV-Ready Summary (verbatim block, as maintained)

**Fuse AI Fellow — Fusemachines AI Fellowship 2026 (Active) | 2026 – Present**
*Fusemachines*

- Admission: Passed entrance examination (March 2026) covering linear algebra, calculus, probability, Python, and ML.
- REST API: Built a containerized customer REST API: FastAPI + PostgreSQL + Docker (4-layer architecture, asyncio concurrency).
- Text-to-SQL agent: Developed a five-stage agentic pipeline (Planner → Generator → Validator → Executor → Summarizer) achieving 100% execution success and 100% accuracy on a 50-question benchmark.
- Churn & CLV modeling: End-to-end pipeline with Logistic Regression / Ridge / SGD classifiers; Stratified 5-fold CV ROC-AUC 0.841 ± 0.005; threshold-tuned for top-200 high-risk segment; Papermill automation.
- Tree-based ensemble: Random Forest + XGBoost with ImbPipeline/SMOTE (zero leakage), SHAP explainability, GridSearch tuning, and Joblib serialization.
- Probabilistic models: Bayesian estimation (MLE/MAP/full Bayes), Dirichlet-multinomial inference, Gaussian process regression, probabilistic graphical models, and Bayesian logistic regression via PyMC/ArviZ/pgmpy.
- Customer segmentation: K-Means, Hierarchical (Ward/Complete/Average/Single dendrograms), and DBSCAN on UCI Online Retail II (~500K transactions); RFM + category-ratio feature engineering; Silhouette/Davies-Bouldin/Calinski-Harabasz validation; business narrative with executive summary.
- Forecasting: Benchmarked 9 classical-to-modern forecasters (SARIMA, Holt-Winters, Prophet, LightGBM, LSTM, XGBoost) on monthly S&P 500 data; built a 4-model ensemble beating all single models (MASE 2.44), confirmed via Diebold-Mariano significance test (p = 0.0092).

*Note: CV label still reads "(Active) | 2026 – Present" — accurate while Wk < 24/Oct 18, 2026; update to a closed date range once the fellowship formally ends.*

---

## 4. Project Ranking (fellowship entries only, from master v7 table)

| Rank | Item | Score | Status |
| --- | --- | --- | --- |
| 2 | Wk5 — Telco Tree-Based Ensemble | 9.0 | Complete |
| 3 | Wk3 — Text-to-SQL Pipeline | 8.7 | Complete |
| 4 | Wk4 — Telco Churn & CLV Pipeline | 8.5 | Complete |
| 5 | Wk6 — Probabilistic Models | 8.2 | Complete — portfolio live |
| 11 | Wk7 — Clustering | 8.0 | Complete — portfolio live (v113) |
| 12 | Wk8 — Forecasting | 8.1 | Complete — portfolio **pending** |
| — | Wk9 — NEU Steel Defect CNN | — | Submitted July 9, 2026; build metrics source-verified (v5); Classroom score not yet posted |
| — | Wk10 — Image Processing / FreshTrack CV | — | Repo-verified July 21, 2026 (v6); no rating assigned, no CV bullet drafted, submission/grading status not yet confirmed |
| — | Wk11 — Vision Transformers | — | Repo-verified July 21, 2026 (v6); no rating assigned, no CV bullet drafted, submission/grading status not yet confirmed |
| 14 | Fellowship Prep Toolkit | 6.5 | Complete |

---

## 5. Dev Standards Gate — Applies to All Fellowship Repos

### 12-Factor Pre-Commit Checklist (§16 in master)

Run before every final `git commit` on any `fuseAiF_*` repo (also applies to Nexus).

| # | Factor | Check |
| --- | --- | --- |
| 1 | Codebase | One repo/project, no stray local branches, `git status` clean except staged. |
| 2 | Dependencies | `requirements.txt`/`pyproject.toml` pinned and current; verify via clean-venv install. |
| 3 | Config | No hardcoded secrets/keys/paths; `.env` gitignored, `.env.example` committed. |
| 4 | Backing services | DB/API/storage paths via env vars, swappable without code change. |
| 5 | Build/Release/Run | Dockerfile separates install from runtime; build artifacts gitignored. |
| 6 | Processes | App stateless between requests; no unsafe module-level mutable state. |
| 7 | Port binding | Port from env var, not hardcoded. |
| 8 | Concurrency | No shared mutable state across `asyncio.gather`/Papermill parallel runs. |
| 9 | Disposability | Fast cold start (<5s), graceful SIGTERM shutdown, no orphaned connections. |
| 10 | Dev/prod parity | `docker-compose.yml` mirrors prod; Python version pinned. |
| 11 | Logs | No stray `print()`; `logging` module, stdout, level via env var. |
| 12 | Admin processes | Migrations/seed/fix scripts standalone under `scripts/`, documented, never in app startup. |

**Quick pre-commit sequence:**

```bash
git diff --cached | grep -iE "(api_key|password|secret|token)" && echo "⚠ SECRET DETECTED" || echo "✅ No secrets"
git diff --cached --name-only | grep "\.env$" && echo "⚠ .env STAGED — remove it" || echo "✅ .env clean"
pip freeze > /tmp/current_reqs.txt && diff requirements.txt /tmp/current_reqs.txt | head -20
pytest -q 2>/dev/null || echo "(no tests yet — add at least one smoke test)"
git status && git diff --stat --cached
```

**Per-repo compliance status:**

| Repo | Factor 2 (deps) | Factor 3 (config) | Factor 11 (logs) | Notes |
| --- | --- | --- | --- | --- |
| `fuseAiF_wk3_text2sql` | ✅ | ✅ | ✅ | Docker + .env pattern established |
| `fuseAiF_wk5_telco_churn_ensembles` | ✅ | N/A | ✅ | No secrets; notebook-based |
| `fuseAiF_wk7_customer_segmentation` | ✅ | N/A | ✅ | `.xlsx` gitignored |
| Future fellowship repos | — | — | — | Start from this checklist |

### Instructor Feedback Log

| Week | Feedback | Status |
| --- | --- | --- |
| Wk 2/3/4 (unconfirmed exact week) | Declutter into subfolders; separate `APIRouter` per domain instead of monolithic single-file API. | ⏳ Not yet retroactively applied — apply to next API-based project. |

---

## 6. Fellowship Priority Trigger — Session Protocol (for future task planning)

**Activates on any of:** repo/filename matching `fuseAiF_*`; mention of "fellowship"/"Fusemachines"/"fuse week"/a week number in that context; a `PATCH_fuse*.md` upload; secondary triggers (CV update, portfolio HTML update, LinkedIn update).

**Order of operations when triggered:**

1. Compute current Fuse week: `floor((today − May 4 2026) / 7) + 1`, capped at 24.
2. Identify which week's repo the session concerns (filename/message).
3. Check for an uploaded `PATCH_*.md` — if present, treat as primary source of truth for that week; run patch-merge mode (read patch meta → apply facts to Projects/Fellowship history → flag conflicts → produce changelog entry).
4. If no patch file: standard session mode — offer to generate a patch summary at session end; apply the 12-Factor checklist gate before any `git commit` advice; track completion against the week's assignment scope.
5. End-of-session: summarize any new repo/notebook/deliverable in patch-ready format (what was done/built/learned, mistakes, open items) for later `PATCH_*.md` generation.

**Patch file naming:** `PATCH_fuseWkN_[topic]_YYYYMMDD.md` (e.g. `PATCH_fuseWk8_nlp_20260626.md`). Always include: source repo, period, generated-by, sections affected, what was done/built/learned, mistakes/corrections, open items, evidence pointers (commit hashes, notebook cells, key metrics).

---

## 7. Open Items / Pending Actions (fellowship-specific)

- **Portfolio trigger — Week 8 Forecasting:** not yet added to `projects.html`. Pending.
- **Portfolio trigger — Week 10/11:** not yet added to `projects.html`. Pending (new, v6).
- **Instructor feedback (APIRouter refactor):** not yet retroactively applied to any repo.
- **Nexus repo Factor 3/11 compliance:** `.env.example` needs check; `print()` statements need replacing with `logging` — flagged before next commit (Nexus, not a fellowship repo itself, but governed by the same checklist).
- **Project selection (post-Wk8) — RESOLVED July 10, 2026, SUPERSEDED July 21, 2026 (v7):** ~~Capstone topic chosen: **Ward office project, team-based**~~. Confirmed capstone: **Vision Fairness & Bias Audit** — diagnostic tool for deployed vision classifiers, multi-demographic test matrix, statistical-disparity flags, compliance report (AIF360, Fairlearn, FairFace, UTKFace). Two-person team with **Tisha Manandhar** (github.com/tiixsha) — full roster now closed at 2. In Progress, phase 1 of 3 (Feasibility & Scope) done. **Domain-fit resolved by inspection:** capstone is CV, directly continuous with Wk10/Wk11 — satisfies §8's "pick a topic where something clicked" directive on its face.
- **CV status label:** still reads "(Active) | 2026 – Present" — will need a closed date range after Oct 18, 2026.
- **Wk9 grading/metric verification:** submission and all build-level accuracy/hyperparameter figures are source-verified (Classroom screenshot + executed notebook, v5). Still open: exact Classroom score, not yet posted.
- **Wk10/Wk11 grading/submission verification (new, v6):** repo/notebook content source-verified directly from cloned repos. **Not verified:** Classroom submission status, due dates, "Handed in" confirmation, or grading score for either week — no Classroom screenshot was provided this session, unlike Wk9's v3/v4 verification path. Rating (x/10) also not assigned for either week — no rating was given by Aaradhya, unlike Wk3–Wk9's tracked pattern.
- **Capstone domain-fit — RESOLVED v7:** see project-selection item above; no longer open.

---

## 8. Known Constraint Relevant to Future Fellowship Planning

**Fellowship learning gap** (last updated June 27, 2026): Tasks are submitted on time, no online class skipped — but concepts are mostly skimmed rather than deeply internalized (fatigue, or material not clicking in a single pass). Work goes in; understanding doesn't always fully land. Risk: if the final/capstone project lands in a domain only skimmed, the gap becomes visible.

**Directive carried in master profile:** pick a final project topic where something actually clicked during the weekly work, so the project forces the consolidation the weekly tasks didn't.
