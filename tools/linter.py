import re
import yaml

# Load YAML rule definitions
with open("rules/java_style_rules.yaml") as f:
    RULES = yaml.safe_load(f)

print(f"🧠 Loaded {len(RULES)} rules from YAML")

def analyze_java_code(file_path):
    violations = []

    violations.append({
        "rule_id": rule["id"],
        "line": lineno,
        "code": line.strip(),
        "suggestion": rule.get("suggestion", "Refer to coding standards."),
        "severity": rule.get("severity", "low"),        # ✅ ADD THIS
        "message": rule.get("description", "")           # ✅ ADD THIS
    })

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"📄 Analyzing {file_path} with {len(lines)} lines...")

    for rule in RULES:
        rule_id = rule.get("id")
        pattern_str = rule.get("pattern")
        suggestion = rule.get("suggestion", "Please review this usage.")

        print(f"🔎 Applying rule {rule_id}: /{pattern_str}/")

        try:
            pattern = re.compile(pattern_str)
        except re.error as e:
            print(f"⚠️ Invalid regex in rule {rule_id}: {e}")
            continue

        for i, line in enumerate(lines, start=1):
            match = pattern.search(line)
            if match:
                print(f"⚠️ Violation at line {i}: {line.strip()}")

                violations.append({
                    "rule_id": rule_id,
                    "line": i,
                    "code": line.strip(),
                    "suggestion": suggestion
                })

    print(f"✅ Found {len(violations)} violations in {file_path}")
    return violations

