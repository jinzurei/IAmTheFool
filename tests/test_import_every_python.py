import importlib
import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Iterable


def is_excluded(path: Path) -> bool:
    parts = path.parts
    # Exclude tests directory, venvs, and git metadata
    if "tests" in parts:
        return True
    if ".git" in parts:
        return True
    if "__pycache__" in parts:
        return True
    return False


def collect_python_files(repo_root: Path) -> Iterable[Path]:
    py_files = list(repo_root.rglob("*.py"))
    return [p for p in py_files if not is_excluded(p) and "site-packages" not in str(p)]


def try_import(path: Path, repo_root: Path, idx: int):
    """Try to import a single file by module name, then by file location.

    Raises an exception with a helpful message on failure.
    """
    rel = path.relative_to(repo_root)
    module_name = str(rel.with_suffix("")).replace("/", ".").replace("\\", ".")

    # Attempt package-style import
    try:
        importlib.import_module(module_name)
        return
    except Exception:
        tb1 = traceback.format_exc()

    # Fallback: load by file location with unique name
    unique_name = f"smoke_{idx}_{module_name.replace('.', '_')}"
    try:
        spec = importlib.util.spec_from_file_location(unique_name, path)
        module = importlib.util.module_from_spec(spec)
        parent_pkg = module_name.rpartition(".")[0]
        module.__package__ = parent_pkg
        sys.modules[unique_name] = module
        spec.loader.exec_module(module)
        return
    except Exception:
        tb2 = traceback.format_exc()
        msg = (
            f"Failed to import {path} (module name '{module_name}').\n"
            "Package import error:\n"
            f"{tb1}\n"
            "File import error:\n"
            f"{tb2}"
        )
        raise ImportError(msg)


def pytest_generate_tests(metafunc):
    # Parametrize one test per python file for clear pytest reporting
    if "pyfile" in metafunc.fixturenames:
        repo_root = Path.cwd()
        sys.path.insert(0, str(repo_root))
        sys.path.insert(1, str(repo_root / "src"))
        files = sorted(collect_python_files(repo_root))
        ids = [str(p.relative_to(repo_root)) for p in files]
    params = list(zip(files, range(1, len(files) + 1)))
    metafunc.parametrize("pyfile,idx", params, ids=ids)


def test_import_file(pyfile: Path, idx: int):
    """Parametrized test: attempt to import the given python file.

    On failure, the raised ImportError will include both the package-style
    import traceback and the file-load traceback for easier debugging.
    """
    repo_root = Path.cwd()
    try:
        try_import(pyfile, repo_root, idx)
    except Exception as e:
        raise AssertionError(str(e))
