# Fusemachines AI Fellowship 2026: Final Examination Study Blueprint

Reference supplement: [Classroom gap coverage](../CLASSROOM_GAP_COVERAGE.md) maps missing topics to inspected instructor-posted materials and records unresolved details.

This document represents the unofficial synthesized revision notes, not independently verified against instructor answers across all five core modules of the Fusemachines AI Fellowship 2026 (Weeks 1 through 18 and Week 25). It bridges both direct session teachings and external mandatory reading links (Stanford CME295, Colah, Shree Nayar, ISLR, Christoph Molnar, NIST AI RMF, EU AI Act, and OWASP).

---

## Module 1: Systems, Data Engineering & Generative Workflows (Weeks 1 - 3)

### Week 1: Data Wrangling & SQL Foundations
- **Tidy Data Principles**: Hadley Wickham definition: Each variable forms a column, each observation forms a row, and each type of observational unit forms a table.
- **Long vs. Wide Format**: Long format (`melt`) is preferred for relational modeling, Seaborn plotting, and tidy analysis; Wide format (`pivot`, `pivot_table`) is preferred for tabular matrix computations and human reporting.
- **Data Integrity vs. Data Fit**:
  - *Data Integrity*: Structural and syntactic correctness (no corrupt types, valid foreign keys, non-null primary keys, adherence to domain constraints).
  - *Data Fit*: Semantic appropriateness for the target business/ML question (e.g. population representativeness, absence of survivor bias).
- **Deductive Imputation**: Filling missing values through deterministic, domain-rule deductions from other observed columns (e.g. calculating `TotalCharges = MonthlyCharges * tenure` when `TotalCharges` is blank) rather than blind statistical mean/median imputation.
- **SQL Aggregations & Joins**: `LEFT JOIN` vs. `INNER JOIN` preservation of cohort sizes; `CASE WHEN` conditional transformations; Window functions (`ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`) for deduplication.

### Week 2: Production Software Development, FastAPI & Concurrency
- **Relational Integrity**: 3rd Normal Form (3NF), declarative SQLAlchemy ORM models, foreign key cascading constraints (`ON DELETE CASCADE` vs. `SET NULL`).
- **Pydantic Validation**: Strict runtime schema enforcement (`BaseModel`), data coercion, error formatting, separation of Request vs. Response schemas.
- **Async Concurrency**: Non-blocking I/O via `asyncio.gather(*tasks)` across multiple database queries. Crucial: CPU-bound tasks must not block the event loop (delegate to `asyncio.to_thread` or process pools).
- **Docker Compose**: Containerized multi-service orchestration (PostgreSQL container + FastAPI application container + volume persistence).

### Week 3: Agentic Text-to-SQL & Tool Use
- **Anthropic Tool Use**: Defining JSON schemas with parameter types, descriptions, and required fields. Model emits structured tool call; system executes SQL and passes results back in tool role.
- **Text-to-SQL Architecture**: Schema pruning (providing only relevant tables/columns to prevent context window explosion), few-shot domain examples, SQL dialect prompting (PostgreSQL vs. SQLite syntax), query validation/sanitization (`EXPLAIN` plan pre-execution gate to block catastrophic table scans and `DROP`/`UPDATE` injections).
- **Evaluation**: Execution Accuracy (does the query return the exact same result set as gold standard?) vs. Exact String Match (misleading due to alias and whitespace differences).

---

## Module 2: Statistical Machine Learning & Tabular Systems (Weeks 4 - 8)

### Week 4: Statistical ML & Linear Models
- **Problem Formulation**: Formal tuple $(X, y, \mathcal{L}, \mathcal{M})$ where $\mathcal{L}$ is the empirical loss function and $\mathcal{M}$ is the evaluation metric.
- **Classification vs. Regression Losses**:
  - *Linear Regression*: Mean Squared Error (MSE / $L_2$) vs. Mean Absolute Error (MAE / $L_1$). Huber loss balances $L_2$ for small residuals and $L_1$ for large residuals (robust to outliers).
  - *Logistic Regression*: Binary Cross-Entropy / Log Loss $-\frac{1}{N}\sum [y \ln p + (1-y)\ln(1-p)]$. Driven by Maximum Likelihood Estimation (MLE).
