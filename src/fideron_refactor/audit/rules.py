AUDIT_RULES = [
    {
        "role": "CONFIG",
        "pattern": (
            r"(?i)"
            r"(https?://|jdbc:|localhost|127\.0\.0\.1|"
            r"schedule|port|database|db_|poll|interval|"
            r"timeout|retries|retry|path|lookback)"
        ),
        "category": "ALREADY_CONFIGURED",
        "reason": (
            "Operational value already lives in a "
            "configuration surface."
        ),
    },
    {
        "role": "PRODUCTION",
        "pattern": (
            r"(?i)"
            r"(https?://localhost|"
            r"https?://127\.0\.0\.1|"
            r"jdbc:.*localhost)"
        ),
        "category": "EXTRACT",
        "reason": (
            "Operational value is hardcoded in production code."
        ),
    },
]