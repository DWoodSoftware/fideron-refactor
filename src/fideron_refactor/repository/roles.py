import re


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
