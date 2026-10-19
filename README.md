# FuseAIF2026

This repository archives weekly coursework, notebooks, datasets, and project work from the Fusemachines AI Fellowship 2026.

<!-- sync-status:start -->
**Last synchronized:** 2026-10-19
<!-- sync-status:end -->

## Archive

Course materials are grouped by module and week. Some weeks contain full local projects; others point to a separate project repository.

| Module | Weeks | Focus |
| --- | --- | --- |
| M1 | 1–4 | Data wrangling, databases, APIs, and linear models |
| M2 | 5–8 | Statistical learning, clustering, and forecasting |
| M3 | 9–12 | Deep learning, computer vision, and NLP foundations |
| M4 | 13–16 | Sequence learning, transformers, and applied AI |
| M5 | 17–18 | Agentic systems, production MLOps, and trustworthy AI guardrails |

<<<<<<< HEAD
## Start here
=======
## Core Engineering Philosophy: The Three-Layer Framework

To avoid the **Commodity Trap** (merely generating syntax, API calls, and boilerplate that LLMs produce in seconds), all fellowship coursework, models, and diagnostic frameworks in this archive are anchored in the **Hierarchy of AI Value**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. FIRST-PRINCIPLES ANCHOR (The Non-Commodity Human Question)          │
│    - What is the underlying physical, economic, or data invariant?     │
│    - Why will a naive off-the-shelf model silently fail here?          │
├────────────────────────────────────────────────────────────────────────┤
│ 2. COMMODITY SCAFFOLDING (What You Let AI Generate)                   │
│    - Boilerplate training loops, standard PyTorch/Scikit-Learn code,   │
│      FastAPI routers, and baseline hyperparameters.                    │
├────────────────────────────────────────────────────────────────────────┤
│ 3. EPISTEMIC RED-TEAMING (The Reality & Invariant Filter)             │
│    - How can this model lie to us? (Data leakage, spurious shortcuts)  │
│    - Hard verification gates (Group splits, Bootstrap CIs, Edge tests) │
└────────────────────────────────────────────────────────────────────────┘
```

- **Tabular ML (Weeks 4-5)**: SHAP is deployed as a strict **leakage detector** against temporal contamination rather than cosmetic plots.
- **Computer Vision (Weeks 9-11)**: Out-of-distribution stress testing (illumination attenuation, synthetic angle jitter) proves morphology learning over background texture.
- **Agentic AI & RAG (Weeks 14-16)**: Replaces circular LLM-as-a-judge with deterministic evaluation harnesses, context firebreaks (`INV-CTX-FIREBREAK`), and $<50\text{ms}$ SLM routing.
- **Capstone (BiasAperture)**: Demographic bias auditing grounded in immutable sample manifests and stratified bootstrap confidence intervals ($B \ge 1000, n < 30$), separating verified live runs from proposed claims.

## Repository Layout
>>>>>>> 9deb2a5 (feat(curriculum): integrate three-layer first-principles framework and sync.bat companion)

- [Learning roadmap](docs/LEARNING_ROADMAP.md) — phases, NotebookLM collections, and concepts to master.
- [Course and source index](docs/COURSE_INDEX.md) — NotebookLM collections, Drive Markdown copies, local notebooks, and weekly project READMEs.
- [Program outline](FUSEMACHINES_FELLOWSHIP_EXTRACT.md) — the archived syllabus and course context.

## Capstone

[BiasAperture](https://github.com/Aaradhya-Dev-Tamrakar/BiasAperture) is the capstone diagnostic framework for measuring and reporting demographic disparities in facial-analysis models. Its Python environment, tests, research, and governance documentation are maintained in that repository.

## Working with the archive

Weeks use separate environments and dependencies. Start with the README in the relevant week folder before installing packages or running a notebook. Notebooks may require datasets, model artifacts, GPU support, or network access.

For repository maintenance, use [sync.ps1](sync.ps1):

```powershell
.\sync.ps1
.\sync.ps1 -m "docs: update archive"
.\sync.ps1 -PullOnly
```

## License

See [LICENSE](LICENSE).
