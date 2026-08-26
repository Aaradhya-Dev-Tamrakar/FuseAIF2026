# fuseAiF_wk12_ner_customer_support

Week 12 — End-to-End Named Entity Recognition (NER) for Customer Support Ticket Analysis · Fusemachines AI Fellowship

Business scenario: identify key entities (persons, organizations, locations, misc) in customer support tickets to automate triage/routing and CRM updates. Full spec in [`docs/W12_NER_Assignment_Brief.md`](docs/W12_NER_Assignment_Brief.md).

## Structure

```
.
├── notebooks/
│   └── Assignment3_NER_CustomerSupport.ipynb   # main deliverable — Tasks 1-6
├── docs/
│   └── W12_NER_Assignment_Brief.md             # assignment spec (tasks, deliverables, rubric)
├── sync.ps1
├── README.md
└── LICENSE
```

## Tasks

1. **Text Preprocessing & EDA** — CoNLL-2003 load, tokenization, sentence-length/word-frequency/entity-distribution visualizations
2. **Feature Engineering** — `word2features`: case, 1-3 char prefix/suffix, orthographic flags, ±1 neighbor context
3. **NER Model (CRF)** — `sklearn-crfsuite`, lbfgs, L1/L2 regularized, entity-wise P/R/F1
4. **Error Analysis** — sample predicted-vs-true mismatches, top 3 error patterns
5. **Business Impact** — ticket-routing/CRM automation case, phased Agent-Assist → Transformer deployment recommendation
6. **Extended Analysis — WNUT-17** — same pipeline (reused feature functions, isolated `wnut_`-prefixed namespace) on noisy, emerging-entity Twitter data; CoNLL vs. WNUT-17 comparative discussion

## How to run

Colab or local, CPU is fine (CRF, not a neural net).

```bash
pip install datasets scikit-learn sklearn-crfsuite matplotlib
```

Run `notebooks/Assignment3_NER_CustomerSupport.ipynb` top-to-bottom. CoNLL-2003 and WNUT-17 both auto-download via `datasets.load_dataset(..., revision="convert/parquet")` on first run.

## Status

**Tasks 1–5: complete, executed, outputs verified.** Task 6 (WNUT-17) code added and reviewed but not yet executed in this environment — run top-to-bottom to populate its outputs.

| Metric (CoNLL-2003 test set) | Value |
|---|---|
| Train / val / test sentences | 14,041 / 3,250 / 3,453 |
| Train vocabulary size | 23,623 |
| Avg / max sentence length | 14.50 / 113 tokens |
| Micro F1 | 0.807 |
| Macro F1 | 0.780 |
| Best entity (F1) | I-PER — 0.911 |
| Weakest entity (F1) | I-MISC — 0.661 |

### Bugs found and fixed during review

- **Cell 12 (sentence-length interpretation)** — markdown claimed lengths "clustered between 100 and 200 tokens," contradicting the cell's own printed stats (avg 14.50, max 113). Corrected to match the actual computed output.
- **Cell 14 (least-frequent-words)** — a self-addressed TODO ("Perform Simmilar Kinds of visualization... for least common words") was left unimplemented. Added the bottom-30 frequency chart and interpretation.

## License

MIT
