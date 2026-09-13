from fideron_refactor.audit import audit_repository


def test_audit_repository_detects_localhost_literal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    source_file = tmp_path / "example.py"
    source_file.write_text(
        'API_URL = "http://localhost:8080"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.discover_repository_files",
        lambda: ["example.py"],
    )

    findings = audit_repository()

    assert any(
        finding["category"] == "ALREADY_CONFIGURED"
        and "localhost" in finding["value"].lower()
        for finding in findings
    )

def test_audit_repository_only_scans_discovered_repository_files(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    tracked_file = tmp_path / "tracked.py"
    tracked_file.write_text(
        'API_URL = "http://localhost:8080"\n',
        encoding="utf-8",
    )

    ignored_file = tmp_path / "ignored.py"
    ignored_file.write_text(
        'API_URL = "http://localhost:9999"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.discover_repository_files",
        lambda: ["tracked.py"],
    )

    findings = audit_repository()

    assert any(
        finding["path"] == "tracked.py"
        for finding in findings
    )

    assert not any(
        finding["path"] == "ignored.py"
        for finding in findings
    )