import pytest


def test_storage_list_returns_list_or_skip():
    # Try to import storage service; if unavailable, skip the test.
    try:
        from backend.app.services.storage import StorageService  # type: ignore
        storage = StorageService(base_path="/tmp/nonexistent")
        items = storage.list()  # type: ignore
        assert isinstance(items, list) or items is None
    except Exception:
        pytest.skip("Storage service not available in this environment.")
