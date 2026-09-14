import subprocess

from fideron_refactor.repository import discover_repository_files


def test_discover_repository_files_returns_tracked_files_and_skips_ignored_paths(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    subprocess.run(["git", "init"], check=True, capture_output=True)

    source_file = tmp_path / "src" / "app.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("print('hello')\n", encoding="utf-8")

    config_file = tmp_path / "config.json"
    config_file.write_text('{"enabled": true}\n', encoding="utf-8")

    ignored_build_file = tmp_path / "build" / "generated.py"
    ignored_build_file.parent.mkdir(parents=True)
    ignored_build_file.write_text("print('generated')\n", encoding="utf-8")

    ignored_binary_file = tmp_path / "assets" / "logo.png"
    ignored_binary_file.parent.mkdir(parents=True)
    ignored_binary_file.write_bytes(b"not-really-a-png")

    subprocess.run(
        [
            "git",
            "add",
            "src/app.py",
            "config.json",
            "build/generated.py",
            "assets/logo.png",
        ],
        check=True,
        capture_output=True,
    )

    files = discover_repository_files()

    assert "src/app.py" in files
    assert "config.json" in files
    assert "build/generated.py" not in files
    assert "assets/logo.png" not in files

def test_discover_repository_files_excludes_configured_ignore_paths(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    subprocess.run(
        ["git", "init"],
        check=True,
        capture_output=True,
    )

    source_dir = tmp_path / "src"
    source_dir.mkdir()
    source_file = source_dir / "service.py"
    source_file.write_text(
        "print('production')\n",
        encoding="utf-8",
    )

    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    test_file = tests_dir / "test_service.py"
    test_file.write_text(
        "print('test')\n",
        encoding="utf-8",
    )

    subprocess.run(
        ["git", "add", "."],
        check=True,
        capture_output=True,
    )

    files = discover_repository_files(
        ignore_paths=["tests/"],
    )

    assert "src/service.py" in files
    assert "tests/test_service.py" not in files