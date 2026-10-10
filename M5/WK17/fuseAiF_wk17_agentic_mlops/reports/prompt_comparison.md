# Prompt Version Comparison — MLflow Experiment Tracking

**Experiment**: `AgenticAI_Prompt_Evaluation`
**Model**: gemini-2.0-flash | **Max Iterations**: 8 | **Retrieval k**: 5

| Version | Completion Rate | Tool Correctness | Avg Trajectory | Tokens | Cost (USD) | Tests Passed | Key Change |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **v1** | 60% | 72% | 3.8 | 14,200 | $0.0071 | 60% | Baseline W16 ReAct prompt |
| **v2** | 80% | 85% | 5.2 | 19,100 | $0.0096 | 80% | +Mandatory release notes cross-check |
| **v3** | 90% | 93% | 3.4 | 12,800 | $0.0064 | 90% | +Query reformulation, scratchpad logging, early synthesis |

### Iteration Narrative

1. **v1 (Baseline)**: The W16 ReAct prompt achieves 60% task completion. Trace analysis reveals the agent reads the first matching document and finalizes without checking for superseding updates. Conflict-resolution and deprecation queries fail systematically.

2. **v2 (Conflict-Aware)**: Adding the mandatory release-notes cross-check rule fixes conflict and deprecation failures, improving completion to 80%. However, the rule triggers broad searches ('release notes latest') that match multiple irrelevant documents, inflating mean trajectory to 5.2 iterations and token cost by 35%.

3. **v3 (Optimized)**: Targeted query reformulation, mandatory scratchpad logging, and an early synthesis gate reduce trajectory to 3.4 iterations (lowest) while achieving 90% completion (highest). Token consumption drops below v1 baseline. One remaining failure on complex multi-hop migration queries where early synthesis triggers prematurely.

### Trade-off: v3 wins on both accuracy and cost
- **v3 vs v1**: +50% completion rate, -10% tokens, -10% cost
- **v3 vs v2**: +12.5% completion rate, -33% tokens, -33% cost
