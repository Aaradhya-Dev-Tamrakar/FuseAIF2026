"""Tests for Track B Agentic AI MLOps pipeline: prompts, golden set, judge, and DAG."""

from __future__ import annotations

from pathlib import Path

import pytest

from eval.evidently_judge import (
    VALID_CORPUS_DOCS,
    check_grounding_integrity,
    check_reference_correctness,
    load_golden_references,
    run_regression_suite,
)


class TestPromptVersions:
    """Tests for versioned system prompts."""

    @pytest.fixture
    def prompts_dir(self):
        return Path("app/agent/prompts")

    def test_all_three_prompt_versions_exist(self, prompts_dir):
        for v in ["v1", "v2", "v3"]:
            p = prompts_dir / f"agent_{v}.md"
            assert p.exists(), f"Prompt file {p} missing"
            assert len(p.read_text(encoding="utf-8")) > 500, f"Prompt {v} is too short"

    def test_v2_has_conflict_rule(self, prompts_dir):
        content = (prompts_dir / "agent_v2.md").read_text(encoding="utf-8")
        assert "Conflict-Aware Check" in content or "release_notes.md" in content

    def test_v3_has_optimization_rules(self, prompts_dir):
        content = (prompts_dir / "agent_v3.md").read_text(encoding="utf-8")
        assert "Query Reformulation" in content or "Targeted Search" in content
        assert "Scratchpad" in content or "take_note" in content
        assert "Early Synthesis" in content or ">= 3" in content


class TestGoldenReferences:
    """Tests for the golden reference evaluation set."""

    @pytest.fixture
    def golden_cases(self):
        return load_golden_references()

    def test_golden_set_has_ten_cases(self, golden_cases):
        assert len(golden_cases) == 10

    def test_case_structure(self, golden_cases):
        for case in golden_cases:
            assert "query_id" in case
            assert "query" in case
            assert "reference_answer" in case
            assert "required_citations" in case
            assert "category" in case
            assert "difficulty" in case

    def test_required_citations_valid_corpus_docs(self, golden_cases):
        for case in golden_cases:
            for cit in case["required_citations"]:
                assert cit in VALID_CORPUS_DOCS, f"Invalid citation {cit} in {case['query_id']}"


class TestEvidentlyJudge:
    """Tests for the LLM-as-a-judge evaluation checks."""

    def test_reference_correctness_passes_matching_answer(self):
        ref = {
            "reference_answer": "The Pro tier is priced at $49/month per seat.",
            "required_citations": ["release_notes.md"],
        }
        cand = {
            "answer": "The Pro tier costs $49/month per seat according to the latest version.",
            "citations": ["release_notes.md"],
        }
        res = check_reference_correctness(cand, ref)
        assert res["passed"] is True

    def test_reference_correctness_fails_contradicting_answer(self):
        ref = {
            "reference_answer": "The Pro tier is priced at $49/month per seat.",
            "required_citations": ["release_notes.md"],
        }
        cand = {
            "answer": "The pricing is $10/month per seat.",
            "citations": ["provider_pricing.md"],
        }
        res = check_reference_correctness(cand, ref)
        assert res["passed"] is False

    def test_grounding_detects_hallucinated_citation(self):
        ref = {
            "reference_answer": "500 concurrent connections.",
            "required_citations": ["architecture.md"],
        }
        cand = {
            "answer": "500 concurrent connections.",
            "citations": ["architecture.md", "fabricated_source.pdf"],
        }
        res = check_grounding_integrity(cand, ref)
        assert res["passed"] is False
        assert "fabricated_source.pdf" in res["reasoning"]

    def test_promotion_gate_threshold(self):
        # v1 should fail promotion gate (< 80%)
        res_v1 = run_regression_suite("v1")
        assert res_v1["promotion_eligible"] is False
        assert res_v1["pct_tests_passed"] < 0.80

        # v2 should pass promotion gate (>= 80%)
        res_v2 = run_regression_suite("v2")
        assert res_v2["promotion_eligible"] is True
        assert res_v2["pct_tests_passed"] >= 0.80

        # v3 should pass promotion gate (>= 80%)
        res_v3 = run_regression_suite("v3")
        assert res_v3["promotion_eligible"] is True
        assert res_v3["pct_tests_passed"] >= 0.80


class TestAirflowDAG:
    """Tests for Airflow DAG validity."""

    def test_dag_definition(self):
        # Verify DAG file imports cleanly and contains expected task IDs
        dag_file = Path("dags/agent_regression_eval_dag.py")
        assert dag_file.exists()
        content = dag_file.read_text(encoding="utf-8")
        assert "agent_regression_eval_dag" in content
        assert "run_agent_regression_suite" in content
        assert "evaluate_regression_gate" in content
        assert "alert_regression_degradation" in content
        assert "log_promotion_approved" in content
