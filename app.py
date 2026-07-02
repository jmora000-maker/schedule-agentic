"""
Script Name: main.py
Description: Main entry point for the schedule-risk pipeline.
Author: James Mora
Created: 2026-06-28
Last Modified: 2026-07-02
"""

import streamlit as st
import contextlib
from src.config import data_folder
from pathlib import Path
from main import run_pipeline
from src.ui_helpers import (
    severity_rank,
    display_case_summary,
    display_evidence,
    display_action_panel,
    display_download_button,
    display_download_report_button
)
from src.utils import StreamlitStdoutRedirector


st.set_page_config(page_title="Schedule Risk Case Management", layout="wide")
st.title("Schedule Risk Case Management")
st.caption("PHASE 1: Structured case review for slip detection")

# Initialize session state
if "cases" not in st.session_state:
    st.session_state["cases"] = []

if "selected_case_id" not in st.session_state:
    st.session_state["selected_case_id"] = None


col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("System Configuration")

    # Check if the data folder exists
    if data_folder.exists():

        st.text(f"Files found in '{data_folder.name}'")
        # iterdir() yields Path objects; we grab .name for just the filename
        files = [f.name for f in data_folder.iterdir()]
        st.write(files)

    else:
        st.error(f"Data directory '{data_folder}' does not exist. Please create it and add your files.")

    start_pipeline = st.button("Execute Schedule Risk Pipeline", use_container_width=True, type="primary")

    st.subheader("Pipeline Summary")
    console_logs = st.empty()

    if start_pipeline:
        console_logs.empty()
        redirector = StreamlitStdoutRedirector(console_logs)
        redirector.reset()
        with st.spinner("Running pipeline..."):
            with contextlib.redirect_stdout(redirector):
                result = run_pipeline(Path("data"))
        st.session_state["cases"] = result["cases"]
        if result["cases"]:
            st.session_state["selected_case_id"] = result["cases"][0].case_id
        st.success(f"Generated {len(result['cases'])} cases")
    else:
        console_logs.info("Click 'Execute Schedule Risk Pipeline' button to begin.")



with col_b:
    st.subheader("Case Management")
    # Display selected case details
    cases = st.session_state["cases"]

    # Sort cases by severity and confidence
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
        st.session_state["selected_case_id"] = selected_case.case_id
        display_case_summary(selected_case)
        display_action_panel(selected_case)
        display_download_report_button(selected_case)
    # 3: Display only the evidence here
    if st.session_state.get("selected_case_id"):
        # Fetch the selected case again to display evidence
        cases = st.session_state["cases"]
        selected_case = next(c for c in cases if c.case_id == st.session_state["selected_case_id"])




