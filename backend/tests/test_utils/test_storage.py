"""Storage utility module unit tests."""

import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from backend.app.utils.storage import is_audio_file, extract_metadata_from_bytes
from backend.app.schemas.storage import FileMetadata


class TestIsAudioFile:
    def test_mp3_file(self):
        assert is_audio_file("song.mp3") is True

    def test_m4a_file(self):
        assert is_audio_file("song.m4a") is True

    def test_flac_file(self):
        assert is_audio_file("song.flac") is True

    def test_ogg_file(self):
        assert is_audio_file("song.ogg") is True

    def test_wav_file(self):
        assert is_audio_file("song.wav") is True

    def test_txt_file(self):
        assert is_audio_file("document.txt") is False

    def test_jpg_file(self):
        assert is_audio_file("image.jpg") is False

    def test_pdf_file(self):
        assert is_audio_file("document.pdf") is False

    def test_path_with_directory(self):
        assert is_audio_file("/path/to/song.mp3") is True

    def test_empty_string(self):
        assert is_audio_file("") is False

    def test_no_extension(self):
        assert is_audio_file("filename") is False

    def test_uppercase_extension(self):
        assert is_audio_file("song.MP3") is True


class TestExtractMetadataFromBytes:
    def test_returns_file_metadata(self):
        fake_data = b"fake audio data for testing"
        result = extract_metadata_from_bytes(fake_data, "test.mp3")
        assert isinstance(result, FileMetadata)

    def test_format_from_extension(self):
        fake_data = b"fake audio data"
        result = extract_metadata_from_bytes(fake_data, "test.mp3")
        assert result.format == "mp3"

    def test_format_flac(self):
        fake_data = b"fake flac data"
        result = extract_metadata_from_bytes(fake_data, "test.flac")
        assert result.format == "flac"

    def test_format_m4a(self):
        fake_data = b"fake m4a data"
        result = extract_metadata_from_bytes(fake_data, "test.m4a")
        assert result.format == "m4a"

    def test_format_ogg(self):
        fake_data = b"fake ogg data"
        result = extract_metadata_from_bytes(fake_data, "test.ogg")
        assert result.format == "ogg"

    def test_no_extension(self):
        fake_data = b"fake data"
        result = extract_metadata_from_bytes(fake_data, "noext")
        assert result.format is None

    def test_defaults_are_none(self):
        fake_data = b"invalid audio data"
        result = extract_metadata_from_bytes(fake_data, "test.mp3")
        assert result.title is None
        assert result.author is None
        assert result.duration is None
        assert result.cover is None

    def test_empty_data(self):
        result = extract_metadata_from_bytes(b"", "test.mp3")
        assert isinstance(result, FileMetadata)
        assert result.format == "mp3"

    def test_path_with_subdirectory(self):
        fake_data = b"fake data"
        result = extract_metadata_from_bytes(fake_data, "/nas/audiobooks/chapter1.mp3")
        assert result.format == "mp3"

    @patch("backend.app.utils.storage.MutagenFile")
    def test_mutagen_returns_none(self, mock_mutagen):
        mock_mutagen.return_value = None
        fake_data = b"fake data"
        result = extract_metadata_from_bytes(fake_data, "test.mp3")
        assert isinstance(result, FileMetadata)
        assert result.title is None
        assert result.author is None

    @patch("backend.app.utils.storage.MutagenFile")
    def test_mutagen_raises_exception(self, mock_mutagen):
        mock_mutagen.side_effect = Exception("Invalid file")
        fake_data = b"fake data"
        result = extract_metadata_from_bytes(fake_data, "test.mp3")
        assert isinstance(result, FileMetadata)
        assert result.format == "mp3"

    @patch("backend.app.utils.storage.MutagenFile")
    def test_mutagen_returns_valid_info(self, mock_mutagen):
        mock_info = MagicMock()
        mock_info.length = 180.5
        mock_mp = MagicMock()
        mock_mp.info = mock_info
        mock_mp.get.return_value = None
        mock_mutagen.return_value = mock_mp

        fake_data = b"fake mp3 data"
        result = extract_metadata_from_bytes(fake_data, "test.mp3")

        assert result.duration == 180.5
        assert result.format == "mp3"

    @patch("backend.app.utils.storage.MutagenFile")
    def test_mutagen_returns_artist(self, mock_mutagen):
        mock_info = MagicMock()
        mock_info.length = 120.0
        mock_mp = MagicMock()
        mock_mp.info = mock_info

        def mock_get(key, default=None):
            mapping = {
                "artist": ["Test Artist"],
                "ARTIST": [],
                "title": ["Test Title"],
                "TITLE": [],
            }
            return mapping.get(key, default)

        mock_mp.get.side_effect = mock_get
        mock_mutagen.return_value = mock_mp

        fake_data = b"fake mp3 data"
        result = extract_metadata_from_bytes(fake_data, "test.mp3")

        assert result.author == "Test Artist"
        assert result.title == "Test Title"
        assert result.duration == 120.0
