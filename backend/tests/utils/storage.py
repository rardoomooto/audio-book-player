"""Fake storage utilities for tests."""

class FakeStorage:
    def __init__(self, base_path: str = "/tmp/storage"):
        self.base_path = base_path

    def list(self):  # pragma: no cover - placeholder
        return []
