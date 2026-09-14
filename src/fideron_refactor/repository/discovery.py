import subprocess
from pathlib import Path

IGNORED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".7z",
    ".jar",
    ".class",
    ".pyc",
    ".pyo",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".lock",
}

IGNORED_PATH_FRAGMENTS = {
    "/.git/",
    "/.venv/",
    "/venv/",
    "/node_modules/",
    "/target/",
    "/dist/",
    "/build/",
    "/coverage/",
    "/.idea/",
    "/.vscode/",
    "/__pycache__/",
}


def discover_repository_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )

    files = []

    for relative_path in result.stdout.splitlines():
        normalised = "/" + relative_path.replace("\\", "/") + "/"

        if any(
            fragment in normalised
            for fragment in IGNORED_PATH_FRAGMENTS
        ):
            continue

        if Path(relative_path).suffix.lower() in IGNORED_EXTENSIONS:
            continue

        files.append(relative_path)

    return files