- **Regularization**:
  - *Ridge ($L_2$)*: Penalty $\lambda \sum w_j^2$. Shrinks weights smoothly toward zero; closed-form analytical solution $(X^T X + \lambda I)^{-1} X^T y$. Handles collinearity.
  - *Lasso ($L_1$)*: Penalty $\lambda \sum |w_j|$. Shrinks weights to exact zero at diamond corners, performing automated feature selection.
  - *Elastic Net*: Combines $L_1$ and $L_2$ ($\alpha L_1 + (1-\alpha) L_2$). Retains grouped feature selection on correlated predictors.
- **Class Imbalance & Evaluation Metrics**:
  - *Accuracy Paradox*: On 95:5 imbalanced data, predicting majority class yields 95% accuracy with 0% minority recall.
  - *Precision vs. Recall*: Precision = $\frac{TP}{TP+FP}$ (cost of false alarms); Recall = $\frac{TP}{TP+FN}$ (cost of missed churn/defects).
  - *ROC-AUC vs. PR-AUC*: ROC-AUC evaluates $TPR$ vs. $FPR$; heavily distorted by huge true negative counts in severe imbalance. PR-AUC evaluates Precision vs. Recall directly and is far more trustworthy for imbalanced problems.
- **Data Leakage & Production Validation**:
  - Fitting transformers/scalers on the whole dataset before splitting leaks test distribution into training. Scalers must be fit strictly on training splits.
  - Target leakage: Including features computed downstream of the target event (e.g. `CustomerSupportCallsAfterCancellation`).

### Week 5: Tree Models & Ensemble Learning
- **Decision Trees**: Splitting criteria: Gini Impurity $1 - \sum p_i^2$ vs. Shannon Entropy $-\sum p_i \log_2 p_i$. High variance, low bias, hypersensitive to noise.
- **Bagging (Bootstrap Aggregation)**: Parallel independent models trained on bootstrap samples (with replacement). Averaging reduces variance without increasing bias. Random Forest adds random feature subset selection ($\sqrt{p}$ for classification, $p/3$ for regression) at each split to de-correlate trees.
- **Boosting**: Sequential additive models where each tree fits the residual errors/negative gradients of preceding trees:
  - *AdaBoost*: Reweights misclassified observations.
  - *Gradient Boosting*: Fits regression trees directly to pseudo-residuals $-\left[\frac{\partial L(y, f(x))}{\partial f(x)}\right]$.
  - *XGBoost*: 2nd-order Taylor expansion (gradients $g_i$ and Hessians $h_i$), split gain formula with tree complexity penalty $\gamma T + \frac{1}{2}\lambda \sum w_j^2$.
  - *LightGBM*: Histogram-based binning, Gradient-based One-Side Sampling (GOSS), Exclusive Feature Bundling (EFB), leaf-wise (best-first) growth.
  - *CatBoost*: Ordered boosting to prevent target leakage on categorical variables, symmetric (oblivious) trees for low-latency inference.
- **Model Interpretability (SHAP & Molnar)**:
  - *Shapley Values*: Cooperative game theory solution satisfying Efficiency, Symmetry, Dummy player, and Additivity axioms.
  - *Local vs. Global SHAP*: Local waterfall plot shows individual feature pushes from base value $E[f(X)]$ to prediction $f(x)$. Global beeswarm plot displays feature distribution effects across whole dataset.

### Week 6: Probabilistic Models & Bayesian ML
- **Naive Bayes**: Conditional independence assumption $P(X|y) = \prod P(x_i|y)$. Gaussian NB (continuous features), Multinomial NB (word counts), Bernoulli NB (binary indicators).
- **Laplace Smoothing**: Adding pseudocount $\alpha=1$ to prevent zero-frequency probabilities from wiping out product terms: $P(w_i|c) = \frac{N_{ic} + \alpha}{N_c + \alpha |V|}$.
- **Probabilistic Calibration**: Brier Score $\frac{1}{N}\sum (p_i - y_i)^2$. Calibration curves (reliability diagrams). Platt scaling (logistic calibration) vs. Isotonic regression (non-parametric monotonic calibration).
- **MCMC & Bayesian Inference**: Prior $\times$ Likelihood $\propto$ Posterior. PyMC No-U-Turn Sampler (NUTS). Diagnostics: Gelman-Rubin $\hat{R} < 1.05$ (convergence), Effective Sample Size (ESS > 400), Highest Density Interval (HDI 94%).

