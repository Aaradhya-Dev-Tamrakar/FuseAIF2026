# Fuse AI Fellowship 2026 — Week 17 Track B: Agentic AI MLOps

Production MLOps governance applied to the **W15/W16 Autonomous Technical Assistant**: reproducible environment management via `uv`, experiment tracking of versioned prompt iterations driven by execution trace failure diagnoses via `MLflow`, regression testing with LLM-as-a-judge via `Evidently AI`, and nightly automated evaluation gating via `Airflow`.

## Quick Start

```bash
# Clone and set up
git clone https://github.com/AaradhyaDT/fuseAiF_wk17_agentic_mlops.git
cd fuseAiF_wk17_agentic_mlops

# Install dependencies (reproducible clean clone via uv)
uv sync

# Run MLflow prompt iteration evaluation & trace logging
uv run python -m eval.harness_mlflow

# Run Evidently LLM-as-a-judge regression test suite & HTML report
uv run python -m eval.evidently_judge

# Verify test suite & linting
uv run ruff check .
uv run pytest -v

# Launch MLflow UI to inspect runs, traces, and regression metrics
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

---

## a. Environment & Reproducibility (`uv`)

This project migrates the Week 15/16 assistant from unstructured `requirements.txt` to deterministic dependency management using **[uv](https://docs.astral.sh/uv/)** (v0.11.24).

### Problems `uv` Solves Specifically for this Agent System

1. **Heavy Multi-Framework Resolution**: The agent system combines PyTorch (for offline SentenceTransformer embeddings), MLflow 3.16, Evidently 0.7, FastAPI, and Qdrant. Historically, resolving these packages via `pip install` resulted in version conflicts (e.g. `pydantic v1` vs `v2` conflicts with older litestar/evidently packages, or `numpy 2.x` vs `1.x` C-extension ABI breaks). `uv` resolves all 171 transitive dependencies in **1.57 seconds** into a deterministic `uv.lock`.
2. **One-Command Clean Reproduction**: A newly cloned environment requires only:
   ```bash
   uv sync
   ```
   No manual wheel builds, no virtualenv activation scripts required, and no hidden dependencies.
3. **Runtime Python Pinning**: `requires-python = ">=3.12,<3.13"` enforces execution on Python 3.12, ensuring identical typing semantics, async task cancellation behavior, and regex engine mechanics across development and production servers.

---

## b. Experiment Tracking Strategy (`MLflow`)

Unlike traditional predictive modeling where model weights are updated, MLOps for Agentic AI governs **configurations, system prompts, retrieval parameters, and execution behavior**.

### Versioned Prompts Driven by Trace Failure Diagnoses

We conducted experiments across **3 versioned system prompts** stored in `app/agent/prompts/`:

```
agent_v1.md (Baseline) ──[Trace Failure Diagnosis]──> agent_v2.md (Conflict-Aware) ──[Trace Failure Diagnosis]──> agent_v3.md (Optimized)
```

Each iteration was driven by **direct forensic inspection of execution traces**, not speculative prompt edits:

#### 1. Prompt v1 (`agent_v1.md`) — Baseline ReAct Prompt
- **Design**: General ReAct loop instructing the model to verify before answering and cite sources.
- **Trace Failure Diagnosis**: On conflict-resolution queries (e.g. `GR-001` Pro pricing, `GR-007` XML API deprecation), execution traces revealed the agent called `search_knowledge_base`, found `provider_pricing.md`, and called `final_answer` immediately. The agent never cross-checked `release_notes.md` to see if newer version updates superseded the document. On multi-hop queries, it did not utilize scratchpad notes, causing redundant document reads.
- **Trace Artifact**: [`trace_conflict_failure.json`](reports/traces_v1/trace_conflict_failure.json) captures the agent answering with stale $39 pricing without inspecting release notes.

#### 2. Prompt v2 (`agent_v2.md`) — Conflict-Aware Prompt
- **Design**: Added mandatory rule: *"Whenever you retrieve any document that references a version number, price, configuration value, or dated specification, you MUST immediately search for release_notes.md to check for superseding updates."*
- **Trace Failure Diagnosis**: Fixes pricing and deprecation accuracy (completion rises to 80%). However, traces revealed **trajectory inflation** from 3.8 to 5.2 average iterations. The broad query heuristic caused the agent to issue generic searches like `search_knowledge_base("release notes latest version updates")`, matching multiple documents and triggering redundant `read_document` calls on irrelevant pages. Token consumption increased by 35%.
- **Trace Artifact**: [`trace_redundant_search.json`](reports/traces_v2/trace_redundant_search.json) captures 2 wasted iterations reading unrelated architecture docs.

#### 3. Prompt v3 (`agent_v3.md`) — Optimized Precedence & Query Reformulation
- **Design**: Added targeted search heuristics (reformulating queries into specific keyword phrases targeting document titles), mandatory immediate scratchpad logging via `take_note`, an early synthesis gate (>=3 relevant passages with notes recorded), and redundancy prevention.
- **Result**: Trajectory drops to 3.4 iterations (lowest), task completion reaches 90% (highest), and token consumption drops below the v1 baseline.

---

### Side-by-Side Version Comparison Table

| Prompt Version | Task Completion | Tool Correctness | Mean Trajectory | Total Tokens | Cost (USD) | Regression Pass Rate | Status |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **v1 (Baseline)** | 60.0% | 72.0% | 3.8 steps | 14,200 | $0.0071 | 50.0% | Evaluated (Failed Gate) |
| **v2 (Conflict-Aware)** | 80.0% | 85.0% | 5.2 steps | 19,100 | $0.0096 | 90.0% | Evaluated (High Cost) |
| **🏆 v3 (Optimized)** | **90.0%** | **93.0%** | **3.4 steps** | **12,800** | **$0.0064** | **80.0%** | **Promoted to Production** |

### Winning Version Justification & Trade-Off Analysis
**v3 wins decisively on both capability and operational efficiency:**
- **v3 vs v1**: +50% higher task completion (90% vs 60%), +29% tool correctness, -10% token consumption, -10% cost.
- **v3 vs v2**: +12.5% higher completion, -35% lower trajectory length (3.4 vs 5.2), -33% lower token cost ($0.0064 vs $0.0096).
- **Trade-off Analysis**: v2 had a slightly higher regression pass rate on one edge case (90% vs 80%), but incurred a 35% latency and cost penalty. In production systems serving high traffic, v3's 33% cost reduction and 35% latency reduction with 90% overall task completion makes it the justified production candidate.

---

### Structured Trace Schema & MLflow Artifacts

Every test query execution records a structured step-by-step trace saved as MLflow artifacts:
```json
{
  "query_id": "GR-001",
  "query": "What is the current pricing for the Pro tier?",
  "outcome": "SUCCESS",
  "termination_reason": "evidence_sufficient",
  "iterations": 4,
  "steps": [
    {
      "step": 1,
      "tool": "search_knowledge_base",
      "args": { "query": "Pro tier pricing monthly seat cost" },
      "result": "Found provider_pricing.md",
      "reasoning": "v3: Reformulated query with specific terms."
    },
    {
      "step": 2,
      "tool": "take_note",
      "args": { "fact": "provider_pricing.md says Pro = $39/month/seat", "doc_id": "provider_pricing.md" },
      "result": "Note recorded",
      "reasoning": "v3: Logging value to scratchpad before cross-check."
    },
    {
      "step": 3,
      "tool": "search_knowledge_base",
      "args": { "query": "release_notes.md v2.4 pricing update" },
      "result": "Found release_notes.md: Pro price updated to $49",
      "reasoning": "v3: Targeted cross-check with specific doc name + version."
    },
    {
      "step": 4,
      "tool": "final_answer",
      "args": {
        "answer": "The Pro tier is $49/month per seat (updated in v2.4 from $39).",
        "citations": ["release_notes.md", "provider_pricing.md"],
        "confidence": "high"
      },
      "result": "Answer submitted",
      "reasoning": "v3: Scratchpad has both values. Synthesizing with 2 passages — conflict resolved."
    }
  ],
  "root_cause": null
}
```

Logged MLflow artifacts per run:
- Versioned prompt text (`prompts/prompt_<version>.md`)
- Detailed forensic failure diagnosis (`diagnosis/failure_diagnosis_<version>.md`)
- 3 representative JSON traces per version (success, failure, and edge cases)

---

## c. Monitoring & Regression Testing Strategy (`Evidently AI`)

### Golden Reference Set (`eval/golden_references.json`)

A curated benchmark of **10 representative queries** pairing real user intents with gold-standard reference answers:
1. `GR-001`: Pro tier pricing (conflict resolution)
2. `GR-002`: Concurrent connection limits (single-hop)
3. `GR-003`: Authentication recommendations (multi-hop)
4. `GR-004`: Developer team pricing calculation (conflict + computation)
5. `GR-005`: High availability deployment configuration (multi-hop)
6. `GR-006`: Version 2.3 to 2.4 release changes (factual lookup)
7. `GR-007`: XML API deprecation status (deprecation check)
8. `GR-008`: API tier rate limits (factual lookup)
9. `GR-009`: Database upgrade migration procedure (multi-hop)
10. `GR-010`: Observability & Prometheus integration (factual lookup)

### Two-Tier Evaluator Checks

Evidently evaluates each candidate response against the reference set across two automated checks:

1. **Check 1: Reference-based Correctness**
   - Evaluates whether the candidate answer preserves the core factual assertions (exact prices, version numbers, deprecated flags, configuration values) without contradiction.
2. **Check 2: Context Grounding & Hallucination Guard**
   - Verifies that all cited documents belong to the genuine corpus (`release_notes.md`, `provider_pricing.md`, `architecture.md`, `security_guidelines.md`, `api_reference.md`) and that fabricated citations are flagged.

### Promotion Gating & Results

The non-negotiable promotion gate requires `pct_tests_passed >= 80%`:

| Prompt Version | Tests Passed | Pass Rate (`pct_tests_passed`) | Gate Verdict |
|:---:|:---:|:---:|:---:|
| **v1 (Baseline)** | 5 / 10 | 50.0% | ❌ **BLOCKED** (< 80% threshold) |
| **v2 (Conflict-Aware)** | 9 / 10 | 90.0% | ✅ **ELIGIBLE** (≥ 80% threshold) |
| **v3 (Optimized)** | 8 / 10 | 80.0% | ✅ **ELIGIBLE** (≥ 80% threshold) |

HTML regression report is saved to `reports/agent_regression_report.html` and logged to MLflow.

### Judge Sanity-Check Interpretation

- **Alignment with Ground Truth**: Manual inspection confirms that v1 fails primarily on `GR-001` (stale $39 price cited instead of $49), `GR-004` (wrong math resulting from stale price), `GR-006` (inability to synthesize release notes), and `GR-007` (claiming XML API is available when deprecated). The automated judge correctly flags all 4 cases.
- **Judge Discrepancy Analysis**: On `GR-009` (v3), the judge flags a failure because the candidate response omits the 5-10 minute downtime estimate, even though it correctly identifies the migration script `migrate_v23_to_v24.sql`. This demonstrates that the judge enforces strict completeness rather than superficial similarity, serving as a reliable quality gate.

---

## d. Orchestration — Airflow Nightly Regression DAG

### DAG: `agent_regression_eval_dag` (`dags/agent_regression_eval_dag.py`)

```
Schedule: @nightly (00:00 UTC)
Start Date: 2026-10-01

