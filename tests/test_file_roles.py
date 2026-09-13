from fideron_refactor.audit import classify_file_role


def test_classify_file_role_identifies_test_files():
    assert classify_file_role("tests/test_worker.py") == "TEST"
    assert classify_file_role("test/example.py") == "TEST"
    assert classify_file_role("src/test_service.py") == "TEST"
    assert classify_file_role("test/domain/QuarterSpec.scala") == "TEST"


def test_classify_file_role_identifies_config_files():
    assert classify_file_role("conf/application.conf") == "CONFIG"
    assert classify_file_role("docker-compose.yml") == "CONFIG"
    assert classify_file_role("compose.yaml") == "CONFIG"
    assert classify_file_role("scheduler.json") == "CONFIG"
    assert classify_file_role("config.yml") == "CONFIG"
    assert classify_file_role(".env") == "CONFIG"
    assert classify_file_role(".env.local") == "CONFIG"


def test_classify_file_role_defaults_to_production():
    assert classify_file_role("src/service.py") == "PRODUCTION"
    assert classify_file_role("app/controllers/HealthController.scala") == "PRODUCTION"
    assert classify_file_role("frontend/src/App.tsx") == "PRODUCTION"