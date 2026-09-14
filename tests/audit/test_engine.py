import pytest

from fideron_refactor.audit import audit_repository


def test_audit_repository_detects_localhost_literal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    source_file = tmp_path / "config.yml"
    source_file.write_text(
        'API_URL = "http://localhost:8080"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: ["config.yml"],
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
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: ["config.yml"],
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
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: ["config.yml", "service.py"],
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
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: ["config.yml"],
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

def test_audit_repository_classifies_localhost_config_finding_type(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_file = tmp_path / "config.yml"
    config_file.write_text(
        'service_url: "http://localhost:8080"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: ["config.yml"],
    )

    findings = audit_repository()

    finding = next(
        finding
        for finding in findings
        if "localhost" in finding["value"].lower()
    )

    assert finding["category"] == "ALREADY_CONFIGURED"
    assert finding["type"] == "localhost"

def test_audit_repository_marks_production_localhost_as_extract(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    source_file = tmp_path / "service.py"
    source_file.write_text(
        'SERVICE_URL = "http://localhost:8080"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: ["service.py"],
    )

    findings = audit_repository()

    assert len(findings) == 1

    finding = findings[0]

    assert finding["category"] == "EXTRACT"
    assert finding["type"] == "localhost"
    assert finding["path"] == "service.py"
    assert finding["line"] == 1
    assert (
        finding["value"]
        == 'SERVICE_URL = "http://localhost:8080"'
    )

def test_audit_repository_marks_hardcoded_sleep_as_extract(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    source_file = tmp_path / "worker.py"
    source_file.write_text(
        "time.sleep(5)\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: ["worker.py"],
    )

    findings = audit_repository()

    assert len(findings) == 1

    finding = findings[0]

    assert finding["category"] == "EXTRACT"
    assert finding["path"] == "worker.py"
    assert finding["line"] == 1
    assert finding["value"] == "time.sleep(5)"
    assert finding["type"] == "delay"


@pytest.mark.parametrize(
    ("source", "expected_type"),
    [
        ("REQUEST_TIMEOUT = 30", "timeout"),
        ("POLL_INTERVAL = 15", "interval"),
        ("RETRY_DELAY = 5", "delay"),
        ("BACKOFF_DELAY = 10", "delay"),
        ("CACHE_TTL = timedelta(seconds=60)", "duration"),
    ],
)
def test_audit_repository_extracts_hardcoded_operational_timing_values(
    tmp_path,
    monkeypatch,
    source,
    expected_type,
):
    monkeypatch.chdir(tmp_path)

    source_file = tmp_path / "worker.py"
    source_file.write_text(
        f"{source}\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: ["worker.py"],
    )

    findings = audit_repository()

    assert len(findings) == 1

    finding = findings[0]

    assert finding["category"] == "EXTRACT"
    assert finding["type"] == expected_type
    assert finding["path"] == "worker.py"
    assert finding["line"] == 1
    assert finding["value"] == source

@pytest.mark.parametrize(
    "source",
    [
        'CONFIG_PATH = "./config.yaml"',
        'SCHEDULER_PATH = "./scheduler.json"',
        'TOKEN_PATH = "./token.json"',
        'ENV_PATH = ".env"',
    ],
)
def test_audit_repository_extracts_hardcoded_operational_paths(
    tmp_path,
    monkeypatch,
    source,
):
    monkeypatch.chdir(tmp_path)

    source_file = tmp_path / "worker.py"
    source_file.write_text(
        f"{source}\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: ["worker.py"],
    )

    findings = audit_repository()

    assert len(findings) == 1

    finding = findings[0]

    assert finding["category"] == "EXTRACT"
    assert finding["type"] == "path"
    assert finding["path"] == "worker.py"
    assert finding["line"] == 1
    assert finding["value"] == source

@pytest.mark.parametrize(
    "source",
    [
        'API_KEY = "super-secret-key"',
        'SECRET_KEY = "super-secret-key"',
        'PASSWORD = "hunter2"',
        'ACCESS_TOKEN = "abc123token"',
    ],
)
def test_audit_repository_detects_hardcoded_secrets(
    tmp_path,
    monkeypatch,
    source,
):
    monkeypatch.chdir(tmp_path)

    source_file = tmp_path / "service.py"
    source_file.write_text(
        f"{source}\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: ["service.py"],
    )

    findings = audit_repository()

    assert len(findings) == 1

    finding = findings[0]

    assert finding["category"] == "SECRET"
    assert finding["path"] == "service.py"
    assert finding["line"] == 1
    assert finding["value"] == source

def test_audit_repository_respects_configured_ignore_paths(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    ignored_dir = tmp_path / "ignored"
    ignored_dir.mkdir()

    ignored_file = ignored_dir / "service.py"
    ignored_file.write_text(
        'SERVICE_URL = "http://localhost:8080"\n',
        encoding="utf-8",
    )

    included_file = tmp_path / "service.py"
    included_file.write_text(
        'SERVICE_URL = "http://localhost:9000"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "fideron_refactor.audit.engine.discover_repository_files",
        lambda ignore_paths=None: (
            ["service.py"]
            if ignore_paths == ["ignored/"]
            else ["service.py", "ignored/service.py"]
        ),
    )

    findings = audit_repository(
        ignore_paths=["ignored/"],
    )

    assert len(findings) == 1
    assert findings[0]["path"] == "service.py"