run_agent_regression_suite  ──>  evaluate_regression_gate
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
            alert_regression_degradation      log_promotion_approved
            (if pass rate < 80%)             (if pass rate >= 80%)
```

**Workflow Architecture**:
1. `run_agent_regression_suite`: Executes the full prompt evaluation across golden test cases and runs Evidently checks. Pushes `pct_tests_passed` to XCom.
2. `evaluate_regression_gate`: Branching operator evaluating production criteria (`pct_tests_passed >= 0.80`).
3. `alert_regression_degradation`: If regression is detected, dispatches alerts across Slack (`#agent-alerts`) and PagerDuty, and blocks promotion in MLflow.
4. `log_promotion_approved`: Approves prompt version for production deployment.

---

## Repository Structure

```
fuseAiF_wk17_agentic_mlops/
├── pyproject.toml              # uv configuration + pinned dependencies
├── uv.lock                     # Deterministic lockfile (171 packages)
├── README.md                   # This comprehensive documentation
├── app/
│   ├── config.py               # Settings and environment variables
│   ├── main.py                 # FastAPI application
│   ├── orchestrator.py         # Provider coordination
│   ├── agent/
│   │   ├── loop.py             # ReAct execution loop
│   │   ├── tools.py            # 8 agent tool specifications
│   │   ├── trace.py            # Structured trace and trajectory schema
│   │   ├── verifier.py         # Deterministic citation verifier
│   │   ├── context.py          # Context engineering & tool clearing
│   │   ├── faults.py           # Fault injection engine
│   │   └── prompts/
│   │       ├── agent_v1.md     # Baseline ReAct prompt
│   │       ├── agent_v2.md     # Conflict-aware prompt
│   │       └── agent_v3.md     # Optimized query reformulation prompt
│   └── rag/                    # Vector store, embeddings, and retriever
├── eval/
│   ├── golden_references.json  # 10 curated golden reference query/answer pairs
│   ├── harness_mlflow.py       # MLflow experiment tracking & trace logging
│   └── evidently_judge.py      # Evidently LLM-as-a-judge regression suite
├── dags/
│   └── agent_regression_eval_dag.py  # Airflow nightly evaluation DAG
├── tests/
│   ├── test_agent_mlops.py     # 11 tests: prompts, golden set, judge, DAG
│   ├── test_agent_loop.py      # Loop termination and tool execution tests
│   ├── test_api.py             # FastAPI endpoint tests
│   └── ...                     # Complete W16 test suite (63 total tests)
└── reports/
    ├── prompt_comparison.md    # Side-by-side prompt version metrics
    ├── agent_regression_report.html # Evidently HTML regression report
    ├── traces_v1/              # Representative v1 execution traces
    ├── traces_v2/              # Representative v2 execution traces
    └── traces_v3/              # Representative v3 execution traces
```

---

## Verification Proof

```bash
# Linting: Clean pass (0 errors)
uv run ruff check .

# Test suite: 63/63 tests passing (100%)
uv run pytest -v

# MLflow UI:
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```
