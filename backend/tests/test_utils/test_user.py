"""User utility module unit tests."""

import pytest
from backend.app.utils.user import (
    hash_password,
    verify_password,
    is_password_strong,
    is_username_email_unique,
)


class TestHashPassword:
    def test_hash_password_returns_string(self):
        result = hash_password("testpassword123")
        assert isinstance(result, str)

    def test_hash_password_produces_bcrypt_hash(self):
        result = hash_password("testpassword123")
        assert result.startswith("$2")

    def test_hash_password_different_each_time(self):
        h1 = hash_password("samepassword")
        h2 = hash_password("samepassword")
        assert h1 != h2

    def test_hash_password_empty_string(self):
        result = hash_password("")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_hash_password_long_password(self):
        long_pw = "a" * 100
        result = hash_password(long_pw)
        assert isinstance(result, str)


class TestVerifyPassword:
    def test_verify_correct_password(self):
        pw = "correctpassword123"
        hashed = hash_password(pw)
        assert verify_password(pw, hashed) is True

    def test_verify_wrong_password(self):
        hashed = hash_password("correctpassword123")
        assert verify_password("wrongpassword", hashed) is False

    def test_verify_empty_password(self):
        hashed = hash_password("somepassword")
        assert verify_password("", hashed) is False

    def test_verify_invalid_hash(self):
        assert verify_password("password", "not_a_valid_hash") is False

    def test_verify_empty_hash(self):
        assert verify_password("password", "") is False

    def test_verify_case_sensitive(self):
        hashed = hash_password("Password123")
        assert verify_password("password123", hashed) is False


class TestIsPasswordStrong:
    def test_strong_password(self):
        assert is_password_strong("StrongPw1") is True

    def test_strong_password_long(self):
        assert is_password_strong("MyStr0ngP@ssw0rd!") is True

    def test_too_short(self):
        assert is_password_strong("Ab1") is False

    def test_exactly_7_chars(self):
        assert is_password_strong("Abcdef1") is False

    def test_exactly_8_chars_strong(self):
        assert is_password_strong("Abcdefg1") is True

    def test_no_uppercase(self):
        assert is_password_strong("strongpass1") is False

    def test_no_lowercase(self):
        assert is_password_strong("STRONGPASS1") is False

    def test_no_digit(self):
        assert is_password_strong("StrongPass") is False

    def test_empty_password(self):
        assert is_password_strong("") is False

    def test_spaces_only(self):
        assert is_password_strong("        ") is False

    def test_special_chars_with_requirements(self):
        assert is_password_strong("Str0ng!@#") is True


class TestIsUsernameEmailUnique:
    def test_unique_username_and_email(self):
        existing = [
            {"username": "alice", "email": "alice@example.com"},
            {"username": "bob", "email": "bob@example.com"},
        ]
        assert is_username_email_unique("charlie", "charlie@example.com", existing) is True

    def test_duplicate_username(self):
        existing = [
            {"username": "alice", "email": "alice@example.com"},
        ]
        assert is_username_email_unique("alice", "new@example.com", existing) is False

    def test_duplicate_email(self):
        existing = [
            {"username": "alice", "email": "alice@example.com"},
        ]
        assert is_username_email_unique("bob", "alice@example.com", existing) is False

    def test_empty_existing_users(self):
        assert is_username_email_unique("newuser", "new@example.com", []) is True

    def test_multiple_existing_no_match(self):
        existing = [
            {"username": "user1", "email": "user1@example.com"},
            {"username": "user2", "email": "user2@example.com"},
        ]
        assert is_username_email_unique("user3", "user3@example.com", existing) is True

    def test_case_sensitive_username(self):
        existing = [
            {"username": "Alice", "email": "alice@example.com"},
        ]
        assert is_username_email_unique("alice", "new@example.com", existing) is True

    def test_case_sensitive_email(self):
        existing = [
            {"username": "alice", "email": "Alice@example.com"},
        ]
        assert is_username_email_unique("bob", "alice@example.com", existing) is True
