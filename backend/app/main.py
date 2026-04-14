from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from .api.v1 import auth as auth_api
from .api.v1 import users as users_api
from .api.v1 import content as content_api
from .api.v1 import playback as playback_api
from .api.v1 import stats as stats_api
from .api.v1 import folders as folders_api
from .api.v1 import permissions as permissions_api
from .api.v1 import limits as limits_api

app = FastAPI(title="AudioBook Player API", version="1.0.0")

# CORS (loose for internal family server usage; adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Versioned routes
app.include_router(auth_api.router, prefix="/api/v1/auth")
app.include_router(users_api.router, prefix="/api/v1/users")
app.include_router(content_api.router, prefix="/api/v1/contents")
app.include_router(playback_api.router, prefix="/api/v1/playback")
app.include_router(stats_api.router, prefix="/api/v1/stats")
app.include_router(folders_api.router, prefix="/api/v1/folders")
app.include_router(permissions_api.router, prefix="/api/v1/permissions")
app.include_router(limits_api.router, prefix="/api/v1/limits")
