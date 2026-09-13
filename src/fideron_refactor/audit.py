from pathlib import Path

from fideron_refactor.git import discover_repository_files


def audit_repository():
    findings = []

    for relative_path in discover_repository_files():
        path = Path.cwd() / relative_path

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
                    "path": relative_path,
                }
            )

    return findings