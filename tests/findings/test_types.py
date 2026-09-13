import pytest

from fideron_refactor.findings.types import (
    FINDING_TYPES,
    classify_finding_type,
)


@pytest.mark.parametrize(
    ("value", "expected_type"),
    [
        ('service_url: "http://localhost:8080"', "localhost"),
        ('service_url: "http://127.0.0.1:8080"', "localhost"),
        ("retries: 3", "retry"),
        ("retry: true", "retry"),
        ("some_other_setting: true", "operational"),
    ],
)
def test_classify_finding_type(value, expected_type):
    assert classify_finding_type(value) == expected_type


def test_finding_types_have_unique_names():
    names = [
        finding_type["name"]
        for finding_type in FINDING_TYPES
    ]

    assert len(names) == len(set(names))