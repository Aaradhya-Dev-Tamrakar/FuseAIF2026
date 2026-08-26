# FuseAIF2026

Central archive for Aaradhya Dev Tamrakar's Fusemachines AI Fellowship 2026 coursework, project notes, notebooks, datasets, reports, and capstone work.

<!-- sync-status:start -->
**Last synchronized:** 2026-08-26
<!-- sync-status:end -->

This is a workspace-level repository. The numbered folders preserve weekly fellowship work; some weeks contain complete local artifacts and others contain archive notes that point to a separate project repository.

## Fellowship

- **Program:** Fusemachines AI Fellowship 2026
- **Duration:** 24 weeks, May 4 to October 18, 2026
- **Current archive coverage:** Modules 1-4, Weeks 1-16
- **Current program position:** Week 17 of 24 as of August 26, 2026
- **Primary themes:** data wrangling, SQL, APIs, agentic systems, classical machine learning, probabilistic modeling, clustering, forecasting, deep learning, computer vision, NLP, and AI assistants
- **Program notes:** [FUSEMACHINES_FELLOWSHIP_EXTRACT.md](FUSEMACHINES_FELLOWSHIP_EXTRACT.md)

## Repository Layout

### Module 1: Foundations and classical ML

- [M1/WK1](M1/WK1/) - data wrangling, SQL, patient and clinical datasets, and exploratory notebooks
- [M1/WK2](M1/WK2/) - FastAPI and PostgreSQL customer management API materials
- [M1/WK3](M1/WK3/) - containerized Text-to-SQL pipeline with FastAPI, Streamlit, PostgreSQL, and Docker
- [M1/WK4](M1/WK4/) - linear models for telco churn and customer lifetime value

### Module 2: Statistical learning

- [M2/WK5](M2/WK5/) - tree-based models, ensembles, SHAP, and model serialization
- [M2/WK6](M2/WK6/) - probabilistic models, Bayesian inference, Gaussian processes, and PyMC
- [M2/WK7](M2/WK7/) - clustering and customer segmentation using RFM and transaction features
- [M2/WK8](M2/WK8/) - S&P 500 forecasting with classical, machine-learning, deep-learning, and ensemble models

### Module 3: Deep learning and computer vision

- [M3/WK9](M3/WK9/) - NEU steel-surface defect classification with CNNs and Optuna
- [M3/WK10](M3/WK10/) - image processing, HSV segmentation, Canny edges, and Hough circle detection
- [M3/WK11](M3/WK11/) - computer vision with CNNs, object detection, segmentation, VAEs, and vision transformers
- [M3/WK12](M3/WK12/) - Week 12 materials, including the NER assignment archive

### Module 4: NLP and applied AI systems

- [M4/WK13](M4/WK13/) - LSTM text classification
- [M4/WK14](M4/WK14/) - agentic routing with encoder-only transformers and small language models
- [M4/WK15](M4/WK15/) - AI assistant and RAG application assignment
- [M4/WK16](M4/WK16/) - Week 16 archive placeholder and future coursework space

### Capstone

- [BiasAperture](fuseai-fellowship/BiasAperture-A-Diagnostic-Framework-for-Demographic-Bias-Auditing-in-Facial-Analysis-Models/) - diagnostic framework for auditing demographic bias in facial-analysis models

BiasAperture is maintained as a nested Python project with its own `pyproject.toml`, `uv.lock`, source package, tests, research, report, and governance documentation. It is scoped as a diagnostic system: it measures and reports disparities but does not retrain or debias the audited model.

## Project Index

The weekly README files provide local setup and deliverable details where available:

- [M1/WK2 README](M1/WK2/README.md)
- [M1/WK3 README](M1/WK3/README.md)
- [M1/WK4 README](M1/WK4/README.md)
- [M2/WK5 README](M2/WK5/README.md)
- [M2/WK6 README](M2/WK6/README.md)
- [M2/WK7 README](M2/WK7/README.md)
- [M2/WK8 README](M2/WK8/README.md)
- [M3/WK9 README](M3/WK9/README.md)
- [M3/WK10 README](M3/WK10/README.md)
- [M3/WK11 README](M3/WK11/README.md)
- [M4/WK13 README](M4/WK13/README.md)
- [M4/WK14 README](M4/WK14/README.md)
- [M4/WK15 README](M4/WK15/README.md)
- [BiasAperture README](fuseai-fellowship/BiasAperture-A-Diagnostic-Framework-for-Demographic-Bias-Auditing-in-Facial-Analysis-Models/README.md)

When a week has no standalone README, start with the notebook, assignment document, or `docs/` folder in that week directory.

## Working With the Archive

This repository contains several independent Python environments rather than one global application. Check the README or dependency file inside the relevant week before installing packages. Notebooks may require datasets, model artifacts, GPU support, or network access that are not shared across weeks.

For the BiasAperture capstone:

```powershell
Set-Location fuseai-fellowship/BiasAperture-A-Diagnostic-Framework-for-Demographic-Bias-Auditing-in-Facial-Analysis-Models
uv sync --extra dev
uv run --extra dev pytest
uv run --extra dev ruff check
uv run --extra dev ruff format --check
```

For notebook-based weeks, open the week directory in VS Code, select an appropriate Python or Jupyter environment, install that week's dependencies, and run the notebook from its repository root so relative dataset paths resolve correctly.

## Repository Maintenance

The workspace uses [sync.ps1](sync.ps1) for the standard pull, commit, and push workflow:

```powershell
.\sync.ps1
.\sync.ps1 -m "docs: update workspace index"
.\sync.ps1 -PullOnly
```

- `graphify-out/` contains generated knowledge-graph output and is maintained by the Graphify workflow.
- `markdownlin.json` contains the workspace markdownlint settings.
- `LICENSE` contains the repository license.
- Generated notebook caches, local environments, secrets, and large raw datasets should remain excluded according to the relevant `.gitignore` files.

## License

See [LICENSE](LICENSE).
