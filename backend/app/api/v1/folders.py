from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

router = APIRouter()


class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class FolderUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class Folder(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None


from ...services.folder import (
    list_folders,
    get_folder,
    create_folder,
    update_folder,
    delete_folder,
    folder_contents,
)
from .deps import get_current_user


@router.get("/")
def list_folders_route(current_user: dict = Depends(get_current_user)) -> List[Folder]:
    # Admins can see all; users can see public folders (no access check in this simple demo)
    return [Folder(**f) for f in list_folders()]


@router.get("/{folder_id}")
def get_folder_route(folder_id: int, current_user: dict = Depends(get_current_user)) -> Folder:
    f = get_folder(folder_id)
    if not f:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    return Folder(**f)


@router.post("/")
def create_folder_route(folder: FolderCreate, current_user: dict = Depends(get_current_user)) -> Folder:
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    f = create_folder(folder.dict())
    return Folder(**f)


@router.put("/{folder_id}")
def update_folder_route(folder_id: int, folder: FolderUpdate, current_user: dict = Depends(get_current_user)) -> Folder:
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    f = update_folder(folder_id, folder.dict(exclude_unset=True))
    if not f:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    return Folder(**f)


@router.delete("/{folder_id}")
def delete_folder_route(folder_id: int, current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    ok = delete_folder(folder_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    return {"detail": "Deleted"}


@router.get("/{folder_id}/contents")
def folder_contents_route(folder_id: int, current_user: dict = Depends(get_current_user)) -> List[dict]:
    f = get_folder(folder_id)
    if not f:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    # In a real app, integrate with Content service to list contents in the folder
    return folder_contents(folder_id)
