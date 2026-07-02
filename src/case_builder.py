"""
Script Name: case_builder.py
Description: Converts findings and explanations into structured cases for risk triage.
Author: James Mora
Created: 2026-07-01
Last Modified: 2026-07-01
"""

from typing import List, Dict, Any
from src.models import SlipRiskCase, EvidenceItem, RecommendedAction, RetrievedEvidenceBundle, ArtifactChunk
from src.finding_adapter import finding_to_dict

# --- CASE BUILDER ---
# This module converts raw findings and explanations into structured cases for risk triage.
# It leverages the finding_adapter module to adapt raw findings to the SlipRiskCase format.
# The cases are then built based on the provided explanations and evidence maps.
# The goal of this module is to prepare the findings and explanations for risk triage.
# 1. Convert raw findings to SlipRiskCase format
# 2. Build cases based on explanations and evidence maps
# 3. Return the list of cases

def _safe_get(obj: Any, attr: str, default=None):
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)


def _normalize_evidence(raw_evidence) -> List[EvidenceItem]:
    items = []
    if not raw_evidence:
        return items

    # Handle RetrievedEvidenceBundle
    if isinstance(raw_evidence, RetrievedEvidenceBundle):
        raw_evidence = raw_evidence.evidence_bundle

    for ev in raw_evidence:
        if isinstance(ev, EvidenceItem):
            items.append(ev)
            continue
        
        if isinstance(ev, ArtifactChunk):
            items.append(
                EvidenceItem(
                    source_type=ev.artifact_type,
                    source_id=ev.source_artifact,
                    quote=ev.text
                )
            )
            continue

        if isinstance(ev, dict):
            items.append(
                EvidenceItem(
                    source_type=ev.get("source_type", "unknown"),
                    source_id=ev.get("source_id"),
                    quote=ev.get("quote", str(ev)),
                    relevance=ev.get("relevance"),
                )
            )
        else:
            items.append(
                EvidenceItem(
                    source_type="unknown",
                    quote=str(ev),
                )
            )
    return items


def _build_default_action(finding_data: dict, explanation_text: str) -> RecommendedAction:
    severity = str(finding_data.get("severity", "medium")).lower()

    if severity in {"high", "critical"}:
        return RecommendedAction(
            action="Review immediately and assign an owner to validate impact and recovery options.",
            owner_role="Project Manager",
            due_date="Next working day",
            rationale="Severity indicates likely schedule impact requiring fast triage."
        )

    return RecommendedAction(
        action="Review in weekly risk triage and confirm whether intervention is needed.",
        owner_role="Project Manager",
        due_date="This week",
        rationale="Initial signal exists , but urgency appears moderate."
    )


def build_cases(
    findings: List[Any],
    explanations: Dict[str, str],
    evidence_map: Dict[str, List[Any]],
) -> List[SlipRiskCase]:
    cases: List[SlipRiskCase] = []

    for idx, finding in enumerate(findings, start=1):
        finding_data = finding_to_dict(finding, f"finding-{idx}")
        finding_id = finding_data["id"]
        title = finding_data["title"]
        severity = finding_data["severity"]
        confidence = finding_data["confidence"]

        explanation = explanations.get(finding_id)
        summary = explanation.summary if explanation else "Potential schedule risk detected."
        raw_evidence = evidence_map.get(finding_id, [])

        impacted_tasks = finding_data["impacted_tasks"]
        impacted_milestones = finding_data["impacted_milestones"]

        case = SlipRiskCase(
            case_id=f"case-{finding_id}",
            finding_id=finding_id,
            title=title,
            summary=summary,
            severity=severity,
            confidence=confidence,
            impacted_tasks=list(impacted_tasks),
            impacted_milestones=list(impacted_milestones),
            evidence=_normalize_evidence(raw_evidence),
            recommended_action=_build_default_action(finding_data, summary),
            metadata={
                "source": "case_builder_phase_1"
            }
        )
        cases.append(case)

    return cases
