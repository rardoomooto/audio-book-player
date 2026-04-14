"""Folder service unit tests."""

import pytest
from backend.app.services import folder as folder_service


@pytest.fixture(autouse=True)
def reset_folders():
    """Reset folder service state before each test."""
    folder_service.folders.clear()
    folder_service.folders[1] = {
        "id": 1,
        "name": "Root",
        "parent_id": None,
        "created_at": "2026-01-01T00:00:00",
        "updated_at": "2026-01-01T00:00:00",
    }
    folder_service._next_id = 2
    yield
    folder_service.folders.clear()
    folder_service.folders[1] = {
        "id": 1,
        "name": "Root",
        "parent_id": None,
        "created_at": "2026-01-01T00:00:00",
        "updated_at": "2026-01-01T00:00:00",
    }
    folder_service._next_id = 2


class TestListFolders:
    def test_list_folders_returns_all(self):
        result = folder_service.list_folders()
        assert len(result) == 1
        assert result[0]["name"] == "Root"

    def test_list_folders_empty(self):
        folder_service.folders.clear()
        result = folder_service.list_folders()
        assert result == []

    def test_list_folders_after_create(self):
        folder_service.create_folder({"name": "Music", "parent_id": 1})
        result = folder_service.list_folders()
        assert len(result) == 2


class TestGetFolder:
    def test_get_existing_folder(self):
        result = folder_service.get_folder(1)
        assert result is not None
        assert result["name"] == "Root"

    def test_get_nonexistent_folder(self):
        result = folder_service.get_folder(999)
        assert result is None

    def test_get_folder_returns_dict(self):
        result = folder_service.get_folder(1)
        assert isinstance(result, dict)
        assert "id" in result
        assert "name" in result
        assert "parent_id" in result


class TestCreateFolder:
    def test_create_folder_with_name(self):
        result = folder_service.create_folder({"name": "Music"})
        assert result["id"] == 2
        assert result["name"] == "Music"
        assert result["parent_id"] is None
        assert "created_at" in result
        assert "updated_at" in result

    def test_create_folder_with_parent(self):
        result = folder_service.create_folder({"name": "Sub", "parent_id": 1})
        assert result["parent_id"] == 1

    def test_create_folder_increments_id(self):
        f1 = folder_service.create_folder({"name": "A"})
        f2 = folder_service.create_folder({"name": "B"})
        assert f1["id"] == 2
        assert f2["id"] == 3

    def test_create_folder_without_name(self):
        result = folder_service.create_folder({})
        assert result["name"] is None

    def test_create_folder_stored_in_global(self):
        folder_service.create_folder({"name": "Test"})
        assert 2 in folder_service.folders

    def test_create_multiple_folders(self):
        for i in range(5):
            folder_service.create_folder({"name": f"Folder{i}"})
        assert len(folder_service.list_folders()) == 6


class TestUpdateFolder:
    def test_update_folder_name(self):
        result = folder_service.update_folder(1, {"name": "NewRoot"})
        assert result is not None
        assert result["name"] == "NewRoot"

    def test_update_folder_parent(self):
        folder_service.create_folder({"name": "Child"})
        result = folder_service.update_folder(2, {"parent_id": 1})
        assert result["parent_id"] == 1

    def test_update_nonexistent_folder(self):
        result = folder_service.update_folder(999, {"name": "X"})
        assert result is None

    def test_update_folder_updates_timestamp(self):
        import datetime
        before = folder_service.get_folder(1)["updated_at"]
        folder_service.update_folder(1, {"name": "Updated"})
        after = folder_service.get_folder(1)["updated_at"]
        assert after >= before

    def test_update_folder_partial(self):
        folder_service.create_folder({"name": "Test", "parent_id": None})
        result = folder_service.update_folder(2, {"name": "Renamed"})
        assert result["name"] == "Renamed"
        assert result["parent_id"] is None

    def test_update_with_unknown_field(self):
        result = folder_service.update_folder(1, {"unknown_field": "value"})
        assert result is not None
        assert result["name"] == "Root"
        assert "unknown_field" not in result


class TestDeleteFolder:
    def test_delete_existing_folder(self):
        result = folder_service.delete_folder(1)
        assert result is True
        assert 1 not in folder_service.folders

    def test_delete_nonexistent_folder(self):
        result = folder_service.delete_folder(999)
        assert result is False

    def test_delete_then_get_returns_none(self):
        folder_service.delete_folder(1)
        assert folder_service.get_folder(1) is None

    def test_delete_multiple_folders(self):
        folder_service.create_folder({"name": "A"})
        folder_service.create_folder({"name": "B"})
        folder_service.delete_folder(1)
        folder_service.delete_folder(2)
        assert len(folder_service.list_folders()) == 1


class TestFolderContents:
    def test_folder_contents_returns_empty_list(self):
        result = folder_service.folder_contents(1)
        assert result == []

    def test_folder_contents_nonexistent(self):
        result = folder_service.folder_contents(999)
        assert result == []

    def test_folder_contents_always_empty(self):
        folder_service.create_folder({"name": "Test"})
        result = folder_service.folder_contents(2)
        assert result == []


class TestNow:
    def test_now_returns_iso_string(self):
        result = folder_service._now()
        assert isinstance(result, str)
        assert "T" in result
