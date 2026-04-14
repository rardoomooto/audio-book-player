# API Documentation for AudioBook Player

This document describes the REST API exposed by the backend service. It mirrors the FastAPI OpenAPI schema generated at runtime.

Note: All examples assume the API is served at http://localhost:8000.

- Authentication
  - POST /api/v1/auth/login
    - Request: {"username": "alice@example.com", "password": "secret"}
    - Response: {"access_token": "...", "refresh_token": "...", "expires_in": 900}
  - POST /api/v1/auth/refresh
    - Request: {"refresh_token": "..."}
    - Response: {"access_token": "...", "expires_in": 900}
  - POST /api/v1/auth/logout
    - Request: none or Authorization header with token
    - Response: {"detail": "Logged out"}
  - GET /api/v1/auth/me
    - Response: {"username": "alice", "email": "alice@example.com", "is_active": true, "is_admin": true}

- User Management (admin)
  - GET /api/v1/users/
  - POST /api/v1/users/
  - GET /api/v1/users/{user_id}
  - PUT /api/v1/users/{user_id}
  - DELETE /api/v1/users/{user_id}
  - PUT /api/v1/users/{user_id}/password
  - PUT /api/v1/users/{user_id}/status

- Content Management
  - GET /api/v1/contents/
  - GET /api/v1/contents/{content_id}
  - POST /api/v1/contents/
  - PUT /api/v1/contents/{content_id}
  - DELETE /api/v1/contents/{content_id}
  - GET /api/v1/contents/{content_id}/stream
  - POST /api/v1/contents/scan

- Folder Management
  - GET /api/v1/folders/
  - GET /api/v1/folders/{folder_id}
  - POST /api/v1/folders/
  - PUT /api/v1/folders/{folder_id}
  - DELETE /api/v1/folders/{folder_id}
  - GET /api/v1/folders/{folder_id}/contents

- Permissions
  - GET /api/v1/permissions/
  - POST /api/v1/permissions/
  - DELETE /api/v1/permissions/{permission_id}
  - GET /api/v1/permissions/users/{user_id}
  - PUT /api/v1/permissions/users/{user_id}

- Playback Control
  - POST /api/v1/playback/play
  - POST /api/v1/playback/pause
  - POST /api/v1/playback/resume
  - POST /api/v1/playback/stop
  - PUT /api/v1/playback/position
  - GET /api/v1/playback/current

- Playback Limits
  - GET /api/v1/limits/
  - POST /api/v1/limits/
  - PUT /api/v1/limits/{limit_id}
  - DELETE /api/v1/limits/{limit_id}
  - GET /api/v1/limits/global
  - PUT /api/v1/limits/global
  - GET /api/v1/limits/users/{user_id}
  - PUT /api/v1/limits/users/{user_id}

- Stats
  - GET /api/v1/stats/daily
  - GET /api/v1/stats/weekly
  - GET /api/v1/stats/monthly
  - GET /api/v1/stats/yearly
  - GET /api/v1/stats/users/{user_id}
  - GET /api/v1/stats/contents/{content_id}
  - GET /api/v1/stats/dashboard

## OpenAPI / Swagger
- Access the automatically generated OpenAPI schema at:
- http://localhost:8000/openapi.json
- Swagger UI available at:
- http://localhost:8000/docs
- ReDoc available at:
- http://localhost:8000/redoc
