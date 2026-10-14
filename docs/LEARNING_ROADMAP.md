# FuseAIF2026 Learning Roadmap

The roadmap groups the fellowship weeks into five phases by subject and estimated difficulty. The concepts are study targets drawn from the weekly coursework; difficulty is a planning estimate.

## Phase 1: Data and Backend Foundations

**Difficulty:** Easiest  
**Weeks:** 1–2  
**Gemini NotebookLM:** [AIF 2026 — Week 2: Database and API Architecture](https://notebooklm.google.com/notebook/e5bdc1b4-a017-49c0-8c6a-f890f3f64b7f) (includes Week 1 SQL and Data Lifecycle material)

**Core concepts:**

- Wrangle multi-table data with Pandas and apply the 14-stage Data Lifecycle.
- Query relational data with joins, CTEs, and `RANK()`; configure apps using 12-Factor principles and Docker database initialization through `/docker-entrypoint-initdb.d/`.
- Build four-layer FastAPI services and coordinate concurrent tasks with `asyncio.gather()`.

## Phase 2: Classical and Probabilistic Machine Learning

**Difficulty:** Low to medium  
**Weeks:** 4–8  
**Gemini NotebookLM:** [Weeks 4–5: Supervised Tabular ML](https://notebooklm.google.com/notebook/41209057-a697-4ccc-afdc-a3b949b5d046); [Week 7: Clustering and Market Segmentation](https://notebooklm.google.com/notebook/97b0378d-f283-46cf-b1ba-b85a32e2da25); [Weeks 6 and 8: Probabilistic ML and Time Series Forecasting](https://notebooklm.google.com/notebook/69078013-99a8-4ac0-babb-85bd4c7e0719)

**Core concepts:**

- Analyze empirical risk and class imbalance; use the 27% churn dataset to examine accuracy limits.
- Train leakage-safe tabular models with bagging, boosting, XGBoost, and LightGBM; interpret model behavior with SHAP.
- Compare RFM clustering with K-Means++, dendrograms, and DBSCAN; fit Bayesian models with MLE, MAP, PyMC, and Gaussian processes; evaluate SARIMA forecasts with walk-forward validation and the Diebold–Mariano test.

## Phase 3: Deep Learning, Vision, and NLP

**Difficulty:** Medium to high  
**Weeks:** 9–14  
**Gemini NotebookLM:** [Weeks 9–11: Deep Learning and Computer Vision](https://notebooklm.google.com/notebook/aeac3de5-39c9-4cf9-8a49-a21ccd73ca3b); [Weeks 12–14: NLP, Sequence Learning, and Transformers](https://notebooklm.google.com/notebook/ac9591f2-fc7b-4bf7-ba4d-ba7bd29c911c)

**Core concepts:**

- Build PyTorch training loops with autograd; estimate Adam memory needs (roughly 6–10× model weights, depending on precision, batch size, and activations); apply He and Xavier initialization.
- Use ResNet-50 with Grad-CAM, Faster R-CNN, YOLO, DeepLabv3+, variational autoencoders with ELBO, ViT, and CLIP zero-shot classification.
- Compare TF-IDF and Word2Vec, RNN/LSTM gates, BERT `[CLS]`, and Qwen2.5 LoRA intent routing.

## Phase 4: Agentic Systems and MLOps

**Difficulty:** High  
**Weeks:** 3, 15–17  
**Gemini NotebookLM:** [Week 3: Agentic Text-to-SQL System](https://notebooklm.google.com/notebook/270b157a-3864-4d54-b372-4e4969688545); [Weeks 15–16: Applied AI, RAG, and Multi-Agent Systems](https://notebooklm.google.com/notebook/e370d78e-3453-498d-9509-1d4b5bfc0446); [Week 17: AI Systems and MLOps](https://notebooklm.google.com/notebook/ffdaa426-4497-44aa-92fb-ed57ccfc789e)

**Core concepts:**

- Decompose and self-correct Text-to-SQL; build hybrid retrieval-augmented generation with BM25, dense retrieval, reciprocal-rank fusion, and cross-encoders.
- Run LangGraph multi-agent topologies and engineer context, harness, and agent loops.
- Use vLLM PagedAttention and FP8/INT8 quantization; manage model workflows with `uv`, MLflow, Evidently, and Airflow.

## Phase 5: Responsible and Causal AI

**Difficulty:** Capstone level  
**Weeks:** 18 and 25  
**Gemini NotebookLM:** [Week 25: Responsible and Trustworthy AI](https://notebooklm.google.com/notebook/12a41b10-84d6-46a7-99c4-fbf933af3794)

**Core concepts:**

- Apply the NIST AI Risk Management Framework and EU AI Act; assess explainability fidelity and stability.
- Trace causal DAGs, including confounders, colliders, and mediators.
- Bound prompt-injection impact and keep tamper-evident audit logs.
