"""Small user-side JSON stores. No manuscript scanning, history, or cloud state."""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    if not isinstance(value, bytes):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def private_path(path):
    path = Path(path).resolve()
    skills = Path(__file__).resolve().parents[2]
    if path == skills or skills in path.parents:
        raise ValueError("User state must be outside installed skills.")
    # A source checkout contains private material neither in tracked files nor ignored outputs.
    repo = skills.parent
    if (repo / ".git").exists() and (path == repo or repo in path.parents):
        raise ValueError("User state must be outside the public skill checkout.")
    return path


def read_json(path, default=None):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else default


def write_json(path, value):
    path = private_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".edu-write-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def locked(path):
    """Fail clearly on concurrent mutation; never leave text-bearing backup journals."""
    path = private_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + ".lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError("Store is busy. Check its writer before removing a stale .lock.")
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink()