### Week 7: Unsupervised Clustering & Segmentation
- **Algorithms**:
  - *K-Means*: Minimizes Within-Cluster Sum of Squares (WCSS / Inertia). Sensitive to scaling and outliers; spherical cluster assumption.
  - *K-Means++*: Distributes initial centroids proportional to squared distance $D(x)^2$ from closest existing centroid; bounds expected error to $O(\log k)$.
  - *K-Medoids (PAM)*: Centroids are actual data exemplars; minimizes Manhattan/arbitrary distances; robust to severe outliers.
  - *Hierarchical / Agglomerative*: Bottom-up tree construction using linkage criteria (Ward minimizes variance; Complete linkage prevents chaining; Single linkage finds arbitrary shapes but suffers from chaining). Cut dendrogram at maximum vertical distance without crossing horizontal lines.
  - *DBSCAN*: Density-based. Core points ($\ge \text{min\_samples}$ in $\varepsilon$-ball), Border points, Noise points (label -1). Finds non-convex shapes without specifying $k$. $\varepsilon$ chosen at the elbow of the sorted $k$-nearest neighbor distance plot.
- **Cluster Validation**:
  - *Silhouette Coefficient*: $s = \frac{b - a}{\max(a, b)} \in [-1, 1]$. Higher is better.
  - *Davies-Bouldin Index*: Ratio of within-cluster scatter to separation. Lower is better.
  - *Calinski-Harabasz Index*: Variance ratio criterion (between-cluster dispersion / within-cluster dispersion). Higher is better.

### Week 8: Time-Series Forecasting
- **Stationarity**: Constant mean, constant variance, autocovariance dependent only on lag $k$.
  - *ADF Test*: Null hypothesis $H_0$: unit root is present (non-stationary). Rejecting $H_0$ ($p < 0.05$) implies stationarity.
  - *KPSS Test*: Null hypothesis $H_0$: series is stationary. Rejecting $H_0$ implies non-stationarity.
- **Decomposition**: STL (Seasonal and Trend decomposition using Loess). Additive $Y_t = T_t + S_t + R_t$ (constant seasonal swing) vs. Multiplicative $Y_t = T_t \times S_t \times R_t$ (seasonal amplitude scales with level).
- **ARIMA / SARIMAX**:
  - $p$: Autoregressive order (inspected via PACF cut-off).
  - $d$: Differencing order for trend stationarity.
  - $q$: Moving Average order (inspected via ACF cut-off).
  - Seasonal $(P, D, Q)_s$: Seasonality at period $s$. Exogenous variables ($X$) integrated via regression error term.
- **Validation & Metrics**: Walk-forward cross-validation (rolling window / expanding window); never standard k-fold. MASE (Mean Absolute Scaled Error) $< 1$ indicates model outperforms a naive seasonal persistence baseline.

---

## Module 3: Deep Learning, Computer Vision & Sequence Modeling (Weeks 9 - 13)

### Week 9: Neural Network Foundations & PyTorch Mechanics
- **Computational Graphs & Backpropagation (Colah)**: Forward pass computes values and caches activations; backward pass applies the Chain Rule $\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y} \frac{\partial y}{\partial z} \frac{\partial z}{\partial w}$. Repeated multiplications of values $< 1$ causes vanishing gradients; values $> 1$ causes exploding gradients.
- **Activation Functions**:
  - *Sigmoid*: $\sigma(z) = \frac{1}{1 + e^{-z}}$. Derivative $\sigma'(z) = \sigma(z)(1-\sigma(z))$ maxes out at $0.25$, causing rapid vanishing gradients in deep networks. Non-zero centered.
  - *ReLU*: $\max(0, z)$. Constant gradient 1 for $z > 0$; mitigates vanishing gradients. Vulnerable to "Dying ReLU" when weights push outputs permanently negative.
  - *GELU / LeakyReLU*: Smooth non-zero gradients in negative regime.
