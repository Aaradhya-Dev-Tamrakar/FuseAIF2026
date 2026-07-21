# fuseAiF_wk6_probabilistic_models

Week 6 — Fusemachines AI Fellowship 2026. Probabilistic models and Bayesian inference, submitted via Google Classroom.

## Submission

| File | Contents |
| --- | --- |
| [`W6_Probabilistic_Models_Assignment.ipynb`](W6_Probabilistic_Models_Assignment.ipynb) | Fully executed notebook (31/31 code cells, sequential 1–31, no errors). Parts 1–6: MLE/MAP/full-posterior estimation, sequential Bayesian updating, multivariate Gaussians, Bayesian Network + MRF, Gaussian Process regression on Mauna Loa CO₂, and Bayesian logistic regression via PyMC/NUTS. |
| [`telco_bayes_lr_v1.pkl`](telco_bayes_lr_v1.pkl) | Fitted PyMC `InferenceData` trace from Part 6 (4 chains × 2,000 draws, R̂ 1.000–1.001, bulk-ESS 5,021–7,238). File size: ~345 MB. Tracked with **Git LFS** — see below before cloning. |
| [`Reflection.md`](Reflection.md) | One-page reflection: where the full Bayesian posterior would change a decision an MLE-only read would not. |

## Repository structure

```.
├── README.md
├── Reflection.md
├── W6_Probabilistic_Models_Assignment.ipynb
├── telco_bayes_lr_v1.pkl                        (LFS)
├── docs/
│   ├── W6_Probabilistic_Models_Resource_Guide.pdf   ← facilitator-provided assignment guide
│   └── GIT_LFS_GUIDE.md                             ← LFS setup/troubleshooting reference
├── .gitattributes                                (declares *.pkl → LFS)
├── .gitignore
├── LICENSE
└── CHANGELOG.md
```

## Cloning this repo

`telco_bayes_lr_v1.pkl` is 345 MB and stored via Git LFS. Without LFS installed, `git clone` will pull a text pointer instead of the file:

```bash
git lfs install
git clone https://github.com/AaradhyaDT/fuseAiF_wk6_probabilistic_models.git
```

## Running the notebook

Dependencies (`pymc`, `arviz`, `pgmpy`, `scikit-learn`, `statsmodels`, `scipy`) install from the notebook's own setup cell — no separate `requirements.txt` needed. Open in Google Colab or Jupyter and run top to bottom.
