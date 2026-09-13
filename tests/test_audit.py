from fideron_refactor.audit import audit_repository


def test_audit_repository_detects_localhost_literal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    source_file = tmp_path / "example.py"
    source_file.write_text(
        'API_URL = "http://localhost:8080"\n',
        encoding="utf-8",
    )

    findings = audit_repository()

    assert any(
        finding["category"] == "ALREADY_CONFIGURED"
        and "localhost" in finding["value"].lower()
        for finding in findings
    )