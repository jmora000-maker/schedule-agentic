"""
Script Name: main.py
Description: Main entry point for the schedule-risk pipeline.
Author: James Mora
Created: 2026-06-28
Last Modified: 2026-07-01
"""

from pathlib import Path
from src.config import vector_store_folder
from src.taxonomy import CorporateTaxonomyNormalizer
from src.inputs import ProjectArtifactLoader
from src.graph_manager import GraphManager
from src.rules import RuleEngine
from src.rag import RAGEngine
from src import llm, report
from src.case_builder import build_cases
from src.case_io import save_cases_to_json

def run_pipeline(data_path: Path = Path("data")) -> dict:
    print("PIPELINE STARTED")

    # 1. Ingest Data
    print("STEP 1: Ingesting Data.")
    normalizer = CorporateTaxonomyNormalizer()
    loader = ProjectArtifactLoader(normalizer)
    loader.load_project_artifacts(data_path)

    # 2. Build Graph
    print("STEP 2: Building Knowledge Graph.")
    graph = GraphManager(graph_path="knowledge_graph/graph.json")
    graph.build_from_artifacts(
        loader.tasks,
        loader.milestones,
        loader.issues,
        loader.task_updates,
        loader.delivery_notes,
        loader.signals
    )
    graph.save()

    # 3. Rule Engine
    print("STEP 3: Running Rule Engine.")
    engine = RuleEngine(loader, graph)
    findings = engine.run()
    print(f" -> Found {len(findings)} risk findings.")

    # 4. RAG and LLM
    print("STEP 4: RAG & LLM Synthesis.")
    rag_dir = vector_store_folder
    rag_engine = RAGEngine.load(rag_dir)
    if not rag_engine:
        print(" -> Building RAG Engine.")
        rag_engine = RAGEngine(loader.raw_chunks)
        rag_engine.save(rag_dir)
    else:
        print(" -> Loaded RAG Engine from vector_store.")

    print(f" -> Building evidence map for {len(findings)} findings.")

    print(" -> Generating risk explanations using LLM.")
    explanations, evidence_map = llm.generate_explanations_and_evidence(findings, rag_engine, graph)

    # 5. Case Generation (Primary Output)
    print("STEP 5: Generating Slip Risk Cases (Primary).")
    cases = build_cases(
        findings=findings,
        explanations=explanations,
        evidence_map=evidence_map,
    )
    save_cases_to_json(cases, "outputs/slip_risk_cases.json")

    # 6. Reporting (Secondary / Backward Compatibility)
    print("STEP 6: Generating Report (Secondary).")
    report_text = report.build_schedule_risk_report(findings, explanations, evidence_map, loader.milestones)

    with open("outputs/schedule_risk_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)

    print("PIPELINE COMPLETED")

    return {
        "cases": cases,
        "cases_json_path": "outputs/slip_risk_cases.json",
        "report_text": report_text,
        "report_path": "outputs/schedule_risk_report.txt",
    }


if __name__ == "__main__":
    result = run_pipeline()
    print(f"Generated {len(result['cases'])} cases")
    print(f"Cases JSON: {result['cases_json_path']}")
