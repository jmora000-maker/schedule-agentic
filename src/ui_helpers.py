"""
Script Name: ui_helpers.py
Description: Helper functions for Streamlit UI components.
Author: James Mora
Created: 2026-07-01
Last Modified: 2026-07-01
"""



import json
from typing import List, Any
import streamlit as st
from src.models import SlipRiskCase, EvidenceItem

# --- UI HELPERS ---
# This module contains helper functions for Streamlit UI components.
# It provides functions to display case summaries, evidence, and action panels.
# The goal of this module is to make the UI components more user-friendly and consistent.

def severity_rank(severity: str) -> int:
    order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }
    return order.get(str(severity).lower(), 99)


def update_case_in_state(updated_case: SlipRiskCase):
    updated_cases = []
    for c in st.session_state["cases"]:
        if c.case_id == updated_case.case_id:
            updated_cases.append(updated_case)
        else:
            updated_cases.append(c)
    st.session_state["cases"] = updated_cases


def display_case_summary(case: SlipRiskCase):
    st.markdown("### Case Summary")
    st.write(f"**Title:** {case.title}")
    st.write(f"**Severity:** {case.severity}")
    st.write(f"**Confidence:** {case.confidence}")
    st.write(f"**Status:** {case.status}")
    st.write(f"**Summary:** {case.summary}")

    st.markdown("### Impact")
    st.write("**Impacted Tasks:**", case.impacted_tasks or [])
    st.write("**Impacted Milestones:**", case.impacted_milestones or [])

    st.markdown("### Structured JSON")
    st.json(case.model_dump())


def display_evidence(evidence: List[EvidenceItem]):
    st.markdown("### Evidence")
    if evidence:
        for i, ev in enumerate(evidence, start=1):
            st.markdown(f"**Evidence {i}**")
            st.write(f"- Source Type: {ev.source_type}")
            st.write(f"- Source ID: {ev.source_id}")
            st.write(f"- Quote: {ev.quote}")
            if ev.relevance:
                st.write(f"- Relevance: {ev.relevance}")
    else:
        st.write("No evidence attached.")


def display_action_panel(case: SlipRiskCase):
    st.markdown("### Action Panel")

    new_status = st.selectbox(
        "Update status",
        ["new", "reviewing", "assigned", "deferred", "resolved"],
        index=["new", "reviewing", "assigned", "deferred", "resolved"].index(
            case.status if case.status in ["new", "reviewing", "assigned", "deferred", "resolved"] else "new"
        ),
        key=f"status_{case.case_id}"
    )

    if st.button("Apply Status"):
        case.status = new_status
        update_case_in_state(case)
        st.success(f"Case status updated to '{new_status}'")

    st.markdown("### Recommended Action")
    if case.recommended_action:
        st.write(f"**Action:** {case.recommended_action.action}")
        st.write(f"**Owner Role:** {case.recommended_action.owner_role}")
        st.write(f"**Due Date:** {case.recommended_action.due_date}")
        st.write(f"**Rationale:** {case.recommended_action.rationale}")
    else:
        st.write("No recommendation available.")

    st.markdown("### Manual Triage Notes")
    triage_note = st.text_area("Add reviewer note", key=f"note_{case.case_id}")

    if st.button("Save Note"):
        notes = case.metadata.get("triage_notes", [])
        if triage_note.strip():
            notes.append(triage_note.strip())
        case.metadata["triage_notes"] = notes
        update_case_in_state(case)
        st.success("Note saved")

def display_download_button(cases: List[SlipRiskCase]):
    cases_json = [c.model_dump() for c in cases]
    st.download_button(
        label="Download Case JSON",
        data=json.dumps(cases_json, indent=2),
        file_name="slip_risk_cases.json",
        mime="application/json",
    )
