def create_playback(**kwargs):
    playback = {
        "id": kwargs.get("id", 1),
        "user_id": kwargs.get("user_id", 1),
        "content_id": kwargs.get("content_id", 1),
        "started_at": kwargs.get("started_at", "2026-01-01T00:00:00"),
        "duration": kwargs.get("duration", 0),
        "status": kwargs.get("status", "playing"),
    }
    playback.update(kwargs)
    return playback
