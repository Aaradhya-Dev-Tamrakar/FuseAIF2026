# Prompt v3 — Trace Failure Diagnosis

## Description
Optimized Precedence + Query Reformulation prompt — targeted search, scratchpad logging, early synthesis gate

## Observed Failure Pattern
v3 achieves the highest task completion rate (90%) with the lowest mean trajectory length (3.4) and token cost. The targeted search heuristic eliminates broad queries that caused redundant reads in v2. Mandatory scratchpad logging after each tool call prevents re-reading documents. The early synthesis gate (>= 3 passages) allows the agent to finalize answers sooner. One failure remains on GR-009 (complex multi-hop database migration question) where the agent synthesizes too early.

## Metrics Summary
| Metric | Value |
|:---|:---:|
| Task Completion Rate | 90% |
| Tool Correctness | 93% |
| Mean Trajectory Length | 3.4 |
| Total Tokens | 12,800 |
| Cost (USD) | $0.0064 |
| Regression Tests Passed | 90% |
