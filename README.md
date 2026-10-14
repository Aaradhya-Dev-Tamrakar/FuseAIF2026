# FuseAIF2026

Central archive for Aaradhya Dev Tamrakar's Fusemachines AI Fellowship 2026 coursework, project notes, notebooks, datasets, reports, and capstone work.

<!-- sync-status:start -->
**Last synchronized:** 2026-10-14
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

## Notebook Index

### Gemini NotebookLM collection

- **Week 2:** AIF 2026 - Week 2: Database & API Architecture
- **Week 3:** AIF 2026 - Week 3: Agentic Text-to-SQL System
- **Weeks 4-5:** AIF 2026 - Weeks 4-5: Supervised Tabular ML (Linear & Tree Ensembles)
- **Weeks 6 & 8:** AIF 2026 - Weeks 6 & 8: Probabilistic ML & Time Series Forecasting
- **Week 7:** AIF 2026 - Week 7: Clustering & Market Segmentation
- **Weeks 9-11:** AIF 2026 - Weeks 9-11: Deep Learning & Computer Vision
- **Weeks 12-14:** AIF 2026 - Weeks 12-14: NLP, Sequence Learning & Transformers
- **Weeks 15-16:** AIF 2026 - Weeks 15-16: Applied AI, RAG & Multi-Agent Systems
- **Week 17:** AIF 2026 - Week 17: AI Systems & MLOps
- **Week 25:** AIF 2026 - Week 25: Responsible & Trustworthy AI

### Repository Jupyter notebooks

All Jupyter notebooks currently in the archive are listed below. The executed copies are linked separately where the archive keeps both a source notebook and an executed notebook.

### Module 1

- **Week 1:** [Data Wrangling pre-week](M1/WK1/DataWranglingPreW1.ipynb); [Heart Attack Data Wrangling](M1/WK1/Wk_1_Data_Wrangling_HeartAttack.ipynb); copies in [`M1/WK1/notebooks/`](M1/WK1/notebooks/): [Data Wrangling pre-week](M1/WK1/notebooks/DataWranglingPreW1.ipynb), [Heart Attack Data Wrangling](M1/WK1/notebooks/Wk_1_Data_Wrangling_HeartAttack.ipynb)
- **Week 4:** [Linear Models Assignment](M1/WK4/W4_Linear_Models_Assignment.ipynb); [executed copy](M1/WK4/W4_Linear_Models_Assignment_executed.ipynb)

### Module 2

- **Week 5:** [Tree-Based Models and Ensembles Assignment](M2/WK5/W5_Tree-Based%20Models%20%26%20Ensembles_Assignment.ipynb)
- **Week 6:** [Probabilistic Models Assignment](M2/WK6/W6_Probabilistic_Models_Assignment.ipynb)
- **Week 7:** [Clustering Assignment](M2/WK7/Week_7_Clustering_Assignment_executed.ipynb); [development artifact copy](M2/WK7/misc/dev_artifacts/Week_7_Clustering_Assignment.ipynb)
- **Week 8:** [Forecasting Assignment](M2/WK8/W8_Forecasting_Assignment.ipynb)

### Module 3

- **Week 9:** [NEU Defect CNN Assignment](M3/WK9/W9_NEU_Defect_CNN_Assignment.ipynb)
- **Week 10:** [Image Processing Assignment](M3/WK10/assignment/W10_Image_Processing_Assignment.ipynb); [executed copy](M3/WK10/W10_Image_Processing_Assignment_executed.ipynb)
- **Week 11:** [Computer Vision Assignment](M3/WK11/notebooks/W11_CV_Assignment_Notebook.ipynb)
- **Week 12:** [NER Customer Support Assignment](M3/WK12/notebooks/Assignment3_NER_CustomerSupport.ipynb)

### Module 4

- **Week 13:** [LSTMs for Text Classification](M4/WK13/LSTMs_for_Text_Classification.ipynb)
- **Week 14:** [Support Routing](M4/WK14/support_routing.ipynb); split notebooks: [Part A — encoders](M4/WK14/split/support_routing_partA_encoders_v2.ipynb) and [Part B — small language models](M4/WK14/split/support_routing_partB_slms_v2.ipynb)

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
