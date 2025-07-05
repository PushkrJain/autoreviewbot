# rules/loader.py

import yaml

def load_rules(yaml_file="rules/java_style_rules.yaml"):
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)
    return data["rules"]
