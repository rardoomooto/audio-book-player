"""Helpers for authentication in tests (mock or fixture-based)."""

def get_auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
