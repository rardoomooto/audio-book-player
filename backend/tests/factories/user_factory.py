def create_user(**kwargs):
    user = {
        "id": kwargs.get("id", 1),
        "username": kwargs.get("username", "testuser"),
        "email": kwargs.get("email", "test@example.com"),
        "is_active": kwargs.get("is_active", True),
        "roles": kwargs.get("roles", ["user"]),
    }
    user.update(kwargs)
    return user
