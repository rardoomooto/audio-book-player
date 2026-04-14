def create_content(**kwargs):
    content = {
        "id": kwargs.get("id", 1),
        "title": kwargs.get("title", "Test Content"),
        "duration": kwargs.get("duration", 3600),
        "path": kwargs.get("path", "/path/to/content.mp3"),
    }
    content.update(kwargs)
    return content
