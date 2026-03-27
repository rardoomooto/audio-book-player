"""Simple in-memory token blacklist for JWT logout/rotation.

This module tracks blacklisted token identifiers (jti) with their expiry.
For a lightweight setup (no Redis), this suffices. Entries expire when their
expiry time passes to avoid unbounded growth.
"""

import time
from typing import Dict

_blacklist: Dict[str, int] = {}


def blacklist_token(jti: str, exp_ts: int) -> None:
    """Register a token's JTI as blacklisted until exp_ts (epoch seconds)."""
    _blacklist[jti] = int(exp_ts)


def is_token_blacklisted(jti: str) -> bool:
    """Return True if token is blacklisted and not yet expired; prune expired entries."""
    if jti not in _blacklist:
        return False
    now = int(time.time())
    exp_ts = _blacklist.get(jti, 0)
    if now >= exp_ts:
        # Token expired, remove from blacklist eagerly
        _blacklist.pop(jti, None)
        return False
    return True


def cleanup_expired() -> None:
    """Optional cleanup: remove any expired entries proactively."""
    now = int(time.time())
    for jti, exp_ts in list(_blacklist.items()):
        if now >= exp_ts:
            _blacklist.pop(jti, None)
