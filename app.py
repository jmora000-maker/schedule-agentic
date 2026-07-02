import streamlit as st
from pathlib import Path
from main import run_pipeline
from src.ui_helpers import (
    severity_rank,
    display_case_summary, 
    display_evidence, 
    display_action_panel,
    display_download_button
)


st.set_page_config(page_title="Schedule Risk Dashboard", layout="wide")
st.title("Schedule Risk Dashboard")
st.caption("Structured case review for slip detection")

if "cases" not in st.session_state:
    st.session_state["cases"] = []

if "selected_case_id" not in st.session_state:
    st.session_state["selected_case_id"] = None


col_a, col_b = st.columns([1, 1])

with col_a:
    if st.button("Run Pipeline", type="primary"):
        with st.spinner("Running pipeline..."):
            result = run_pipeline(Path("data"))
        st.session_state["cases"] = result["cases"]
        if result["cases"]:
            st.session_state["selected_case_id"] = result["cases"][0].case_id
        st.success(f"Generated {len(result['cases'])} cases")

with col_b:
    if st.session_state["cases"]:
        display_download_button(st.session_state["cases"])

cases = st.session_state["cases"]

if cases:
    cases = sorted(cases, key=lambda c: (severity_rank(c.severity), -c.confidence))

    st.subheader("Risk Cases")

    case_map = {c.case_id: f"{c.title} ({c.finding_id}) | {c.severity} | {c.status}" for c in cases}
    selected_case_id = st.selectbox(
        "Select a case", 
        options=list(case_map.keys()),
        format_func=lambda cid: case_map[cid]
    )

    selected_case = next(c for c in cases if c.case_id == selected_case_id)

    left, right = st.columns([2, 1])

    with left:
        display_case_summary(selected_case)
        display_evidence(selected_case.evidence)

    with right:
        display_action_panel(selected_case)

else:
    st.info("Run the pipeline to generate cases.")
