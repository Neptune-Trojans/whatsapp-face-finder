"""Utilities for working with archive files."""

from __future__ import annotations

import zipfile
from pathlib import Path


def extract_zip(zip_path: str | Path, dest_dir: str | Path | None = None) -> Path:
    """Extract a zip file and return the directory it was extracted into.

    Args:
        zip_path: Path to the .zip file.
        dest_dir: Directory to extract into. Defaults to a folder next to the
            zip file, named after the zip (without the .zip suffix).

    Returns:
        The directory the contents were extracted into.

    Raises:
        FileNotFoundError: If ``zip_path`` does not exist.
        zipfile.BadZipFile: If the file is not a valid zip archive.
    """
    zip_path = Path(zip_path)
    if not zip_path.is_file():
        raise FileNotFoundError(f"Zip file not found: {zip_path}")

    dest_dir = Path(dest_dir) if dest_dir is not None else zip_path.with_suffix("")
    dest_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(dest_dir)

    return dest_dir
