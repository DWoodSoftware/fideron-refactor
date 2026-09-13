import re


FINDING_TYPES = [
    {
        "name": "localhost",
        "patterns": [
            r"localhost",
            r"127\.0\.0\.1",
        ],
    },
    {
        "name": "retry",
        "patterns": [
            r"\bretries?\b",
            r"\bretry\b",
        ],
    },
    {
        "name": "delay",
        "patterns": [
            r"\btime\.sleep\s*\(",
            r"\bretry_delay\b",
            r"\bbackoff_delay\b",
        ],
    },
    {
        "name": "timeout",
        "patterns": [
            r"\btimeout\b",
            r"\brequest_timeout\b",
        ],
    },
    {
        "name": "interval",
        "patterns": [
            r"\binterval\b",
            r"\bpoll_interval\b",
        ],
    },
    {
        "name": "duration",
        "patterns": [
            r"\btimedelta\s*\(",
            r"\bttl\b",
        ],
    },
]


def classify_finding_type(value: str) -> str:
    for finding_type in FINDING_TYPES:
        for pattern in finding_type["patterns"]:
            if re.search(
                pattern,
                value,
                re.IGNORECASE,
            ):
                return finding_type["name"]

    return "operational"