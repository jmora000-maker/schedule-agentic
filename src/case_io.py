"""
Script Name: case_io.py
Description: Handles input/output for structured risk cases.
Author: James Mora
Created: 2026-07-01
Last Modified: 2026-07-01
"""

import json
from pathlib import Path
from typing import List
from src.models import SlipRiskCase

# --- CASE IO ---
# This module handles the input and output of structured risk cases.
# It provides functions to save and load cases from JSON files.
# The goal of this module is to make it easier to work with risk cases in a structured format.

def save_cases_to_json(cases: List[SlipRiskCase], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([case.model_dump() for case in cases], f, indent=2)


def load_cases_from_json(input_path:  str | Path) -> List[SlipRiskCase]:
    input_path = Path(input_path)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [SlipRiskCase(**item) for item in data]
