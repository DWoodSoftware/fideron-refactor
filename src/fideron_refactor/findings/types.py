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