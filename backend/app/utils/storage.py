from __future__ import annotations

import mimetypes
import os
from io import BytesIO
from typing import Optional

from mutagen import File as MutagenFile
from ..schemas.storage import FileMetadata


def is_audio_file(path: str) -> bool:
    mime, _ = mimetypes.guess_type(path)
    if mime is None:
        return False
    return mime.startswith("audio/")


def _extract_basic_metadata(path: str, data: bytes) -> FileMetadata:
    # Try to determine format from extension
    fmt = os.path.splitext(path)[1].lstrip(".") or None
    duration = None
    title = None
    author = None
    cover = None

    try:
        mp = MutagenFile(BytesIO(data), easy=True)
        if mp is not None:
            if isinstance(mp, MutagenFile):
                duration = getattr(mp.info, "length", None)
                artist = mp.get("artist", []) or mp.get("ARTIST", [])
                if artist:
                    author = artist[0]
                title_list = mp.get("title", []) or mp.get("TITLE", [])
                if title_list:
                    title = title_list[0]
            # Best-effort: try cover from tags if present
            # Some formats expose pictures via ID3
    except Exception:
        pass

    return FileMetadata(title=title, author=author, duration=duration, format=fmt, cover=cover)


def extract_metadata_from_bytes(data: bytes, path: str) -> FileMetadata:
    """Public helper to extract metadata from audio bytes."""
    return _extract_basic_metadata(path, data)
