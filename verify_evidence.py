from pathlib import Path
from main import run_pipeline
from src.models import SlipRiskCase

# Run the pipeline
result = run_pipeline(Path("data"))
cases = result["cases"]

print(f"Generated {len(cases)} cases")
for case in cases:
    print(f"Case: {case.case_id}, Title: {case.title}, Finding ID: {case.finding_id}, Evidence count: {len(case.evidence)}")
    for ev in case.evidence:
        print(f" - Evidence: {ev.source_type} - {ev.quote[:50]} - ID: {ev.source_id}")
