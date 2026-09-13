from pathlib import Path


def audit_repository():
    findings = []

    for path in Path.cwd().rglob("*"):
        if not path.is_file():
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        if "localhost" in content.lower():
            findings.append(
                {
                    "category": "ALREADY_CONFIGURED",
                    "value": "localhost",
                    "reason": f"Localhost reference found in {path}",
                    "path": str(path),
                }
            )

    return findings