"""Helpers for locating, copying, and thumbnailing media files."""

from __future__ import annotations

import shutil
from collections.abc import Iterator
from pathlib import Path

import cv2
import numpy as np

from ..config import IMAGE_EXTS


def iter_images(root: Path) -> Iterator[Path]:
    """Yield image files under ``root`` (recursively), sorted for determinism.

    Only files whose suffix is in :data:`face_finder.config.IMAGE_EXTS` are
    returned. The comparison is case-insensitive.
    """
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            yield path


def copy_into(source: Path, dest_dir: Path) -> Path:
    """Copy ``source`` into ``dest_dir`` under its original name.

    Any existing file of the same name is overwritten. Returns the destination
    path.
    """
    target = dest_dir / source.name
    shutil.copy2(source, target)
    return target


def make_thumbnail(path: Path, max_side: int) -> bytes:
    """Return JPEG-encoded bytes of ``path`` scaled so its longest side <= ``max_side``.

    Reads the file as raw bytes (so non-ASCII names decode reliably) and never
    upscales. Raises ValueError if the file can't be decoded or re-encoded.
    """
    buffer = np.frombuffer(path.read_bytes(), dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not decode image: {path}")

    height, width = image.shape[:2]
    scale = max_side / max(height, width)
    if scale < 1:
        image = cv2.resize(
            image, (round(width * scale), round(height * scale)),
            interpolation=cv2.INTER_AREA,
        )

    ok, encoded = cv2.imencode(".jpg", image)
    if not ok:
        raise ValueError(f"Could not encode thumbnail: {path}")
    return encoded.tobytes()
