from pathlib import Path

def find_project_root(start: Path | None = None) -> Path | None:
    path = (start or Path(__file__)).resolve()
    for directory in [path.parent, *path.parents]:
        if (directory / ".git").exists():
            return directory
    return None

def find_dir(
    name: str,
    start: Path | None = None,
) -> Path:

    path = (start or Path(__file__)).resolve()
    for directory in [path.parent, *path.parents]:
        candidate = directory / name
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(f"Directory '{name}' not found.")