- **Optimizers & Memory States**:
  - *SGD*: $w \leftarrow w - \eta \nabla L$. Memory: 0 auxiliary states per parameter.
  - *SGD with Momentum*: Adds velocity vector $v_t = \beta v_{t-1} + \nabla L$. Memory: 1 state per param ($4\text{ bytes/param}$ in FP32).
  - *Adam*: Tracks 1st moment $m_t$ (mean) and 2nd uncentered moment $v_t$ (variance). Memory: 2 states per param ($8\text{ bytes/param}$ in FP32).
- **Regularization & Normalization**:
  - *Batch Normalization*: Normalizes across mini-batch dimension $\frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} \gamma + \beta$. Smooths optimization landscape; behaves differently in `train()` (batch statistics) vs. `eval()` (running exponential moving average).
  - *Dropout*: In `train()`, zeroes activations with probability $p$ and scales remaining by $\frac{1}{1-p}$ (inverted dropout). In `eval()`, acts as identity.

### Week 10: Classical Image Processing & OpenCV (Shree Nayar / MIT 6.003)
- **Linear Shift-Invariant (LSI) Systems**: Convolution $f * g$ requires flipping the kernel by $180^\circ$ ($g(-x, -y)$) to preserve associativity and shift invariance. Cross-correlation slides the kernel without flipping.
- **Color Spaces**: RGB is hypersensitive to illumination changes. HSV separates Chromaticity (Hue: 0-180 in OpenCV, Saturation: 0-255) from Intensity (Value: 0-255). Red wraps around the Hue axis (0–10 and 170–180), requiring two masks combined with `cv2.bitwise_or`.
- **Filtering & Histograms**:
  - *Gaussian Blur*: Linear weighted smoothing; removes Gaussian noise but blurs edges.
  - *Median Filter*: Non-linear; replaces pixel with neighborhood median. SOTA for salt-and-pepper noise.
  - *Bilateral Filter*: Combines spatial Gaussian distance with range radiometric Gaussian difference; smooths textures while preserving sharp step edges.
  - *CLAHE (Contrast Limited Adaptive Histogram Equalization)*: Local tile equalization with clip limit to prevent noise over-amplification in uniform regions.
- **Morphology**:
  - *Erosion*: $\min$ in structuring element; shrinks bright regions, strips noise blobs.
  - *Dilation*: $\max$ in structuring element; expands bright regions, closes gaps.
  - *Opening*: Erosion followed by Dilation. Eliminates small background noise blobs.
  - *Closing*: Dilation followed by Erosion. Fills small holes within objects.
  - *Morphological Gradient*: Dilation $-$ Erosion. Extracts exact boundary outline.
  - *Top Hat*: Original $-$ Opening (isolates elements brighter than surroundings).
  - *Black Hat*: Closing $-$ Original (isolates elements darker than surroundings).
- **Feature Detection**:
  - *Canny 5-Stage Pipeline*: (1) 5x5 Gaussian filter, (2) Sobel gradients $G = \sqrt{G_x^2 + G_y^2}$ and $\theta = \arctan(G_y / G_x)$, (3) Non-Maximum Suppression (thinning to 1-pixel ridges along gradient direction), (4) Double Thresholding (high/low thresholds), (5) Hysteresis edge tracking (weak edges retained only if connected to strong edges).
  - *Harris Corner Detector*: Second moment matrix $M = \sum w(x,y) \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix}$. Response $R = \det(M) - k\,\text{Tr}(M)^2 = \lambda_1 \lambda_2 - k(\lambda_1 + \lambda_2)^2$. Corner: $\lambda_1, \lambda_2$ both large ($R > 0$); Edge: one large, one small ($R < 0$); Flat: both small ($|R| \approx 0$).
  - *Hough Circles*: Dual accumulator voting in parameter space $(x-a)^2 + (y-b)^2 = r^2$.

