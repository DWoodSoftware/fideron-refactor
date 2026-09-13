# findings.py

CLEANUP_CATEGORIES = {
    "EXTRACT",
    "SECRET",
}

CLEANUP_VALUE_HINTS = {
    "time.sleep(",
    "schedule",
    "token_path",
    "password",
    "config.yaml",
    "scheduler.json",
    "manifest",
    "localhost",
    "127.0.0.1",
}


def is_cleanup_target(finding: dict) -> bool:
    category = finding.get("category", "")
    value = finding.get("value", "").lower()
    reason = finding.get("reason", "").lower()

    if category in {"REVIEW", "KEEP"}:
        return False

    if category == "ALREADY_CONFIGURED":
        return any(
            marker in value
            for marker in (
                "* * * * *",
                "localhost",
                "127.0.0.1",
            )
        )

    if category in CLEANUP_CATEGORIES:
        return True

    if any(hint in value for hint in CLEANUP_VALUE_HINTS):
        return True

    return any(
        marker in reason
        for marker in (
            "hardcoded",
            "secret",
            "temporary",
        )
    )