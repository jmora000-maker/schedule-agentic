import json
from pathlib import Path

# Path to the JSON file
json_path = Path("outputs/slip_risk_cases.json")

if not json_path.exists():
    print("JSON file not found.")
else:
    with open(json_path, "r", encoding="utf-8") as f:
        cases = json.load(f)
    
    print(f"Loaded {len(cases)} cases.")
    for case in cases:
        print(f"Case ID: {case['case_id']}, Evidence count: {len(case['evidence'])}")
        # Print a snippet of the quote to compare evidence across cases
        for ev in case['evidence']:
            print(f" - Quote: {ev['quote'][:50]} (Source ID: {ev['source_id']})")
