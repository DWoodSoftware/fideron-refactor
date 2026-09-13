# findings.py

from fideron_refactor.finding_categories import FINDING_CATEGORIES

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

    category_definition = FINDING_CATEGORIES.get(category)

    if category_definition:
        cleanup_policy = category_definition["cleanup_policy"]

        if cleanup_policy == "never":
            return False

        if cleanup_policy == "always":
            return True

        if cleanup_policy == "conditional":
            return any(
                marker in value
                for marker in (
                    "* * * * *",
                    "localhost",
                    "127.0.0.1",
                )
            )


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