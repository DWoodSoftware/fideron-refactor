import re
from pathlib import Path

from fideron_refactor.audit_rules import AUDIT_RULES
from fideron_refactor.finding_types import classify_finding_type
from fideron_refactor.git import discover_repository_files


def apply_audit_rule(
    *,
    rule: dict,
    content: str,
    relative_path: str,
) -> list[dict]:
    findings = []

    for line_number, line in enumerate(
        content.splitlines(),
        start=1,
    ):
        if not re.search(rule["pattern"], line):
            continue

        findings.append(
            {
                "category": rule["category"],
                "type": classify_finding_type(line),
                "value": line.strip(),
                "reason": rule["reason"],
                "path": relative_path,
                "line": line_number,
            }
        )

    return findings

def classify_file_role(relative_path: str) -> str:
    path = relative_path.replace("\\", "/")

    test_patterns = (
        r"(^|/)tests?/",
        r"(^|/)test/",
        r"(?i)(^|/).*test_.*\.py$",
        r"(?i).*Spec\.scala$",
    )

    if any(re.search(pattern, path) for pattern in test_patterns):
        return "TEST"

    config_patterns = (
        r"(?i)application\.conf$",
        r"(?i)(docker-)?compose\.ya?ml$",
        r"(?i)scheduler\.json$",
        r"(?i)config\.ya?ml$",
        r"(?i)(^|/)\.env(\..*)?$",
    )

    if any(re.search(pattern, path) for pattern in config_patterns):
        return "CONFIG"

    return "PRODUCTION"

def audit_repository():
    findings = []

    for relative_path in discover_repository_files():
        path = Path.cwd() / relative_path

        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        role = classify_file_role(relative_path)

        for rule in AUDIT_RULES:
            if rule["role"] != role:
                continue

            findings.extend(
                apply_audit_rule(
                    rule=rule,
                    content=content,
                    relative_path=relative_path,
                )
            )

    return findings