"""
Script Name: finding_adapter.py
Description: Converts findings to a standardized format.
Author: James Mora
Created: 2026-07-01
Last Modified: 2026-07-01
"""

from typing import Any

# ---------| Finding Adapter |---------
# Converts findings to a standardized format
# for easy consumption by the LLM

def finding_to_dict(finding: Any, fallback_id: str) -> dict:
    if isinstance(finding, dict):
        task_uid = finding.get("task_uid")
        milestone_id = finding.get("milestone_id")
        signal_type = finding.get("signal_type", "unknown_signal")
        
        target = f"task UID {task_uid}" if task_uid else "an unknown task"
        if milestone_id:
            target += f" and milestone {milestone_id}"

        return {
            "id": finding.get("finding_id", finding.get("id", fallback_id)),
            "title": f"{target} - {signal_type}",
            "severity": finding.get("severity", "medium"),
            "confidence": float(finding.get("confidence", 0.5)),
            "impacted_tasks": [str(task_uid)] if task_uid else [],
            "impacted_milestones": [str(milestone_id)] if milestone_id else [],
        }

    task_uid = getattr(finding, "task_uid", None)
    milestone_id = getattr(finding, "milestone_id", None)
    signal_type = getattr(finding, "signal_type", "unknown_signal")

    target = f"task UID {task_uid}" if task_uid else "an unknown task"
    if milestone_id:
        target += f" and milestone {milestone_id}"

    return {
        "id": getattr(finding, "finding_id", getattr(finding, "id", fallback_id)),
        "title": f"{target} - {signal_type}",
        "severity": getattr(finding, "severity", "medium"),
        "confidence": float(getattr(finding, "confidence", 0.5)),
        "impacted_tasks": [str(task_uid)] if task_uid else [],
        "impacted_milestones": [str(milestone_id)] if milestone_id else [],
    }
