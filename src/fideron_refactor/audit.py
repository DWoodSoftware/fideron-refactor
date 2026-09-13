import re
from pathlib import Path

from fideron_refactor.git import discover_repository_files


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

        if role == "CONFIG":
            for line_number, line in enumerate(
                content.splitlines(),
                start=1,
            ):
                if re.search(
                    r"(?i)(https?://|jdbc:|localhost|127\.0\.0\.1|schedule|port|database|db_|poll|interval|timeout|retries|retry|path|lookback)",
                    line,
                ):
                    findings.append(
                        {
                            "category": "ALREADY_CONFIGURED",
                            "value": line.strip(),
                            "reason": "Operational value already lives in a configuration surface.",
                            "path": relative_path,
                            "line": line_number,
                        }
                    )

    return findings