### Week 11: Modern Computer Vision (ResNet, ViT, YOLO, CLIP)
- **ResNet**: Residual skip connection $y = \mathcal{F}(x, \{W_i\}) + x$. Enables gradients to flow uninterrupted via identity mapping $\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y}(1 + \frac{\partial \mathcal{F}}{\partial x})$, destroying vanishing gradients in deep architectures.
- **Vision Transformers (ViT)**: Flattens image into non-overlapping patches of size $P \times P$, projects linearly to dimension $D$, appends learnable `[CLS]` token, adds 1D learnable position embeddings, passes through Standard Transformer Encoder. Global receptive field from layer 1 (unlike CNNs which build local-to-global hierarchy).
- **Object Detection (YOLOv8)**: Anchor-free detection head, Task-Aligned Assigner, decoupled classification and bounding-box regression heads, loss combination of Complete IoU (CIoU) and Distribution Focal Loss (DFL).
- **CLIP (Contrastive Language-Image Pre-Training)**: Dual image and text encoders. Symmetric InfoNCE loss across $N \times N$ batch pairs: maximizes cosine similarity of $N$ positive diagonal pairs while minimizing $N^2 - N$ off-diagonal negative pairs. Enables zero-shot classification via text prompts.
- **Interpretability**: Grad-CAM calculates gradients of target class score $y^c$ with respect to feature activation map $A^k$, computing importance weights $\alpha_k^c = \frac{1}{Z}\sum_i \sum_j \frac{\partial y^c}{\partial A_{i,j}^k}$ followed by $\text{ReLU}(\sum \alpha_k^c A^k)$.

### Weeks 12 - 13: Classical NLP, Embeddings & Sequence Learning
- **Information Retrieval & Embeddings**:
  - *BM25*: Upgrades TF-IDF with non-linear term frequency saturation parameter $k_1 \approx 1.2\text{--}2.0$ and document length normalization parameter $b \approx 0.75$.
  - *Word2Vec (Skip-Gram Negative Sampling)*: Predicts context words given target word; negative sampling approximates denominator using noise distribution $P_n(w) \propto U(w)^{0.75}$.
  - *FastText*: Represents words as bags of character $n$-grams; solves out-of-vocabulary (OOV) tokens and morphology.
- **Linear-Chain Conditional Random Fields (CRF)**: Global sequence normalization $P(y|x) = \frac{1}{Z(x)} \exp\left(\sum [W \cdot f(y_t, x) + T(y_{t-1}, y_t)]\right)$. Unlike token-level classifiers, transition matrix $T$ guarantees structural validity (e.g. forbids `I-PER` following `B-LOC`). Solved via Viterbi decoding.
- **Recurrent Architectures**:
  - *Vanilla RNN*: BPTT (Backpropagation Through Time). Repeated multiplication by transition matrix $W_{hh}^T$ causes spectral radius $\rho(W_{hh}) > 1 \implies$ exploding gradients, $\rho(W_{hh}) < 1 \implies$ vanishing gradients.
  - *LSTM*: Solves vanishing gradients via additive Constant Error Carousel (CEC). Forget gate $f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)$, Input gate $i_t$, Candidate $\tilde{C}_t$, Cell state update $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$, Output gate $o_t$, Hidden state $h_t = o_t \odot \tanh(C_t)$.
  - *Attention Mechanisms*: Bahdanau (additive: $v_a^T \tanh(W_a s_{t-1} + U_a h_i)$) vs. Luong (multiplicative: $s_t^T W_a h_i$).

---

## Module 4: Transformers, LLMs & Production AI Engineering (Weeks 14 - 15, Week 25)

### Week 14: Transformers & Foundational LLMs (Stanford CME295 / Jay Alammar / HF)
- **Scaled Dot-Product Attention**: $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$. Scaling factor $\frac{1}{\sqrt{d_k}}$ prevents dot products from growing excessively large in high dimensions, which would push softmax into regions with vanishing gradients.
- **Architectural Upgrades**:
  - *Pre-LN vs. Post-LN*: Post-LN (original transformer) places LayerNorm on the residual path, causing gradient instability that requires aggressive learning rate warmup. Pre-LN applies LayerNorm before sub-layers inside the residual stream, enabling stable zero-warmup training.
  - *Rotary Position Embedding (RoPE)*: Encodes relative position by rotating query and key vectors in complex 2D planes using orthogonal rotation matrices: $\langle R_{\Theta, m} q, R_{\Theta, n} k \rangle = g(q, k, m-n)$. Preserves relative distance decay without static additive vectors.
  - *KV-Cache & Memory*: During autoregressive decoding, keys and values of previous tokens are cached to avoid $O(N^2)$ recalculation. Memory per token: $2 \times 2 \times n_{\text{layers}} \times n_{\text{heads}} \times d_{\text{head}} \times \text{bytes\_per\_param}$.
  - *Multi-Query (MQA) & Grouped-Query Attention (GQA)*: MQA shares a single key-value head across all query heads (shrinking KV-cache by $n_{\text{heads}}$). GQA groups query heads (e.g. 8 groups sharing 1 KV pair), balancing latency and representation capacity.
