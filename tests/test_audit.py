from fideron_refactor.audit import audit_repository


def test_audit_repository_detects_localhost_literal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    source_file = tmp_path / "config.yml"
    source_file.write_text(
        'API_URL = "http://localhost:8080"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.discover_repository_files",
        lambda: ["config.yml"],
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

    tracked_file = tmp_path / "config.yml"
    tracked_file.write_text(
        'API_URL = "http://localhost:8080"\n',
        encoding="utf-8",
    )

    ignored_file = tmp_path / "ignored.yml"
    ignored_file.write_text(
        'API_URL = "http://localhost:9999"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.discover_repository_files",
        lambda: ["config.yml"],
    )

    findings = audit_repository()

    assert any(
        finding["path"] == "config.yml"
        for finding in findings
    )

    assert not any(
        finding["path"] == "ignored.yml"
        for finding in findings
    )

def test_audit_repository_classifies_operational_config_values(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_file = tmp_path / "config.yml"
    config_file.write_text(
        'service_url: "http://localhost:8080"\n',
        encoding="utf-8",
    )

    production_file = tmp_path / "service.py"
    production_file.write_text(
        'API_URL = "http://localhost:9000"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.discover_repository_files",
        lambda: ["config.yml", "service.py"],
    )

    findings = audit_repository()

    configured_findings = [
        finding
        for finding in findings
        if finding["category"] == "ALREADY_CONFIGURED"
    ]

    assert any(
        finding["path"] == "config.yml"
        and "localhost" in finding["value"].lower()
        for finding in configured_findings
    )

    assert not any(
        finding["path"] == "service.py"
        for finding in configured_findings
    )

def test_audit_repository_reports_config_finding_line_and_value(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_file = tmp_path / "config.yml"
    config_file.write_text(
        (
            'service_name: "example"\n'
            'service_url: "http://localhost:8080"\n'
            'retries: 3\n'
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.discover_repository_files",
        lambda: ["config.yml"],
    )

    findings = audit_repository()

    localhost_finding = next(
        finding
        for finding in findings
        if "localhost" in finding["value"].lower()
    )

    assert localhost_finding["path"] == "config.yml"
    assert localhost_finding["line"] == 2
    assert (
        localhost_finding["value"]
        == 'service_url: "http://localhost:8080"'
    )
