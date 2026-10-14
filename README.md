# FuseAIF2026

This repository archives weekly coursework, notebooks, datasets, and project work from the Fusemachines AI Fellowship 2026.

<!-- sync-status:start -->
**Last synchronized:** 2026-10-14
<!-- sync-status:end -->

## Archive

Course materials are grouped by module and week. Some weeks contain full local projects; others point to a separate project repository.

| Module | Weeks | Focus |
| --- | --- | --- |
| M1 | 1–4 | Data wrangling, databases, APIs, and linear models |
| M2 | 5–8 | Statistical learning, clustering, and forecasting |
| M3 | 9–12 | Deep learning, computer vision, and NLP foundations |
| M4 | 13–16 | Sequence learning, transformers, and applied AI |
| M5 | 17 | Agentic systems and MLOps |

## Start here

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