- **Scaling Laws & Post-Training**:
  - *Chinchilla Scaling Laws (Hoffmann et al.)*: For compute-optimal training, model parameters and training tokens should scale equally: $\approx 20\text{ tokens per parameter}$.
  - *LoRA (Low-Rank Adaptation)*: Freezes pre-trained weight $W_0 \in \mathbb{R}^{d \times k}$ and injects trainable rank decomposition matrices $W = W_0 + \frac{\alpha}{r} BA$ where $B \in \mathbb{R}^{d \times r}$ is initialized to zero and $A \in \mathbb{R}^{r \times k}$ is Gaussian initialized. Initialized update $\Delta W = 0$ prevents perturbation at step 0. QLoRA quantizes $W_0$ to 4-bit NormalFloat (NF4) with double quantization.
  - *Alignment*: RLHF (PPO optimizes reward model with KL divergence penalty against reference model) vs. DPO (Direct Preference Optimization derives analytical closed-form loss directly from Bradley-Terry preference probability, eliminating separate reward model and reinforcement learning training loop).

### Week 15 & Week 25: Applied AI, LLM Serving & Production RAG
- **LLM Serving Mechanics (vLLM)**:
  - *Memory Waste*: Traditional systems suffer 60–80% memory waste due to internal/external fragmentation and reservation for worst-case maximum sequence lengths.
  - *PagedAttention*: Allocates KV-cache in fixed-size non-contiguous physical memory blocks (similar to virtual memory in operating systems). Enables dynamic sharing of prompt KV blocks during parallel sampling.
  - *Serving Metrics*: TTFT (Time To First Token = prefill latency) vs. ITL (Inter-Token Latency = decode throughput). Speculative decoding verifies draft model tokens in parallel on target model.
- **Production Retrieval-Augmented Generation (RAG)**:
  - *Hybrid Search*: Combines dense semantic vector retrieval (approximate nearest neighbor HNSW/Cosine) with sparse keyword retrieval (BM25).
  - *Reciprocal Rank Fusion (RRF)*: Merges rankings without score calibration: $RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$ where constant $k \approx 60$.
  - *Cross-Encoder Reranking*: Dual-encoder bi-encoders calculate independent vectors for speed; Cross-encoder feeds concatenated $(Q, D)$ through full self-attention to capture deep token-level interactions.
  - *RAG Triad Evaluation (TruLens/RAGAS)*: (1) Context Relevance (is retrieved context free of noise?), (2) Groundedness / Faithfulness (is the answer derived strictly from context?), (3) Answer Relevance (does the response directly address user prompt?).

---

## Module 5: Agentic Systems, MLOps & Trustworthy AI (Weeks 16 - 18)

### Week 16: Agentic AI Architectures & Anthropic Guidelines
- **Core Patterns (Anthropic Building Effective Agents)**:
  - *Prompt Chaining*: Linear workflow decomposing tasks into sequential steps.
  - *Routing*: Classifying inputs to dispatch to specialized models or prompts.
  - *Parallelization*: Sectioning independent sub-tasks (Sectioning) or voting for consensus.
  - *Orchestrator-Workers*: Central orchestrator breaks dynamic task into subtasks and coordinates workers.
  - *Evaluator-Optimizer*: Multi-turn loop where one agent generates and another critiques until stopping criteria are satisfied.
- **Five Structural Multi-Agent Failure Modes**:
  1. *Oscillation*: Two agents endlessly disagree or flip-flop states.
  2. *Deadlock*: Mutual dependency blocking execution progress.
  3. *Cascading Hallucination*: Downstream agent treats unverified hallucinated output as ground truth.
  4. *Echo Chambers*: Agents reinforce biases without external tool grounding.
  5. *Context Starvation*: Inadequate provenance passed between execution steps.
- **Model Context Protocol (MCP)**: Standardized client-server protocol enabling LLMs to discover and execute tools, read resources, and ingest prompt templates across local/remote services without custom point-to-point wrappers.
- **Evaluation**: $pass@k = 1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}$ (probability of at least 1 correct solution in $k$ samples) vs. $pass^k$ (all $k$ steps must succeed for task completion).

