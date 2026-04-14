from __future__ import annotations

from typing import Dict

from fastapi import Depends, HTTPException, status

from ..core.security import oauth2_scheme, get_current_user as _get_current_user


async def get_current_user(current_user: Dict = Depends(_get_current_user)) -> Dict:
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return current_user


async def get_current_active_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    if not current_user.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


async def get_current_admin_user(current_user: Dict = Depends(get_current_active_user)) -> Dict:
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return current_user


# Alias for backward compatibility
get_current_admin = get_current_admin_user
