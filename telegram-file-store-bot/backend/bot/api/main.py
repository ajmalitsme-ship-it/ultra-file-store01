from fastapi import FastAPI
from api.stream import router as stream_router
from api.admin_api import router as admin_router

app = FastAPI(
    title="Telegram File Store API",
    version="1.0.0"
)

# Public routes
app.include_router(stream_router)

# Admin routes
app.include_router(admin_router, prefix="/admin")
