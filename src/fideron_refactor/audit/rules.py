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
    {
        "role": "PRODUCTION",
        "pattern": r"(?i)\btime\.sleep\s*\(\s*\d+(?:\.\d+)?\s*\)",
        "category": "EXTRACT",
        "reason": "Operational delay is hardcoded in production code.",
    },
    {
        "role": "PRODUCTION",
        "pattern": (
            r"(?i)"
            r"\b("
            r"[A-Z_]*TIMEOUT|"
            r"[A-Z_]*INTERVAL|"
            r"[A-Z_]*DELAY|"
            r"[A-Z_]*TTL"
            r")\b"
            r"\s*=\s*"
            r"("
            r"\d+(?:\.\d+)?|"
            r"timedelta\s*\([^)]*\)"
            r")"
        ),
        "category": "EXTRACT",
        "reason": "Operational timing value is hardcoded in production code.",
    },
    {
        "role": "PRODUCTION",
        "pattern": (
            r"(?i)"
            r"\b("
            r"CONFIG_PATH|"
            r"SCHEDULER_PATH|"
            r"TOKEN_PATH|"
            r"ENV_PATH"
            r")\b"
            r"\s*=\s*"
            r"[\"'][^\"']+[\"']"
        ),
        "category": "EXTRACT",
        "reason": "Operational path is hardcoded in production code.",
    },
    {
        "role": "PRODUCTION",
        "pattern": (
            r"(?i)"
            r"\b("
            r"API_KEY|"
            r"SECRET_KEY|"
            r"PASSWORD|"
            r"ACCESS_TOKEN"
            r")\b"
            r"\s*=\s*"
            r"[\"'][^\"']+[\"']"
        ),
        "category": "SECRET",
        "reason": "Potential secret is hardcoded in production code.",
    },
]