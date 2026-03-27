from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class PlaybackState(str, Enum):
    idle = "idle"
    playing = "playing"
    paused = "paused"
    stopped = "stopped"


class Playback(BaseModel):
    id: int
    user_id: int
    content_id: int
    state: PlaybackState
    position_seconds: int
    started_at: datetime
    updated_at: datetime
