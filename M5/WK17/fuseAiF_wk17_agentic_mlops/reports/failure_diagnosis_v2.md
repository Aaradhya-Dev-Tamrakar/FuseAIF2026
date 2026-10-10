# Prompt v2 — Trace Failure Diagnosis

## Description
Conflict-Aware prompt — mandatory release notes cross-check on version/price/config values

## Observed Failure Pattern
The v2 conflict-aware rule successfully fixes pricing and deprecation errors (GR-001, GR-004, GR-007 now pass). However, trace analysis reveals trajectory length increased from 3.8 to 5.2 average iterations. Root cause: the mandatory cross-check triggers broad search_knowledge_base calls like 'release notes latest' which match multiple documents, causing redundant read_document calls on already-seen content. Token consumption increases 35% despite improved accuracy.

## Metrics Summary
| Metric | Value |
|:---|:---:|
| Task Completion Rate | 80% |
| Tool Correctness | 85% |
| Mean Trajectory Length | 5.2 |
| Total Tokens | 19,100 |
| Cost (USD) | $0.0096 |
| Regression Tests Passed | 80% |
