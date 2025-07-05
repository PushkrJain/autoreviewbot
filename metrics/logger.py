import os
import csv
import json
from datetime import datetime

CSV_LOG = "metrics/logs/violations.csv"
JSON_LOG = "metrics/logs/violations.jsonl"

HEADERS = [
    "timestamp", "repo", "pr_number", "filename",
    "line", "rule_id", "severity", "message"
]

# Ensure header written only once
def initialize_logs():
    if not os.path.exists(CSV_LOG):
        with open(CSV_LOG, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()

def log_violation(data: dict):
    timestamp = datetime.utcnow().isoformat()
    entry = {
        "timestamp": timestamp,
        "repo": data["repo"],
        "pr_number": data["pr_number"],
        "filename": data["filename"],
        "line": data["line"],
        "rule_id": data["rule_id"],
        "severity": data["severity"],
        "message": data["message"]
    }

    # Append to CSV
    with open(CSV_LOG, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(entry)

    # Append to JSONL
    with open(JSON_LOG, mode='a') as f:
        json.dump(entry, f)
        f.write('\n')
