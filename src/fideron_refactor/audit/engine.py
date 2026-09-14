import re
from pathlib import Path

from fideron_refactor.audit.rules import AUDIT_RULES
from fideron_refactor.findings.types import classify_finding_type
from fideron_refactor.repository.discovery import discover_repository_files
from fideron_refactor.repository.roles import classify_file_role


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


def audit_repository(
    ignore_paths: list[str] | None = None,
) -> list[dict]:
    findings = []

    for relative_path in discover_repository_files(
        ignore_paths=ignore_paths,
    ):
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