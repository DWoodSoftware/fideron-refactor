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


def discover_repository_files(
    ignore_paths: list[str] | None = None,
) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )

    ignore_paths = ignore_paths or []

    normalised_ignore_paths = [
        ignore_path.replace("\\", "/")
        .removeprefix("./")
        .rstrip("/")
        for ignore_path in ignore_paths
    ]

    files = []

    for relative_path in result.stdout.splitlines():
        normalised = "/" + relative_path.replace("\\", "/") + "/"

        if any(
            fragment in normalised
            for fragment in IGNORED_PATH_FRAGMENTS
        ):
            continue

        if any(
            relative_path.replace("\\", "/") == ignore_path
            or relative_path.replace("\\", "/").startswith(
                ignore_path + "/"
            )
            for ignore_path in normalised_ignore_paths
        ):
            continue

        if Path(relative_path).suffix.lower() in IGNORED_EXTENSIONS:
            continue

        files.append(relative_path)

    return files