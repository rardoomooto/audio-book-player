from typing import Dict, Optional, List
from datetime import datetime

# In-memory folders store (demo purposes)
folders: Dict[int, Dict] = {
    1: {"id": 1, "name": "Root", "parent_id": None, "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()},
}
_next_id = 2


def _now() -> str:
    return datetime.utcnow().isoformat()


def list_folders() -> List[Dict]:
    return list(folders.values())


def get_folder(folder_id: int) -> Optional[Dict]:
    return folders.get(folder_id)


def create_folder(data: Dict) -> Dict:
    global _next_id
    new = {
        "id": _next_id,
        "name": data.get("name"),
        "parent_id": data.get("parent_id"),
        "created_at": _now(),
        "updated_at": _now(),
    }
    folders[_next_id] = new
    _next_id += 1
    return new


def update_folder(folder_id: int, data: Dict) -> Optional[Dict]:
    if folder_id not in folders:
        return None
    f = folders[folder_id]
    if "name" in data:
        f["name"] = data["name"]
    if "parent_id" in data:
        f["parent_id"] = data["parent_id"]
    f["updated_at"] = _now()
    folders[folder_id] = f
    return f


def delete_folder(folder_id: int) -> bool:
    if folder_id in folders:
        del folders[folder_id]
        return True
    return False


def folder_contents(folder_id: int):
    # Placeholder: would connect to contents service to fetch items
    return []