### Week 17: Production MLOps, Drift Detection & Deployment
- **Continuous Monitoring & Drift Types**:
  - *Data Drift (Covariate Shift)*: Input feature distribution shifts $P(X) \neq P'(X)$ while conditional relationship $P(y|X)$ remains constant.
  - *Concept Drift*: Relationship between inputs and targets changes $P(y|X) \neq P'(y|X)$.
- **Statistical Drift Tests**:
  - *Kolmogorov-Smirnov (K-S) Test*: Non-parametric test comparing continuous cumulative distributions $D = \sup_x |F_1(x) - F_2(x)|$.
  - *Population Stability Index (PSI)*: $\sum (Actual\% - Expected\%) \times \ln(Actual\% / Expected\%)$. Calibration: $< 0.1$ (no significant change), $0.1\text{--}0.25$ (moderate drift; investigate), $\ge 0.25$ (significant drift; trigger automated retraining).
  - *Wasserstein Distance*: Earth Mover's Distance measuring minimum work to transform one distribution into another.
- **Deployment Strategies**: Canary (route 5-10% of live traffic to new version), Blue-Green (instant cutover between identical environments with zero downtime rollback), Shadow (mirror live production traffic to new model without serving predictions to users).

### Week 18: Responsible & Trustworthy AI, Guardrails & Governance
- **Fairness Metrics & Bias Auditing**:
  - *Demographic Parity*: Selection rate is independent of protected attribute: $P(\hat{Y}=1 | A=a) = P(\hat{Y}=1 | A=b)$. Four-fifths (80%) rule: $\frac{\text{selection rate minority}}{\text{selection rate majority}} \ge 0.80$.
  - *Equalized Odds*: Predictor satisfies equal True Positive Rate and equal False Positive Rate across groups: $P(\hat{Y}=1 | A=a, Y=y) = P(\hat{Y}=1 | A=b, Y=y)$.
  - *Equal Opportunity*: Relaxes Equalized Odds to only require equal True Positive Rate for advantageous outcome ($y=1$).
- **Causal Fairness & Pearl's Ladder of Causation**:
  - Association (Seeing: $P(y|x)$), Intervention (Doing: $P(y|do(x))$), Counterfactuals (Imagining: $P(y_x | x', y')$).
  - Graph structures: Confounders (common cause affecting treatment and outcome; must control for), Mediators (causal path between treatment and outcome; controlling introduces over-controlling bias), Colliders (common effect of two variables; conditioning on a collider opens a spurious non-causal path).
- **Regulatory Frameworks & Invariants**:
  - *NIST AI RMF 1.0*: Core functions: `GOVERN`, `MAP`, `MEASURE`, `MANAGE`.
  - *EU AI Act*: Risk categorization: Unacceptable Risk (banned: social scoring, cognitive manipulation), High Risk (Annex III: employment, credit, biometric, critical infrastructure — requires strict risk management, data governance, conformity assessment), Limited Risk (transparency obligations for chatbots/deepfakes), Minimal Risk.
  - *GDPR Invariants*: Article 15 (Right of access & meaningful explanation of logic), Article 22 (Right not to be subject to solely automated decision making producing legal effects), Article 33 (72-hour breach notification), Article 35 (Data Protection Impact Assessment - DPIA).
- **OWASP Top 10 for LLM Applications**:
  - *LLM01: Prompt Injection*: Direct (jailbreaks) and Indirect (untrusted external data instructing model to ignore system prompt).
  - *LLM02: Sensitive Information Disclosure*: PII leakage via training data extraction or prompt reverberation.
  - *LLM04: Model Denial of Service*: Resource exhaustion via unbounded recursive queries or massive context injection.
  - *LLM06: Excessive Agency*: Granting autonomous models unrestricted destructive permissions (e.g. `rm`, `DROP TABLE`) without human-in-the-loop verification gates.
- **Differential Privacy**: An algorithm $\mathcal{M}$ satisfies $(\varepsilon, \delta)$-differential privacy if for all neighboring datasets $D, D'$ differing by at most one individual: $P(\mathcal{M}(D) \in S) \le e^{\varepsilon} P(\mathcal{M}(D') \in S) + \delta$.
