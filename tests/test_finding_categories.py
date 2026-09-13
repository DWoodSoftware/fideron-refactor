from fideron_refactor.finding_categories import FINDING_CATEGORIES


def test_finding_category_registry_defines_supported_categories():
    assert set(FINDING_CATEGORIES) == {
        "SECRET",
        "EXTRACT",
        "REVIEW",
        "ALREADY_CONFIGURED",
        "KEEP",
    }